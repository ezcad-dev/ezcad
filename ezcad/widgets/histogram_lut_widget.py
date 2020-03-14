# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
"""
Copyright (c) 2012  University of North Carolina at Chapel Hill
Luke Campagnola    ('luke.campagnola@%s.com' % 'gmail')
The MIT License

Some customization to the pyqtgraph.HistogramLUTWidget
Widget displaying an image histogram along with gradient editor.
Can be used to adjust the appearance of images.
This is a wrapper around HistogramLUTItem
"""

from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.widgets.GraphicsView import GraphicsView
from ezcad.widgets.histogram_lut_item import HistogramLUTItem

__all__ = ['HistogramLUTWidget']


class HistogramLUTWidget(GraphicsView):
    
    def __init__(self, parent=None,  *args, **kwargs):
        background = kwargs.get('background', 'default')
        GraphicsView.__init__(self, parent, useOpenGL=False,
                              background=background)
        self.item = HistogramLUTItem(*args, **kwargs)
        self.setCentralItem(self.item)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred,
                           QtGui.QSizePolicy.Expanding)
        self.setMinimumWidth(95)

    def sizeHint(self):
        return QtCore.QSize(115, 200)

    def __getattr__(self, attr):
        return getattr(self.item, attr)
