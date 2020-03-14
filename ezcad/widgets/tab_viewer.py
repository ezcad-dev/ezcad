# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

# Third party imports
from qtpy.QtCore import Signal
from qtpy.QtWidgets import QTabWidget

# Local imports
from ezcad.widgets.vispy_plot import VispyPlot
from ezcad.widgets.vispy_image import VispyImage
from ezcad.widgets.vispy_volume import VispyVolume
# from ezcad.widgets.plot_widget import PlotWidget
# from ezcad.widgets.image_view import ImageView
# from ezcad.widgets.ogl_view_widget import glViewWidget

LIB_CODE = {'vispy': 'vs', 'pyqtgraph': 'pg'}
DIM_CODE = {1: 'plot', 2: 'image', 3: 'volume'}


class TabViewer(QTabWidget):
    sigCurrentViewerChanged = Signal(dict)

    def __init__(self, parent=None, options_button=None):
        QTabWidget.__init__(self, parent)
        self.parent = parent
        self.counter = 0
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        # default viewer open at launch
        self.new_viewer()

    def new_viewer(self, lib='vispy', dim=3, sec='iline'):
        self.counter += 1
        libCode = LIB_CODE[lib]
        dimCode = DIM_CODE[dim]
        if lib == 'vispy':
            name = '_'.join((str(self.counter), libCode, dimCode))
            if dim == 1:
                viewer = VispyPlot(parent=self, name=name)
            elif dim == 2:
                viewer = VispyImage(parent=self, name=name)
            elif dim == 3:
                viewer = VispyVolume(parent=self, name=name)
            else:
                raise ValueError("Unknown dimension {}".format(dim))
        # elif lib == 'pyqtgraph':
        #     name = '_'.join((str(self.counter), libCode, dimCode))
        #     if dim == 1:
        #         viewer = PlotWidget(parent=self, name=name)
        #     elif dim == 2:
        #         name = '_'.join((str(self.counter), libCode, dimCode, sec))
        #         viewer = ImageView(parent=self, name=name, section_type=sec)
        #     elif dim == 3:
        #         viewer = glViewWidget(parent=self, name=name)
        #     else:
        #         raise ValueError("Unknown dimension {}".format(dim))
        else:
            raise ValueError("Unknown library {}".format(lib))
        index = self.addTab(viewer, name)
        self.setCurrentIndex(index)

    # def new_pg_plot(self):
    #     lib, dim = 'pyqtgraph', 1
    #     self.new_viewer(lib=lib, dim=dim)
    #
    # def new_pg_image_depth(self):
    #     lib, dim, sec = 'pyqtgraph', 2, 'depth'
    #     self.new_viewer(lib=lib, dim=dim, sec=sec)
    #
    # def new_pg_image_iline(self):
    #     lib, dim, sec = 'pyqtgraph', 2, 'iline'
    #     self.new_viewer(lib=lib, dim=dim, sec=sec)
    #
    # def new_pg_image_xline(self):
    #     lib, dim, sec = 'pyqtgraph', 2, 'xline'
    #     self.new_viewer(lib=lib, dim=dim, sec=sec)
    #
    # def new_pg_image_aline(self):
    #     lib, dim, sec = 'pyqtgraph', 2, 'aline'
    #     self.new_viewer(lib=lib, dim=dim, sec=sec)

    # TODO Link map view and section view?

    def new_pg_volume(self):
        lib, dim = 'pyqtgraph', 3
        self.new_viewer(lib=lib, dim=dim)

    def new_vs_plot(self):
        lib, dim = 'vispy', 1
        self.new_viewer(lib=lib, dim=dim)

    def new_vs_image(self):
        lib, dim = 'vispy', 2
        self.new_viewer(lib=lib, dim=dim)

    def new_vs_volume(self):
        lib, dim = 'vispy', 3
        self.new_viewer(lib=lib, dim=dim)

    def close_tab(self, index):
        """
        Close tab from widget
        """
        # print("removing tab", index)
        widget = self.widget(index)
        if widget is not None:
            widget.deleteLater()
        self.removeTab(index)
