#!/usr/bin/env python
"""
Tools for working with healpix.
"""
__author__ = "Alex Drlica-Wagner"
import numpy as np
import healpy as hp
import pandas as pd

def get_map_range(hpxmap, pixel=None, nside=None, wrap_angle=180):
    """ Calculate the longitude and latitude range for a map. """
    if isinstance(hpxmap,np.ma.MaskedArray):
        hpxmap = hpxmap.data

    if pixel is None:
        nside = hp.get_nside(hpxmap)
        pixel = np.arange(len(hpxmap),dtype=int)

    ipring,=np.where(np.isfinite(hpxmap) & (hpxmap>hp.UNSEEN))
    theta,phi = hp.pix2ang(nside, pixel[ipring])
    lon = np.mod(np.degrees(phi),360)
    lat = 90.0-np.degrees(theta)

    # Small offset to add to make sure we get the whole pixel
    eps = np.degrees(hp.max_pixrad(nside))

    # CHECK ME
    hi,=np.where(lon > wrap_angle)
    lon[hi] -= 360.0

    lon_min = max(lon.min()-eps,wrap_angle-360)
    lon_max = min(lon.max()+eps,wrap_angle)
    lat_min = max(lat.min()-eps,-90)
    lat_max = min(lat.max()+eps,90)

    return (lon_min,lon_max), (lat_min,lat_max)

def hpx2xy(hpxmap, pixel=None, nside=None, xsize=800, aspect=1.0,
           lonra=None, latra=None):
    """ Convert a healpix map into x,y pixels and values"""
    if lonra is None and latra is None:
        lonra,latra = get_map_range(hpxmap,pixel,nside)
    elif (lonra is None) or (latra is None):
        msg = "Both lonra and latra must be specified"
        raise Exception(msg)

    lon = np.linspace(lonra[0],lonra[1], xsize)
    lat = np.linspace(latra[0],latra[1], int(aspect*xsize))
    lon, lat = np.meshgrid(lon, lat)

    if nside is None:
        if isinstance(hpxmap,np.ma.MaskedArray):
            nside = hp.get_nside(hpxmap.data)
        else:
            nside = hp.get_nside(hpxmap)

    try:
        pix = hp.ang2pix(nside,lon,lat,lonlat=True)
    except TypeError:
        pix = hp.ang2pix(nside,np.radians(90-lat),np.radians(lon))

    if pixel is None:
        values = hpxmap[pix]
    else:
        # Things get fancy here...
        # Match the arrays on the pixel index
        pixel_df = pd.DataFrame({'pix':pixel,'idx':np.arange(len(pixel))})
        # Pandas warns about type comparison (probably doesn't like `pix.flat`)...
        pix_df = pd.DataFrame({'pix':pix.flat},dtype=int)
        idx = pix_df.merge(pixel_df,on='pix',how='left')['idx'].values
        mask = np.isnan(idx)

        # Index the values by the matched index
        values = np.nan*np.ones(pix.shape,dtype=hpxmap.dtype)
        values = np.ma.array(values,mask=mask)
        values[np.where(~mask.reshape(pix.shape))] = hpxmap[idx[~mask].astype(int)]

    return lon,lat,values

def ang2disc(nside, lon, lat, radius, inclusive=False, fact=4, nest=False):
    """
    Wrap `query_disc` to use lon, lat, and radius in degrees.
    """
    vec = hp.ang2vec(lon,lat,lonlat=True)
    return hp.query_disc(nside,vec,np.radians(radius),inclusive,fact,nest)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args()
