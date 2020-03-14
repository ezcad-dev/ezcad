# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

"""Project console plugin"""

# Third party imports
from qtpy.QtWidgets import QVBoxLayout

# Local imports
from ezcad.config.base import _
from ezcad.plugins.base import EasyPluginWidget
from ezcad.widgets.terminal import Terminal


class ProjectConsole(EasyPluginWidget):
    """Project Console DockWidget."""
    CONF_SECTION = 'project_console'

    def __init__(self, parent):
        """Initialization."""
        EasyPluginWidget.__init__(self, parent)

        # Initialize plugin
        self.initialize_plugin()

        self.terminal = Terminal(self, options_button=self.options_button)

        layout = QVBoxLayout()
        layout.addWidget(self.terminal)
        self.setLayout(layout)

    def get_plugin_title(self):
        """Return widget title"""
        return _("Project console")

    def get_focus_widget(self):
        """
        Return the widget to give focus to when
        this plugin's dockwidget is raised on top-level
        """
        return self.terminal

    def get_plugin_actions(self):
        """Return a list of actions related to plugin"""
        return []

    def register_plugin(self):
        """Register plugin in the main window"""
        self.main.add_dockwidget(self)

        self.terminal.set_work_dir(self.main.workdir)
        self.terminal.sigRunScript.connect(self.main.run_script)

    def refresh_plugin(self, new_path=None, force_current=True):
        """Refresh log widget"""
        pass

    def closing_plugin(self, cancelable=False):
        """Perform actions before parent main window is closed"""
        return True
