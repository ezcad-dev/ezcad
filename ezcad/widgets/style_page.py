# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

from qtpy.QtWidgets import QWidget
from ezcad.widgets.property_table import refresh


class StylePage(QWidget):
    NAME = None   # configuration page name, e.g. _("General")
    ICON = None   # name of icon resource (24x24)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent = parent

        # For each style page, self.parent is the style dialog, and
        # self.parent.parent is the tree widget.
        # The style dialog has apply etc buttons and is page frame.
        # The tree widget has all data objects and is database.
        # Each style dialog serves one data object in the tree.
        # Each style dialog has one or more style pages.
        # Each style page has self.dob for loading from and applying to.

        # This line is hard to read, instead use the following OOP coding.
        # self.dob = self.parent.parent.object_data[self.parent.objname]
        if self.parent is not None:
            treebase = self.parent.parent
            object_name = self.parent.objname
            self.dob = treebase.object_data[object_name]

    def initialize(self):
        """
        Initialize configuration page:
            * setup GUI widgets
            * load settings and change widgets accordingly
        """
        self.setup_page()
        self.load_style()

    def setup_page(self):
        """Setup style page widget"""
        raise NotImplementedError

    def load_style(self):
        """Load style settings from data"""
        raise NotImplementedError

    def get_icon(self):
        """Loads page icon named by self.ICON"""
        return self.ICON

    def get_name(self):
        """Configuration page name"""
        return self.NAME

    def refresh_prop_table(self):
        refresh(self.prop_table, self.dob.prop)
