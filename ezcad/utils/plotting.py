# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
"""
Plot and visualize data
"""

import pyqtgraph as pg
import vispy as vp


# from vispy.visuals.markers import _marker_dict # TODO
symbol2char = {'circle': 'o', 'square': 's', 'triangle': 't',
               'diamond': 'd', 'plus': '+'}
color2char = {'red': 'r', 'green': 'g', 'blue': 'b', 'cyan': 'c',
              'magenta': 'm', 'yellow': 'y', 'black': 'k', 'white': 'w'}
# atom_sizeList = ['0','1','2','3','4','5','6','7','8','9','10']
atom_symbols = ['disc', 'arrow', 'ring', 'clobber', 'square', 'diamond',
                'vbar', 'hbar', 'cross', 'tailed_arrow', 'x', 'star',
                'triangle_up', 'triangle_down']
atomColorList = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow',
                 'black', 'white']


rgba_black = (0, 0, 0, 255)
rgba_white = (255, 255, 255, 255)
rgba_red = (255, 0, 0, 255)
rgba_green = (0, 255, 0, 255)
rgba_blue = (0, 0, 255, 255)


#: This is the default color gradient.
default_gradient = {'ticks': [(0, rgba_black),
                              (1, rgba_white)],
                    'mode': 'rgb'}


def make_colormap(zmin, zmax, alpha=255):
    """ make the default colormap """
    stops = [zmin, zmax]
    colors = [[0, 0, 0, alpha], [255, 0, 0, alpha]]  # black-to-red
    cmap = pg.ColorMap(stops, colors)
    return cmap


def set_gradient_alpha(gradient, alpha):
    """
    -i- gradient : dictionary, color gradient
    -i- alpha : integer, constant opacity value between 0-255.
    The pre-defined colorbar gradients all have constant alpha=255.
    This function sets it to the input constant.
    The gradient has too few control points/colors, so is not suitable for
    defining variable alpha. Maybe on LUT? TODO.
    """
    ticks = []
    for tick in gradient['ticks']:
        t = tick[0]
        r, g, b, a = tick[1]
        ticks.append((t, (r, g, b, alpha)))
    gradient['ticks'] = ticks

    # The tick in gradient is tuple, which does not support item assignment.
    # If it were list, can simply index and assign, rgba[3] = alpha
    # What is the pros/cons of using tuple or list?


def make_colormap_from_gradient(clip, gradient):
    """
    -i- clip : list, clip value, [min, max], physical values
    -i- gradient : dictionary, color gradient, grade value range is 0-1.
    -o- colormap : class object
    Scale the gradient to the clip range and return colormap.
    """
    mode = gradient['mode']
    pos, color = [], []
    for tick in gradient['ticks']:
        # scale from color tick value to physical value in clip range
        stop = clip[0] + tick[0] * (clip[1] - clip[0])
        pos.append(stop)
        color.append(tick[1])
    colormap = pg.ColorMap(pos, color, mode)  # TODO check mode
    return colormap


def make_colormap_from_gradient_vispy(gradient):
    ticks = sorted(gradient['ticks'], key=lambda tup: tup[0])
    controls, colors = [], []
    for tick in ticks:
        controls.append(tick[0])
        color = tick[1]
        color = [c/255. for c in color]
        colors.append(color)
    colormap = vp.color.Colormap(colors, controls=controls)
    return colormap


# def make_colorbar(cmap):
#     """ make the default colorbar """
#     from ezcad.widgets.colorbar import ColorBar
#     width, height = 10, 200  # in pixel?
#     cb = ColorBar(cmap, width, height, ticks=cmap.pos)
#     cb.translate(120, 60)  # (0,0) is at top left, in pixel?
#     return cb
