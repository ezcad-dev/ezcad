# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
"""
Convenient class to offload methods in data tree base class
"""

from ezcad.dialogs.colorbar_editor import ColorbarEditor
from ezcad.dialogs.camera_operator import Dialog as CameraOperatorDialog
from ezcad.widgets.dialogs import PropertyOperatorDialog, RenameObjectDialog, \
    CopyObjectDialog, RemoveObjectDialog, CreatePropertyDialog, \
    RenamePropertyDialog, RemovePropertyDialog, ConfigDialog


class Buds:
    def __init__(self, treebase=None):
        self.base = treebase
        self.main = self.base.main
        self.dob = None
        self.workerThreads = []
        self.prefs_index = None
        self.prefs_dialog_size = None

    def open_colorbar_editor(self):
        dialog = ColorbarEditor(self.base)
        dialog.show()

    def open_colorbar_editor_rc(self):
        dialog = ColorbarEditor(self.base)
        # right-clicked is also highlighted/selected ready for grab
        dialog.grab_object_rc()
        dialog.load_property()
        dialog.show()

    def open_property_operator(self):
        dialog = PropertyOperatorDialog(self.base)
        dialog.sig_start.connect(self.property_operation)
        dialog.show()

    def property_operation(self, object_name, script):
        self.dob = self.base.object_data[object_name]
        prop_names = list(self.dob.prop.keys())
        for prop_name in prop_names:
            if prop_name in script:
                new = "self.dob.prop['%s'][self.dob.prop_array_key][:]"\
                      % prop_name
                script = script.replace(prop_name, new)
        exec(script)
        # TODO update property-related values, color, clip, etc.

    def open_camera_operator(self):
        dialog = CameraOperatorDialog(self.base)
        dialog.load_from_viewer()
        dialog.show()

    def open_rename_object(self):
        dialog = RenameObjectDialog(self.base)
        dialog.sig_start.connect(self.base.rename_object)
        dialog.show()

    def open_copy_object(self):
        dialog = CopyObjectDialog(self.base)
        dialog.sig_start.connect(self.base.copy_object)
        dialog.show()

    def open_remove_object(self):
        dialog = RemoveObjectDialog(self.base)
        dialog.sig_start.connect(self.base.remove_object_worker)
        dialog.show()

    def open_rename_property(self):
        dialog = RenamePropertyDialog(self.base)
        dialog.sig_start.connect(self.base.rename_property)
        dialog.show()

    def open_remove_property(self):
        dialog = RemovePropertyDialog(self.base)
        dialog.sig_start.connect(self.base.remove_property)
        dialog.show()
 
    def open_create_property(self):
        dialog = CreatePropertyDialog(self.base)
        dialog.sig_start.connect(self.base.create_property)
        dialog.show()

    def create_property_rc(self):
        dialog = CreatePropertyDialog(self.base)
        dialog.grab_object_rc()
        dialog.sig_start.connect(self.base.create_property)
        dialog.show()

    def rename_object_rc(self):
        dialog = RenameObjectDialog(self.base)
        dialog.grab_object_rc()
        dialog.sig_start.connect(self.base.rename_object)
        dialog.show()

    def copy_object_rc(self):
        dialog = CopyObjectDialog(self.base)
        dialog.grab_object_rc()
        dialog.sig_start.connect(self.base.copy_object)
        dialog.show()

    def __preference_page_changed(self, index):
        """Preference page index has changed"""
        self.prefs_index = index

    def set_prefs_size(self, size):
        """Save preferences dialog size"""
        self.prefs_dialog_size = size

    def open_style_editor_rc(self):
        """ by right click """
        key = self.base.itemRightClicked.text(0)
        dob = self.base.object_data[key]
        self.open_style_editor(dob)

    def open_style_editor(self, dob):
        """ """
        dlg = ConfigDialog(self.base, dob.name)
        dlg.size_change.connect(self.set_prefs_size)
        if self.prefs_dialog_size is not None:
            dlg.resize(self.prefs_dialog_size)
        for stylepage in dob.style_pages:
            page = stylepage(dlg)  # dialog is page parent
            page.initialize()
            dlg.add_page(page)
        if self.prefs_index is not None:
            dlg.set_current_index(self.prefs_index)

        dlg.show()
        # dlg.check_all_settings()
        dlg.pages_widget.currentChanged.connect(self.__preference_page_changed)
        dlg.exec_()
