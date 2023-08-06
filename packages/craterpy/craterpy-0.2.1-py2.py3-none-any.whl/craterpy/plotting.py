"""This file contains helper functions for plotting.
"""
from __future__ import division, print_function, absolute_import
import matplotlib.pyplot as plt


def plot_CraterRoi(croi, figsize=((8, 8)), title=None,
                   vmin=None, vmax=None, cmap='gray', **kwargs):
    """Plot 2D CraterRoi.

    The plot offers limited arguments for basic customization. It is further
    customizable by supplying valid matplotlib.imshow() keyword-arguments. See
    matplotlib.imshow for full documentation.

    Parameters
    ----------
    roi : CraterRoi object
        2D CraterRoi to plot.
    figsize : tuple
        Length and width of plot in inches (default 8in x 8in).
    title : str
        Plot title (default 'CraterRoi').
    vmin : int or float
        Minimum pixel data value for plotting.
    vmax : int or float
        Maximum pixel data value for plotting.
    cmap : str
        Color map to plot (default 'gray'). See matplotlib.cm for full list.

    Other parameters
    ----------------
    **kwargs : object
        Keyword arguments to pass to imshow. See matplotlib.pyplot.imshow
    """
    if not title:
        title = "CraterRoi at ({}, {})".format(croi.lat, croi.lon)
    plt.figure(title, figsize=figsize)
    plt.imshow(croi, extent=croi.extent, cmap=cmap, vmin=vmin, vmax=vmax,
               **kwargs)
    plt.title(title)
    plt.xlabel('Longitude (degrees)')
    plt.ylabel('Latitude (degrees)')
    plt.show()


def plot_ejecta_stats():
    """Plot ejecta statistics.
    """
    pass  # TODO: implement this


def plot_ejecta_profile_stats():
    """Plot ejecta profile statistics.
    """
    pass  # TODO: implement this

#
# if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
