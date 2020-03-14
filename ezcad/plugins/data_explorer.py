# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

"""Data explorer plugin"""

# Third party imports
from qtpy.QtWidgets import QVBoxLayout

# Local imports
from ezcad.config.base import _
from ezcad.plugins.base import EasyPluginWidget
from ezcad.widgets.data_tree import DataTree


class DataExplorer(EasyPluginWidget):
    """Data explorer dockWidget"""
    CONF_SECTION = 'data_explorer'

    def __init__(self, parent):
        """Initialization."""
        EasyPluginWidget.__init__(self, parent)

        # Initialize plugin
        self.initialize_plugin()

        self.tree = DataTree(self, options_button=self.options_button)

        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        self.setLayout(layout)

    def get_plugin_title(self):
        """Return widget title"""
        return _("Data explorer")

    def get_focus_widget(self):
        """
        Return the widget to give focus to when
        this plugin's dockwidget is raised on top-level
        """
        return self.tree

    def get_plugin_actions(self):
        """Return a list of actions related to plugin"""
        return []

    def register_plugin(self):
        """Register plugin in the main window"""
        self.main.add_dockwidget(self)

        treebase = self.tree.base
        buds = treebase.buds

        # Every viewer must have these methods.

        treebase.sigItemChecked.connect(
            lambda item: self.main.current_viewer.add_item_agent(item))
        treebase.sigItemUnchecked.connect(
            lambda item: self.main.current_viewer.remove_item_agent(item))

        treebase.sigItemPropertyChecked.connect(
            lambda item, prop: self.main.current_viewer.add_item_prop(
            item, prop))
        treebase.sigItemPropertyUnchecked.connect(
            lambda item, prop: self.main.current_viewer.remove_item_prop(
            item, prop))

        treebase.sigCubeSectionChecked.connect(
            lambda item, section: self.main.current_viewer.add_cube_section(
            item, section))
        treebase.sigCubeSectionUnchecked.connect(
            lambda item, section: self.main.current_viewer.remove_cube_section(
            item, section))
        treebase.sig_unchecked_all.connect(
            lambda: self.main.current_viewer.clear_all())

        self.main.colorbar_editor_action.triggered.connect(
            buds.open_colorbar_editor)
        self.main.property_operator_action.triggered.connect(
            buds.open_property_operator)
        self.main.camera_operator_action.triggered.connect(
            buds.open_camera_operator)
        self.main.rename_object_action.triggered.connect(
            buds.open_rename_object)
        self.main.copy_object_action.triggered.connect(
            buds.open_copy_object)
        self.main.remove_object_action.triggered.connect(
            buds.open_remove_object)
        self.main.rename_property_action.triggered.connect(
            buds.open_rename_property)
        self.main.remove_property_action.triggered.connect(
            buds.open_remove_property)
        self.main.create_new_property_action.triggered.connect(
            buds.open_create_property)

        self.main.data_loader.sigDataObjectLoaded.connect(treebase.add_item)

    def refresh_plugin(self, new_path=None, force_current=True):
        """Refresh log widget"""
        pass

    def closing_plugin(self, cancelable=False):
        """Perform actions before parent main window is closed"""
        return True
