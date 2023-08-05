# -*- coding: utf-8 -*-
"""qwX plotting functions

   Anything plotting related goes here, these functions are imported with
   ``import quantumworldX as qw`` from there you are able to use all plot functions,
   for example to utilize `time_plot` you would use ``qw.time_plot``.

"""


import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
import mpl_toolkits.mplot3d.axes3d as axes3d
from cycler import cycler
from .core import sph_harm_real, spherical_to_cartesian
from mpl_toolkits import axes_grid1

# global variables
COLOR_MAP = 'viridis'


def plot_settings():
    params = {'legend.fontsize': 'small',
              'axes.labelsize': 'large',
              'axes.titlesize': 'medium',
              'image.cmap': COLOR_MAP,
              'lines.linewidth': 2,
              'axes.prop_cycle': cycler('color', ['#1f77b4', '#ff7f0e',
                                                  '#2ca02c', '#d62728',
                                                  '#9467bd', '#8c564b',
                                                  '#e377c2', '#7f7f7f',
                                                  '#bcbd22', '#17becf'])
              }
    mpl.rcParams.update(params)
    return


def _extend_range(v, percent=0.05):
    vmin, vmax = np.min(v), np.max(v)
    vdiff = (vmax - vmin)
    vmin -= vdiff * percent
    vmax += vdiff * percent
    return vmin, vmax


def _time_colormap(t):
    cmap = mpl.cm.get_cmap(COLOR_MAP)
    norm = mpl.colors.Normalize(vmin=np.min(t), vmax=np.max(t))

    def color_map(v):
        return cmap(norm(v))

    return color_map


def _time_colorbar(t):
    cmap = mpl.cm.get_cmap(COLOR_MAP)
    norm = mpl.colors.Normalize(vmin=np.min(t), vmax=np.max(t))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    # fake up the array of the scalar mappable
    sm._A = []
    return sm


def time_plot(x, y, t, t_step=1):
    """Plot several plots overlaid across time

    Utility plotting function that will setup plots of several snapshots in
    time (t) of a function (y) over a spatial grid (x). You can control the
    frequency of these plots with t_step, with a higher value indicating less
    frequent plots across time. At some moment after use, `plt.show` should
    be utilized to display the figure.

    Args:
        x (:obj:`np.array`): 1-D array of shape `(n)` representing a spatial
            grid
        y (:obj:`np.array`): 2-D array of shape `(n,m)` representing several
            snapshots across time of a function on a spatial grid
        t (:obj:`np.array`): 1-D array of shape `(m)` representing a time grid
        t_step (int): integer indicating how many frames to skip for plotting,
            for example, t_step=10, means it will plot every 10 frame of t,
            while t_step=1, will plot every frame possible.

    Returns:
        Does not return anything, will have a plot already loaded to be
        use along with matplotlib.pyplot (`plt.show`).

    """
    cmap = _time_colormap(t)

    for indt in range(0, len(t), t_step):
        ti = t[indt]
        plt.plot(x, y[:, indt], c=cmap(ti))

    plt.xlim(_extend_range(x))
    plt.ylim(_extend_range(y))
    plt.xlabel('$x$')
    plt.ylabel('$y$')

    plt.colorbar(_time_colorbar(t), label='time ($t$)',
                 orientation='horizontal')
    return


def time_plot1D(x, t, t_step=1):
    """Plot several plots overlaid across time for a 1-D particle.

    Utility plotting function that will setup plots of several snapshots in
    time (t) of a the position of a 1-D particle(x). You can control the
    frequency of these plots with t_step, with a higher value indicating less
    frequent plots across time. At some moment after use, `plt.show` should
    be utilized to display the figure.

    Args:
        x (:obj:`np.array`): 1-D array of shape `(n)` representing a spatial
            grid.
        t (:obj:`np.array`): 1-D array of shape `(m)` representing a time grid.
        t_step (int): integer indicating how many frames to skip for plotting,
            for example, t_step=10, means it will plot every 10 frame of t,
            while t_step=1, will plot every frame possible.

    Returns:
        Does not return anything, will have a plot already loaded to be
        use along with matplotlib.pyplot (`plt.show`).

    """
    cmap = _time_colormap(t)
    if not isinstance(x, list):
        x = [x]
    for x_arr in x:
        for indx in range(0, len(t), t_step):
            ti = t[indx]
            xi = x_arr[indx]
            plt.scatter(ti, xi, c=cmap(ti), s=100)

    plt.xlim([np.min(t), np.max(t)])
    plt.ylim(_extend_range(x))
    plt.xlabel('$t$')
    plt.ylabel('$x$')

    plt.colorbar(_time_colorbar(t), label='time ($t$)',
                 orientation='horizontal')
    return


def plot_3d_surface(xx, yy, zz):
    """Plot a 3D surface.

    Based on three `numpy.ndarray` objects xx,yy and zz of the same shape, it will plot
    the surface represented by z on the axis x and y. Typically xx and yy are
    constructed via `np.meshgrid` and then zz by a function evaluation on these
    grids.

    Args:
        xx (:obj:`np.ndarray`): 2-D coordinate array representing a spatial
            grid on the x axis.
        yy (:obj:`np.ndarray`): 2-D coordinate array representing a spatial
            grid on the y axis.
        zz (:obj:`np.ndarray`): 2-D coordinate array representing a spatial
                    grid on the z axis.

    Returns:
        Does not return anything, will have a plot already loaded to be
        use along with matplotlib.pyplot (`plt.show`).

    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # Plot as a surface
    ax.plot_surface(xx, yy, zz, rstride=8, cstride=8, alpha=0.25)
    # This sets the angle at which we view the plot
    ax.view_init(30, -60)
    # THIS IS FANCY BUT USELESS: Plots the projections onto the xy, xz, yz
    # planes
    ax.contour(xx, yy, zz, zdir='z')
    # label axes and add title
    plt.xlabel('x')
    plt.ylabel('y')
    return


def plot_contours(xx, yy, zz, vmin=None, vmax=None):
    """Plot a heatmap and level set contours of a 3d surface.

    Based on three `numpy.ndarray` objects xx,yy and zz of the same shape, it will plot
    a heatmap, a 2D colored image representing values of z across x and y, along
    with several contour level sets, curves where z is constant. Both visualizations
    provide an alternative way of looking at 3-D surfaces in a 2-D projection.

    Args:
        xx (:obj:`np.ndarray`): 2-D coordinate array representing a spatial
            grid on the x axis.
        yy (:obj:`np.ndarray`): 2-D coordinate array representing a spatial
            grid on the y axis.
        zz (:obj:`np.ndarray`): 2-D coordinate array representing a spatial
                    grid on the z axis.
        vmin (float): Mainimum value of z, used to anchor the colormap.
                      Defaults to None, which means it will calculate it dynamically.
        vmax (float): Maximum value of z, used to anchor the colormap.
                      Defaults to None, which means it will calculate it dynamically.

    Returns:
        Does not return anything, will have a plot already loaded to be
        use along with matplotlib.pyplot (`plt.show`).

    """
    cmap = mpl.cm.get_cmap(COLOR_MAP)
    plt.contour(xx, yy, zz, linewidths=3.0, cmap=cmap)
    CS = plt.contour(xx, yy, zz, colors='k', linewidths=0.5)
    im = plt.imshow(zz, interpolation='nearest',
                    extent=[xx.min(), xx.max(), yy.min(), yy.max()],
                    vmin=vmin, vmax=vmax, aspect='auto')
    plt.clabel(CS, fontsize='x-small', inline=1)
    _add_colorbar(im, label='z')
    # plt.colorbar()
    plt.xlabel('x')
    plt.ylabel('y')
    return


def _add_colorbar(im, aspect=20, pad_fraction=0.5, **kwargs):
    """Add a vertical color bar to an image plot."""
    divider = axes_grid1.make_axes_locatable(im.axes)
    width = axes_grid1.axes_size.AxesY(im.axes, aspect=1. / aspect)
    pad = axes_grid1.axes_size.Fraction(pad_fraction, width)
    current_ax = plt.gca()
    cax = divider.append_axes("right", size=width, pad=pad)
    plt.sca(current_ax)
    return im.axes.figure.colorbar(im, cax=cax, **kwargs)


def plot_spherical_harmonics(m, l):
    """Plot a spherical harmonics function on a sphere.

    This function does some matplotlib trickery to plot the  real Y_lm spherical harmonics on the surface of a 3D sphere as a colormap.

    Args:
        l (int): Quantum number l.
        m (int): Quantum number m.

    Returns:
        Does not return anything, will have a plot already loaded to be
        use along with matplotlib.pyplot (`plt.show`).

    """
    fig = plt.figure(figsize=(6, 6))
    theta = np.arange(0, 2 * np.pi, 0.01)
    phi = np.arange(0, np.pi, 0.01)
    ax = fig.add_subplot(111, projection='3d')
    theta_mg, phi_mg = np.meshgrid(theta, phi)
    # computing the spherical harmonics
    Y_lm_real = sph_harm_real(m, l, theta_mg, phi_mg)

    color_map = mpl.cm.get_cmap(name='seismic', lut=None)
    cm = mpl.cm.ScalarMappable(norm=None, cmap=color_map)
    mapped_Y_lm = cm.to_rgba(Y_lm_real)
    cm.set_array(mapped_Y_lm)

    x, y, z = spherical_to_cartesian(theta_mg, phi_mg, r=1)

    dt = np.dtype(object)
    colors = np.zeros(Y_lm_real.shape, dtype=dt)

    for ph in range(len(phi)):
        for th in range(len(theta)):
            colors[ph, th] = mapped_Y_lm[ph, th]

    ax.plot_surface(x, y, z, facecolors=colors)
    fig.colorbar(cm, shrink=0.5)
    ax.view_init(20, 45)
    ax.set_title('l=' + str(l) + ' m=' + str(m))
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    return


def plot_energy_diagram(energy_list, figsize=(14, 6), fontsize='xx-small'):
    """Plot a typical energy diagram.

    Will plot the representation of several energy levels and their associated
    quantum numbers in a energy diagram. It uses as input a list of Energy tuples.

    Args:
        energy_list (:obj:`list`): A list of dictionaries with quantum numbers and energies.
        figsize (tuple): The figure size, a tuple of width and height, defaults to (14,6).
        fontsize (string or integer): The font size of the annotations, defaults to 'xx-small'.

    Returns:
        Does not return anything, will have a plot already loaded to be
        use along with matplotlib.pyplot (`plt.show`).

    """
    e = [i['energy'] for i in energy_list]
    e_diff = np.max(e) - np.min(e)
    linewidth = 200.0
    offset_to_add = 480

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)

    eprev = 0.0
    offset = 0.0
    indx = 0.0
    for et in energy_list:
        if eprev == et['energy']:
            offset += offset_to_add
            indx = indx + 1
        else:
            offset = 0.0
            indx = 0.0

        yalign = 'top' if indx % 2 else 'bottom'
        y_offset = -e_diff * 0.01 if indx % 2 else e_diff * 0.01

        xmin = -linewidth / 2.0 + offset
        xmax = linewidth / 2.0 + offset
        y = et['energy']
        plt.hlines(y, xmin, xmax, linewidth=2)
        ax.annotate(_energy_label(et), xy=(xmin, y + y_offset),
                    fontsize=fontsize, horizontalalignment='left',
                    verticalalignment=yalign)
        eprev = et['energy']
    plt.xlim([-linewidth / 2.0 - 5.0, 2000.0])
    plt.ylim([np.min(e) - 0.05 * e_diff, np.max(e) + 0.05 * e_diff])
    plt.tick_params(axis='x', which='both', bottom='off',
                    top='off', labelbottom='off')
    plt.ylabel('Energy')
    return


def _energy_label(qdict):
    vals = []
    if 'n' in qdict.keys():
        vals.append('n={:d}'.format(qdict['n']))
    if 'l' in qdict.keys():
        vals.append('l={:d}'.format(qdict['l']))
    if 'm' in qdict.keys():
        vals.append('m={:d}'.format(qdict['m']))
    return ', '.join(vals)


def wavelength_to_colourstring(lam):
    """Convert a wavelength to a html(hex) color string.

    Will return the html/hex string associated to the color of a particular wavelength.

    Args:
        lam (float): The wavelength lambda.

    Returns:
        A string of the form '#xxxxxx'.

    """
    rgb = wavelength_to_colour(lam)
    r = int(rgb[0] * 255)
    g = int(rgb[1] * 255)
    b = int(rgb[2] * 255)
    return '#%02x%02x%02x'.format(r, g, b)


def wavelength_to_colour(lam):
    """Convert a wavelength to a RGB colour

    Will return the color associated to a particular wavelength.

    Args:
        lam (float): The wavelength lambda.

    Returns:
        A tuple (R,G,B) of colors in the 0 to 1 range.

    """
    if lam >= 380 and lam < 440:
        R = -(lam - 440.) / (440. - 350.)
        G = 0.0
        B = 1.0
    elif lam >= 440 and lam < 490:
        R = 0.0
        G = (lam - 440.) / (490. - 440.)
        B = 1.0
    elif lam >= 490 and lam < 510:
        R = 0.0
        G = 1.0
        B = -(lam - 510.) / (510. - 490.)
    elif lam >= 510 and lam < 580:
        R = (lam - 510.) / (580. - 510.)
        G = 1.0
        B = 0.0
    elif lam >= 580 and lam < 645:
        R = 1.0
        G = -(lam - 645.) / (645. - 580.)
        B = 0.0
    elif lam >= 645 and lam <= 780:
        R = 1.0
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0

    # intensity correction
    if lam >= 380 and lam < 420:
        SSS = 0.3 + 0.7 * (lam - 350) / (420 - 350)
    elif lam >= 420 and lam <= 700:
        SSS = 1.0
    elif lam > 700 and lam <= 780:
        SSS = 0.3 + 0.7 * (780 - lam) / (780 - 700)
    else:
        SSS = 0.0

    return (SSS * R, SSS * G, SSS * B)

if __name__ == "__main__":
    print("Load me as a module please")
