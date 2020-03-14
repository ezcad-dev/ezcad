# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

"""Viewer plugin"""

# Third party imports
from qtpy.QtWidgets import QVBoxLayout

# Local imports
from ezcad.config.base import _
from ezcad.plugins.base import EasyPluginWidget
from ezcad.widgets.tab_viewer import TabViewer
from ezcad.utils.functions import myprint


class Viewer(EasyPluginWidget):
    """Viewers dockWidget"""
    CONF_SECTION = 'viewer'

    def __init__(self, parent):
        """Initialization."""
        EasyPluginWidget.__init__(self, parent, has_options_button=False)

        # Initialize plugin
        self.initialize_plugin()

        self.tabs = TabViewer(self)

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def get_plugin_title(self):
        """Return widget title"""
        return _("Viewer")

    # def get_focus_widget(self):
    #     """
    #     Return the widget to give focus to when
    #     this plugin's dockwidget is raised on top-level
    #     """
    #     return self.tabs

    def get_plugin_actions(self):
        """Return a list of actions related to plugin"""
        return []

    def register_plugin(self):
        """Register plugin in the main window"""
        self.main.add_dockwidget(self)

        # connect signal (from plugin) and slot (in main)
        self.main.current_viewer = self.tabs.currentWidget().base
        self.main.current_viewer.sig_hide_all.connect(
                self.main.data_explorer.tree.base.uncheck_all_items)

        # Is this lambda using correct??
        self.main.act_plot_aspect.triggered.connect(
                lambda: self.main.current_viewer.set_aspect())
        self.main.act_bkgd_color.triggered.connect(
                lambda: self.main.current_viewer.set_background_color())
        # if viewer is image view or opengl, make the method as pass
        self.main.canvas_export_action.triggered.connect(
                lambda: self.main.current_viewer.export_canvas())

        self.tabs.currentChanged.connect(self.current_viewer_changed)

        self.tabs.sigCurrentViewerChanged.connect(
                self.main.data_explorer.tree.base.update_checks)

    def current_viewer_changed(self, index):
        # Is this redundant? Has self.tabs.currentChanged.connect()

        myprint("current tab index is ", index)
        if index == -1:  # no viewer is available
            return
        # TODO use lambda? It is repeat as in register_plugin above.
        self.main.current_viewer = self.tabs.widget(index).base
        self.main.current_viewer.sig_hide_all.connect(
                self.main.data_explorer.tree.base.uncheck_all_items)

        # update the data tree (which checked and which unchecked)
        currentItems = self.main.current_viewer.dpState
        myprint('current viewer items ', currentItems)
        self.tabs.sigCurrentViewerChanged.emit(currentItems)

    def refresh_plugin(self, new_path=None, force_current=True):
        """Refresh log widget"""
        pass

    def closing_plugin(self, cancelable=False):
        """Perform actions before parent main window is closed"""
        return True
