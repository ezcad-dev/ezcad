# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

"""Menubar+ plugin"""

# Local imports
from ezcad.config.base import _
from ezcad.plugins.base import EasyPluginWidget
from ezcad.widgets.mode_switch import ModeSwitch


class MenubarPlus(EasyPluginWidget):
    """Menubar+ DockWidget."""
    CONF_SECTION = 'menubar_plus'

    def __init__(self, parent):
        """Initialization."""
        EasyPluginWidget.__init__(self, parent, has_options_button=False)

        self.toolbar = ModeSwitch(self)

        self.toolbar.setWindowTitle(self.get_plugin_title())
        # Used to save Window state
        self.toolbar.setObjectName(self.get_plugin_title())

        self.initialize_plugin()

    def get_plugin_title(self):
        """Return widget title"""
        return _("Menubar Plus")

    def get_focus_widget(self):
        """
        Return the widget to give focus to when
        this plugin's dockwidget is raised on top-level
        """
        return self.toolbar

    def get_plugin_actions(self):
        """Return a list of actions related to plugin"""
        return []

    def register_plugin(self):
        """Register plugin in the main window"""
        # self.main.add_dockwidget(self)
        self.main.addToolBar(self.toolbar)

    def refresh_plugin(self, new_path=None, force_current=True):
        """Refresh log widget"""
        pass

    def closing_plugin(self, cancelable=False):
        """Perform actions before parent main window is closed"""
        return True
