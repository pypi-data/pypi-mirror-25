from __future__ import division, print_function, absolute_import
import numpy as np
import craterpy.helper as ch


def circle_mask(shape, radius, center=None):
    """Return boolean array of True inside circle of radius at center.

    Parameters
    ----------
    shape : tuple of int
        Shape of output boolean mask array of the form (ysize, xsize).
    radius : int or float
        Radius of circle [pixels].
    center : tuple of int
        Two element tuple of (yindex, xindex) of circle center (defaults to
        center of the mask).

    Returns
    -------
    mask : numpy 2D array

    Examples
    --------
    >>> circle_mask((3,3), 1)
    array([[False,  True, False],
           [ True,  True,  True],
           [False,  True, False]], dtype=bool)
    >>> circle_mask((3,3), 1, center=(1, 2))
    array([[False, False,  True],
           [False,  True,  True],
           [False, False,  True]], dtype=bool)
    """
    cy, cx = center if center else np.array(shape)/2 - 0.5
    height, width = shape
    x = np.arange(width) - cx
    y = np.arange(height).reshape(-1, 1) - cy
    return x*x + y*y <= radius*radius


def ellipse_mask(shape, ysize, xsize, center=None):
    """Return numpy 2D boolean array of True inside  ellipse.

    Parameters
    ----------
    shape : tuple of int
        Shape of output boolean mask array of the form (ysize, xsize).
    ysize : int or float
        Vertical semi-axis [pixels].
    xsize : int or float
        Horizontal semi-axis [pixels].
    center : tuple of int
        Two element tuple of (yindex, xindex) of ellipse center (defautls to
        center of the mask).

    Returns
    -------
    mask : numpy 2D array

    Examples
    --------
    >>> ellipse_mask((4,5), 1.5, 3)
    array([[False, False,  True, False, False],
           [ True,  True,  True,  True,  True],
           [ True,  True,  True,  True,  True],
           [False, False,  True, False, False]], dtype=bool)
    >>> ellipse_mask((4,5), 1.5, 3, center=(1.5, 3))
    array([[False, False, False,  True, False],
           [False,  True,  True,  True,  True],
           [False,  True,  True,  True,  True],
           [False, False, False,  True, False]], dtype=bool)
    """
    cy, cx = center if center else np.array(shape)/2 - 0.5
    height, width = shape
    y, x = np.ogrid[-cy:height-cy, -cx:width-cx]
    return (x*x)/(xsize*xsize) + (y*y)/(ysize*ysize) <= 1


def ring_mask(shape, rmin, rmax, center=None):
    """Return bool array of True in a circular ring from rmin to rmax.

    Parameters
    ----------
    shape : tuple of int
        Shape of output boolean mask array of the form (ysize, xsize).
    rmin : int or float
        Inner ring radius [pixels].
    rmax : int or float
        Outer ring radius [pixels].
    center : tuple of int
        Two element tuple of (yindex, xindex) of ellipse center (defautls to
        center of the mask).

    Returns
    -------
    mask : numpy 2D array

    Examples
    --------
    >>> ring_mask((5,5), 1, 2)
    array([[False, False,  True, False, False],
           [False,  True, False,  True, False],
           [ True, False, False, False,  True],
           [False,  True, False,  True, False],
           [False, False,  True, False, False]], dtype=bool)
    >>> ring_mask((5,5), 0.5, 1.5)
    array([[False, False, False, False, False],
           [False,  True,  True,  True, False],
           [False,  True, False,  True, False],
           [False,  True,  True,  True, False],
           [False, False, False, False, False]], dtype=bool)
    """
    inner = circle_mask(shape, rmin, center)
    outer = circle_mask(shape, rmax, center)
    return outer*~inner


def crater_floor_mask(croi):
    """Return bool mask of interior of a crater in a CraterRoi.

    Parameters
    ----------
    croi : CraterRoi
        Crater region of interest specifying crater to mask

    Returns
    -------
    mask : numpy 2D array

    Examples
    --------
    """
    pixwidth = ch.km2pix(croi.rad, croi.cds.calc_mpp(croi.lat))
    pixheight = ch.km2pix(croi.rad, croi.cds.calc_mpp())
    return ellipse_mask(croi.roi.shape, pixwidth, pixheight)


def crater_ring_mask(croi, rmin, rmax):
    """Return bool mask of interior of a ring aroun a crater in a CraterRoi.

    Ring is calculated by subtracting an inner ellipse mask from an outer
    ellipse mask which are specified by rmin and rmax, respectively.

    Parameters
    ----------
    croi : CraterRoi
        Crater region of interest specifying crater to mask
    rmin : int or float
        Inner ring radius [km].
    rmax : int or float
        Outer ring radius [km].

    Returns
    -------
    mask : numpy 2D array

    Examples
    --------
    """
    rmax_pixheight = ch.km2pix(rmax, croi.cds.calc_mpp())
    rmax_pixwidth = ch.km2pix(rmax, croi.cds.calc_mpp(croi.lat))
    rmin_pixheight = ch.km2pix(rmin, croi.cds.calc_mpp())
    rmin_pixwidth = ch.km2pix(rmin, croi.cds.calc_mpp(croi.lat))
    outer = ellipse_mask(croi.roi.shape, rmax_pixwidth, rmax_pixheight)
    inner = ellipse_mask(croi.roi.shape, rmin_pixwidth, rmin_pixheight)
    return outer * ~inner


def polygon_mask(croi, poly_verts):
    """Mask the region inside a polygon given by poly_verts.

    Uses the matplotlib.Path module and included contains_points() method to
    calculate the interior of a polygon specified as a list of (lat, lon)
    vertices.

    Parameters
    ==========
    croi : CraterRoi
        Crater region of interest being masked.
    poly_verts : list of tuple
        List of (lon, lat) polygon vertices.

    Returns
    -------
    mask : numpy 2D array

    Example
    =======
    >>> import os.path as p
    >>> f = p.join(p.dirname(p.abspath('__file__')), 'examples', 'moon.tif')
    >>> cds = CraterpyDataset(f, radius=1737)
    >>> croi = CraterRoi(cds, -27.2, 80.9, 207)  # Humboldt crater
    >>> poly = [[-27.5, 80.5], [-28, 80.5], [-28, 81], [-27.5, 81]]
    >>> mask = polygon_mask(cds, roi, extent, poly)
    >>> croi.mask(mask)
    >>> croi.plot()
    """
    from matplotlib.path import Path
    minlon, maxlon, minlat, maxlat = croi.extent
    # Create grid
    nlat, nlon = croi.roi.shape
    x, y = np.meshgrid(np.arange(nlon), np.arange(nlat))
    x, y = x.flatten(), y.flatten()
    gridpoints = np.vstack((x, y)).T
    poly_pix = [(ch.deg2pix(lon-minlon, croi.cds.ppd),
                ch.deg2pix(lat-minlat, croi.cds.ppd))
                for lon, lat in poly_verts]
    path = Path(poly_pix)
    mask = path.contains_points(gridpoints).reshape((nlat, nlon))
    return mask
