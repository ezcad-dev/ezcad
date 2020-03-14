# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

"""Process log plugin"""

# Third party imports
from qtpy.QtWidgets import QVBoxLayout

# Local imports
from ezcad.config.base import _
from ezcad.plugins.base import EasyPluginWidget
from ezcad.widgets.log_box import LogBox


class ProcessLog(EasyPluginWidget):
    """Process Log DockWidget."""
    CONF_SECTION = 'process_log'

    def __init__(self, parent):
        """Initialization."""
        EasyPluginWidget.__init__(self, parent)

        # Initialize plugin
        self.initialize_plugin()

        self.logbox = LogBox(self, options_button=self.options_button)

        # Find/replace widget
        # self.find_widget = FindReplace(self)
        # self.find_widget.set_editor(self.logbox.textBrowser)
        # self.find_widget.hide()
        # self.register_widget_shortcuts(self.find_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.logbox)
        # layout.addWidget(self.find_widget)
        self.setLayout(layout)

    def get_plugin_title(self):
        """Return widget title"""
        return _("Process log")

    def get_focus_widget(self):
        """
        Return the widget to give focus to when
        this plugin's dockwidget is raised on top-level
        """
        return self.logbox.textBrowser

    def get_plugin_actions(self):
        """Return a list of actions related to plugin"""
        return []

    def register_plugin(self):
        """Register plugin in the main window"""
        self.main.add_dockwidget(self)

    def refresh_plugin(self, new_path=None, force_current=True):
        """Refresh log widget"""
        pass

    def closing_plugin(self, cancelable=False):
        """Perform actions before parent main window is closed"""
        return True
