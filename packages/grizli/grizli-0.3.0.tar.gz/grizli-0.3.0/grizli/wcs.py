#!/usr/bin/env python
# encoding: utf-8
"""
Tools for WCS manipulation

(These are all mostly duplicated from `utils`, need to point here in all 
the necessary places.)
"""

import numpy as np

import astropy.io.fits as pyfits
import astropy.wcs as pywcs

def get_wcs_pscale(wcs):
    """Get correct pscale from a `~astropy.wcs.WCS` object
    
    
    Parameters
    ----------
    wcs : `~astropy.wcs.WCS`
        
    Returns
    -------
    pscale : float
        Pixel scale from `wcs.cd`
        
    """
    from numpy import linalg
    det = linalg.det(wcs.wcs.cd)
    pscale = np.sqrt(np.abs(det)) * 3600.
    return pscale
    
def transform_wcs(in_wcs, translation=[0.,0.], rotation=0., scale=1.):
    """Update WCS with shift, rotation, & scale
    
    
    Paramters
    ---------
    in_wcs: `~astropy.wcs.WCS`
        Input WCS
        
    translation: [float, float]
        xshift & yshift in pixels
    
    rotation: float
        CCW rotation (towards East), radians
    
    scale: float
        Pixel scale factor
    
    Returns
    -------
    out_wcs: `~astropy.wcs.WCS`
        Modified WCS
    """
    out_wcs = in_wcs.deepcopy()
    out_wcs.wcs.crpix += np.array(translation)
    theta = -rotation
    _mat = np.array([[np.cos(theta), -np.sin(theta)],
                     [np.sin(theta), np.cos(theta)]])
    
    out_wcs.wcs.cd = np.dot(out_wcs.wcs.cd, _mat)/scale
    out_wcs.pscale = get_wcs_pscale(out_wcs)
    out_wcs.wcs.crpix *= scale
    if hasattr(out_wcs, '_naxis1'):
        out_wcs._naxis1 = int(np.round(out_wcs._naxis1*scale))
        out_wcs._naxis2 = int(np.round(out_wcs._naxis2*scale))
        
    return out_wcs

def reproject_faster(input_hdu, output, pad=10, **kwargs):
    """Speed up `reproject` module with array slices of the input image

    
    Parameters
    ----------
    input_hdu : `~astropy.io.fits.ImageHDU`
        Input image HDU to reproject.  
        
    output : `~astropy.wcs.WCS` or `~astropy.io.fits.Header`
        Output frame definition.
    
    pad : int
        Pixel padding on slices cut from the `input_hdu`.
        
    kwargs : dict
        Arguments passed through to `~reproject.reproject_interp`.  For 
        example, `order='nearest-neighbor'`.
    
    Returns
    -------
    reprojected : `~numpy.ndarray`
        Reprojected data from `input_hdu`.
        
    footprint : `~numpy.ndarray`
        Footprint of the input array in the output frame.
    
    .. note::
    
    `reproject' is an astropy-compatible module that can be installed with 
    `pip`.  See https://reproject.readthedocs.io.
     
    """
    import reproject
    
    # Output WCS
    if isinstance(output, pywcs.WCS):
        out_wcs = output
    else:
        out_wcs = pywcs.WCS(output, relax=True)
    
    if 'SIP' in out_wcs.wcs.ctype[0]:
        print('Warning: `reproject` doesn\'t appear to support SIP projection')
        
    # Compute pixel coordinates of the output frame corners in the input image
    input_wcs = pywcs.WCS(input_hdu.header, relax=True)
    out_fp = out_wcs.calc_footprint()
    input_xy = input_wcs.all_world2pix(out_fp, 0)
    slx = slice(int(input_xy[:,0].min())-pad, int(input_xy[:,0].max())+pad)
    sly = slice(int(input_xy[:,1].min())-pad, int(input_xy[:,1].max())+pad)
    
    # Make the cutout
    sub_data = input_hdu.data[sly, slx]
    sub_header = wcs_to_header(get_slice_wcs(input_wcs, slx, sly), relax=True)
    sub_hdu = pyfits.PrimaryHDU(data=sub_data, header=sub_header)
    
    # Get the reprojection
    seg_i, fp_i = reproject.reproject_interp(sub_hdu, output, **kwargs)
    return seg_i.astype(sub_data.dtype), fp_i.astype(np.uint8)

def full_spectrum_wcsheader(center_wave=1.4e4, dlam=40, NX=100, spatial_scale=1, NY=10):
    """Make a WCS header for a 2D spectrum
    
    
    Parameters
    ----------
    center_wave : float
        Wavelength of the central pixel, in Anstroms
        
    dlam : float
        Delta-wavelength per (x) pixel
        
    NX, NY : int
        Number of x & y pixels. Output will have shape `(2*NY, 2*NX)`.
        
    spatial_scale : float
        Spatial scale of the output, in units of the input pixels
    
    Returns
    -------
    header : `~astropy.io.fits.Header`
        Output WCS header
    
    wcs : `~astropy.wcs.WCS`
        Output WCS
    
    Examples
    --------
        
        >>> from grizli.utils import make_spectrum_wcsheader
        >>> h, wcs = make_spectrum_wcsheader()
        >>> print(wcs)
        WCS Keywords
        Number of WCS axes: 2
        CTYPE : 'WAVE'  'LINEAR'  
        CRVAL : 14000.0  0.0  
        CRPIX : 101.0  11.0  
        CD1_1 CD1_2  : 40.0  0.0  
        CD2_1 CD2_2  : 0.0  1.0  
        NAXIS    : 200 20

    """
    
    h = pyfits.ImageHDU(data=np.zeros((2*NY, 2*NX), dtype=np.float32))
    
    refh = h.header
    refh['CRPIX1'] = NX+1
    refh['CRPIX2'] = NY+1
    refh['CRVAL1'] = center_wave/1.e4
    refh['CD1_1'] = dlam/1.e4
    refh['CD1_2'] = 0.
    refh['CRVAL2'] = 0.
    refh['CD2_2'] = spatial_scale
    refh['CD2_1'] = 0.
    refh['RADESYS'] = ''
    
    refh['CTYPE1'] = 'RA---TAN-SIP'
    refh['CUNIT1'] = 'mas'
    refh['CTYPE2'] = 'DEC--TAN-SIP'
    refh['CUNIT2'] = 'mas'
    
    ref_wcs = pywcs.WCS(refh)    
    ref_wcs.pscale = get_wcs_pscale(ref_wcs)
    
    return refh, ref_wcs
    
def make_spectrum_wcsheader(center_wave=1.4e4, dlam=40, NX=100, spatial_scale=1, NY=10):
    """Make a WCS header for a 2D spectrum
    
    
    Parameters
    ----------
    center_wave : float
        Wavelength of the central pixel, in Anstroms
        
    dlam : float
        Delta-wavelength per (x) pixel
        
    NX, NY : int
        Number of x & y pixels. Output will have shape `(2*NY, 2*NX)`.
        
    spatial_scale : float
        Spatial scale of the output, in units of the input pixels
    
    Returns
    -------
    header : `~astropy.io.fits.Header`
        Output WCS header
    
    wcs : `~astropy.wcs.WCS`
        Output WCS
    
    Examples
    --------
        
        >>> from grizli.utils import make_spectrum_wcsheader
        >>> h, wcs = make_spectrum_wcsheader()
        >>> print(wcs)
        WCS Keywords
        Number of WCS axes: 2
        CTYPE : 'WAVE'  'LINEAR'  
        CRVAL : 14000.0  0.0  
        CRPIX : 101.0  11.0  
        CD1_1 CD1_2  : 40.0  0.0  
        CD2_1 CD2_2  : 0.0  1.0  
        NAXIS    : 200 20

    """
    
    h = pyfits.ImageHDU(data=np.zeros((2*NY, 2*NX), dtype=np.float32))
    
    refh = h.header
    refh['CRPIX1'] = NX+1
    refh['CRPIX2'] = NY+1
    refh['CRVAL1'] = center_wave
    refh['CD1_1'] = dlam
    refh['CD1_2'] = 0.
    refh['CRVAL2'] = 0.
    refh['CD2_2'] = spatial_scale
    refh['CD2_1'] = 0.
    refh['RADESYS'] = ''
    
    refh['CTYPE1'] = 'WAVE'
    refh['CTYPE2'] = 'LINEAR'
    
    ref_wcs = pywcs.WCS(h.header)
    ref_wcs.pscale = np.sqrt(ref_wcs.wcs.cd[0,0]**2 + ref_wcs.wcs.cd[1,0]**2)*3600.
    
    return refh, ref_wcs

def wcs_to_header(wcs, relax=True):
    """Modify `astropy.wcs.WCS.to_header` to produce more keywords
    
    
    Parameters
    ----------
    wcs : `~astropy.wcs.WCS`
        Input WCS.
    
    relax : bool
        Passed to `WCS.to_header(relax=)`.
        
    Returns
    -------
    header : `~astropy.io.fits.Header`
        Output header.
        
    """
    header = wcs.to_header(relax=relax)
    if hasattr(wcs, '_naxis1'):
        header['NAXIS'] = wcs.naxis
        header['NAXIS1'] = wcs._naxis1
        header['NAXIS2'] = wcs._naxis2
    
    for k in header:
        if k.startswith('PC'):
            cd = k.replace('PC','CD')
            header.rename_keyword(k, cd)
    
    return header
    
def make_wcsheader(ra=40.07293, dec=-1.6137748, size=2, pixscale=0.1, get_hdu=False, theta=0):
    """Make a celestial WCS header
    
        
    Parameters
    ----------
    ra, dec : float
        Celestial coordinates in decimal degrees
        
    size, pixscale : float or 2-list
        Size of the thumbnail, in arcsec, and pixel scale, in arcsec/pixel.
        Output image will have dimensions `(npix,npix)`, where
            
            >>> npix = size/pixscale
            
    get_hdu : bool
        Return a `~astropy.io.fits.ImageHDU` rather than header/wcs.
        
    theta : float
        Position angle of the output thumbnail
    
    Returns
    -------
    hdu : `~astropy.io.fits.ImageHDU` 
        HDU with data filled with zeros if `get_hdu=True`.
    
    header, wcs : `~astropy.io.fits.Header`, `~astropy.wcs.WCS`
        Header and WCS object if `get_hdu=False`.

    Examples
    --------
    
        >>> from grizli.utils import make_wcsheader
        >>> h, wcs = make_wcsheader()
        >>> print(wcs)
        WCS Keywords
        Number of WCS axes: 2
        CTYPE : 'RA---TAN'  'DEC--TAN'  
        CRVAL : 40.072929999999999  -1.6137748000000001  
        CRPIX : 10.0  10.0  
        CD1_1 CD1_2  : -2.7777777777777e-05  0.0  
        CD2_1 CD2_2  : 0.0  2.7777777777777701e-05  
        NAXIS    : 20 20
        
        >>> from grizli.utils import make_wcsheader
        >>> hdu = make_wcsheader(get_hdu=True)
        >>> print(hdu.data.shape)
        (20, 20)
        >>> print(hdu.header.tostring)
        XTENSION= 'IMAGE   '           / Image extension                                
        BITPIX  =                  -32 / array data type                                
        NAXIS   =                    2 / number of array dimensions                     
        PCOUNT  =                    0 / number of parameters                           
        GCOUNT  =                    1 / number of groups                               
        CRPIX1  =                   10                                                  
        CRPIX2  =                   10                                                  
        CRVAL1  =             40.07293                                                  
        CRVAL2  =           -1.6137748                                                  
        CD1_1   = -2.7777777777777E-05                                                  
        CD1_2   =                  0.0                                                  
        CD2_1   =                  0.0                                                  
        CD2_2   = 2.77777777777777E-05                                                  
        NAXIS1  =                   20                                                  
        NAXIS2  =                   20                                                  
        CTYPE1  = 'RA---TAN'                                                            
        CTYPE2  = 'DEC--TAN'
    """
    
    if np.isscalar(pixscale):
        cdelt = [pixscale/3600.]*2
    else:
        cdelt = [pixscale[0]/3600., pixscale[1]/3600.]
        
    if np.isscalar(size):
        npix = np.cast[int]([size/pixscale, size/pixscale])
    else:
        npix = np.cast[int]([size[0]/pixscale, size[1]/pixscale])
        
    hout = pyfits.Header()
    hout['CRPIX1'] = npix[0] / 2
    hout['CRPIX2'] = npix[1] / 2
    hout['CRVAL1'] = ra
    hout['CRVAL2'] = dec
    hout['CD1_1'] = -1 * cdelt[0]
    hout['CD1_2'] = hout['CD2_1'] = 0.
    hout['CD2_2'] = cdelt[1]
    hout['NAXIS1'] = npix[0]
    hout['NAXIS2'] = npix[1]
    hout['CTYPE1'] = 'RA---TAN'
    hout['CTYPE2'] = 'DEC--TAN'
    
    wcs_out = pywcs.WCS(hout)
    
    theta_rad = np.deg2rad(theta)
    mat = np.array([[np.cos(theta_rad), -np.sin(theta_rad)], 
                    [np.sin(theta_rad),  np.cos(theta_rad)]])

    rot_cd = np.dot(mat, wcs_out.wcs.cd)
    
    for i in [0,1]:
        for j in [0,1]:
            hout['CD{0:d}_{1:d}'.format(i+1, j+1)] = rot_cd[i,j]
            wcs_out.wcs.cd[i,j] = rot_cd[i,j]
                
    wcs_out.pscale = get_wcs_pscale(wcs_out)
        
    if get_hdu:
        hdu = pyfits.ImageHDU(header=hout, data=np.zeros((npix[1], npix[0]), dtype=np.float32))
        return hdu
    else:
        return hout, wcs_out

def add_padding_to_wcs(wcs_in, pad=200):
    """Pad the appropriate WCS keywords"""
    wcs = wcs_in.deepcopy()
    
    for attr in ['naxis1', '_naxis1', 'naxis2', '_naxis2']:
        if hasattr(wcs, attr):
            value = wcs.__getattribute__(attr) 
            if value is not None:
                wcs.__setattr__(attr, value+2*pad)
    
    wcs.naxis1 = wcs._naxis1
    wcs.naxis2 = wcs._naxis2
    
    wcs.wcs.crpix[0] += pad
    wcs.wcs.crpix[1] += pad
    
    # Pad CRPIX for SIP
    for wcs_ext in [wcs.sip]:
        if wcs_ext is not None:
            wcs_ext.crpix[0] += pad
            wcs_ext.crpix[1] += pad
    
    # Pad CRVAL for Lookup Table, if necessary (e.g., ACS)        
    for wcs_ext in [wcs.cpdis1, wcs.cpdis2, wcs.det2im1, wcs.det2im2]:
        if wcs_ext is not None:
            wcs_ext.crval[0] += pad
            wcs_ext.crval[1] += pad
    
    return wcs

    
def get_slice_wcs(wcs, slx=slice(480,520), sly=slice(480,520)):
    """Get slice of a WCS including higher orders like SIP and DET2IM
    
    The normal `~astropy.wcs.wcs.WCS` `slice` method doesn't apply the
    slice to all of the necessary keywords.  For example, SIP WCS also
    has a `CRPIX` reference pixel that needs to be offset along with
    the main `CRPIX`.
    
    Parameters
    ----------
    slx, sly : slice
        Slices in x and y dimensions to extract
    
    """
    NX = slx.stop - slx.start
    NY = sly.stop - sly.start
    
    slice_wcs = wcs.slice((sly, slx))
    slice_wcs.naxis1 = slice_wcs._naxis1 = NX
    slice_wcs.naxis2 = slice_wcs._naxis2 = NY
    
    if hasattr(slice_wcs, 'sip'):
        if slice_wcs.sip is not None:
            for c in [0,1]:
                slice_wcs.sip.crpix[c] = slice_wcs.wcs.crpix[c]
    
    ACS_CRPIX = [4096/2,2048/2] # ACS
    dx_crpix = slice_wcs.wcs.crpix[0] - ACS_CRPIX[0]
    dy_crpix = slice_wcs.wcs.crpix[1] - ACS_CRPIX[1]
    for ext in ['cpdis1','cpdis2','det2im1','det2im2']:
        if hasattr(slice_wcs, ext):
            wcs_ext = slice_wcs.__getattribute__(ext)
            if wcs_ext is not None:
                wcs_ext.crval[0] += dx_crpix
                wcs_ext.crval[1] += dy_crpix
                slice_wcs.__setattr__(ext, wcs_ext)
    
    return slice_wcs