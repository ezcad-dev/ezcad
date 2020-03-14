# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

"""
"""

# Third party imports
from qtpy.QtCore import Qt, QSize
from qtpy.QtWidgets import QWidget, QHBoxLayout, QMessageBox

# Local imports
from ezcad.widgets.vispy_canvas import VispyCanvas
from ezcad.utils.qthelpers import (create_plugin_layout, create_toolbutton,
    create_toolbutton_help)
from ezcad.utils import icon_manager as ima
from ezcad.config.base import _
from ezcad.utils.logger import logger


class VispyPlot(QWidget):

    def __init__(self, parent=None, options_button=None, name=None):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.base = PlotBase(parent=self, name=name)

        btn_layout = QHBoxLayout()
        for btn in self.setup_buttons():
            btn.setIconSize(QSize(16, 16))
            btn_layout.addWidget(btn)
        if options_button:
            btn_layout.addStretch()
            btn_layout.addWidget(options_button, Qt.AlignRight)

        layout = create_plugin_layout(btn_layout, self.base)
        self.setLayout(layout)

        self.base.canvas.show() # show after parent widgets are in place

    def setup_buttons(self):
        hide_all_btn = create_toolbutton(self,
            icon=ima.icon('hide_all'),
            tip=_('Hide all'),
            shortcut="Ctrl+L",
            triggered=self.base.hide_all)
        self.pick_btn = create_toolbutton(self,
            icon=ima.icon('pick_mode'),
            tip=_('Pick mode'), shortcut="P",
            toggled=self.base.toggle_pick_mode)
        color_btn = create_toolbutton(self,
            icon=ima.icon('bkgd_color'),
            tip=_('Background color'),
            triggered=self.base.set_background_color)
        export_btn = create_toolbutton(self,
            icon=ima.icon('photo'),
            tip=_('Export canvas to picture'),
            triggered=self.base.export_canvas)
        help_btn = create_toolbutton_help(self,
            triggered=self.show_help)
        return (hide_all_btn, self.pick_btn, color_btn, export_btn,
            help_btn)

    def show_help(self):
        QMessageBox.information(self, _('How to use'), self.base.HELP)


class PlotBase(VispyCanvas):
    NAME = _('vispy plot')

    def __init__(self, parent=None, name=None):
        super(PlotBase, self).__init__(parent=parent, name=name)
        ax = self.canvas00
        ax.plot([[0, 0], [1, 1]]) # to show axis by aid of a line
        ax.visuals[0].parent = None # to hide the line
        ax.visuals.pop(0) # remove from list

        self.camera = self.canvas00.camera
        self.view = self.canvas00.view
        self.aspect_method = "Equal"
        self.aspect_ratio = 1.0

        # TODO think about subclass canvas and use signal/slot for picking
        #self.canvas = Canvas(show=True, keys='interactive', bgcolor='white')
        #self.canvas.show()

    @property
    def aspect_ratio(self):
        return self.camera.aspect

    @aspect_ratio.setter
    def aspect_ratio(self, value):
        self.camera.aspect = value

    @property
    def state(self):
        """
        -o- state : dict, used for save viewer to database
        """
        state = {}
        state['aspect_method'] = self.aspect_method
        state['aspect_ratio'] = self.aspect_ratio
        state['bgcolor'] = self.bgcolor.rgba
        return state

    @state.setter
    def state(self, state):
        if 'aspect_method' in state:
            self.aspect_method = state['aspect_method']
        if 'aspect_ratio' in state:
            self.aspect_ratio = state['aspect_ratio']
        if 'bgcolor' in state:
            self.bgcolor = state['bgcolor']

    def add_item_agent(self, dob):
        parent = self._name
        geom = dob.geometry_type
        if geom not in ['Point', 'Label', 'Line']:
            QMessageBox.critical(self, _("Warning"),
                _("{} cannot display {}".format(parent, dob.name)))
            return

        logger.info('{} is adding {}'.format(parent, dob.name))
        if parent not in dob.vs2d:
            dob.make_vs2d(parent=parent)
        item = dob.vs2d[parent]
        self.add_item(item)
        self.save_display_state(dob.name, 'object', 'self', True)

    def add_item(self, item):
        self.view.add(item)
        self.canvas.visuals.append(item)
        self.camera.set_range()

    def remove_item_agent(self, dob):
        parent = self._name
        name = dob.name
        key = 'object'
        if name in self.dpState:
            if key in self.dpState[name]:
                if self.dpState[name][key]['self']:
                    logger.info('{} is removing {}'.format(parent, name))
                    try:
                        item = dob.vs2d[parent]
                        self.remove_item(item)
                    except ValueError as e:
                        print("Ignore %s" % str(e))
                    self.save_display_state(dob.name, 'object', 'self', False)
