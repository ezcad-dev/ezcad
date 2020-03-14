# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

"""
Template dialog that includes convenient methods to creating common components.
"""

# Standard library imports
import os.path as osp

# Third party imports
from qtpy.compat import getopenfilename, getsavefilename, getexistingdirectory
from qtpy.QtCore import Qt, QRegExp
from qtpy.QtGui import QRegExpValidator
from qtpy.QtWidgets import (QWidget, QDialog, QLabel, QLineEdit, QPushButton,
    QMessageBox, QVBoxLayout, QHBoxLayout, QComboBox, QGridLayout)

# Local imports
from ezcad.config.base import _, getcwd_or_home
from ezcad.utils import icon_manager as ima
from ezcad.utils.functions import to_text_string


class EasyDialog(QDialog):
    NAME = _("Template Dialog")
    HELP_HEAD = _("How to use")
    HELP_BODY = _("Sorry no help is available")

    def __init__(self, parent=None, set_tree=False, set_db=False, test=False):
        """Initialize.

        :param parent: parent
        :type parent: QWidget
        :param set_tree: set connection to tree
        :type set_tree: bool
        :param set_db: set connection to DB
        :type set_db: bool
        :param test: test mode
        :type test: bool
        """
        QDialog.__init__(self, parent)
        self.setWindowTitle(self.NAME)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.parent = parent
        self.treebase = parent # for grab object
        self.object_name = None
        # Use less wires and more signal/slot
        if set_tree:
            self.treebase = parent  # connection wire to outside world
            if self.treebase is not None:
                self.mainwindow = self.treebase.main
        if set_db and self.treebase is not None:
            self.database = self.treebase.object_data
        if test:
            self.test()

    def test(self):
        vbox = QVBoxLayout()
        label1 = QLabel(_("Open existing file"))
        file1 = self.create_browsefile(_("File"))
        label2 = QLabel(_("Create new file"))
        file2 = self.create_browsefile(_("File"), new=True)
        vbox.addWidget(label1)
        vbox.addWidget(file1)
        vbox.addWidget(label2)
        vbox.addWidget(file2)
        self.setLayout(vbox)

    def create_action(self, ok=True, apply_label='Apply'):
        """Create action buttons.

        :param ok: have the OK button
        :type ok: bool
        :param apply_label: label of the apply button
        :type apply_label: str
        :return: QWidget
        """
        if ok:
            btn_ok = QPushButton(_('OK'))
            btn_ok.clicked.connect(self.apply_and_close)
        btn_apply = QPushButton(_(apply_label))
        btn_apply.clicked.connect(self.apply)
        btn_close = QPushButton(_('Cancel'))
        btn_close.clicked.connect(self.close)
        btn_help = QPushButton(_('Help'))
        btn_help.clicked.connect(self.show_help)
        layout = QHBoxLayout()
        layout.addStretch()
        if ok:
            layout.addWidget(btn_ok)
        layout.addWidget(btn_apply)
        layout.addWidget(btn_close)
        layout.addWidget(btn_help)
        action = QWidget(self)
        action.setLayout(layout)
        return action

    def apply_and_close(self):
        """Apply and close."""
        self.apply()
        self.close()

    def show_help(self):
        """Show help message."""
        # logger.warning(self.HELP_BODY)
        QMessageBox.information(self, self.HELP_HEAD, self.HELP_BODY)

    def create_cubeframe(self):
        widget = QWidget(self)
        lbl_iline = QLabel(_("Iline first, last, step"))
        widget.le_il_frst = QLineEdit()
        widget.le_il_last = QLineEdit()
        widget.le_il_ncrt = QLineEdit()
        lbl_xline = QLabel(_("Xline first, last, step"))
        widget.le_xl_frst = QLineEdit()
        widget.le_xl_last = QLineEdit()
        widget.le_xl_ncrt = QLineEdit()
        lbl_depth = QLabel(_("Depth first, last, step"))
        widget.le_dp_frst = QLineEdit()
        widget.le_dp_last = QLineEdit()
        widget.le_dp_ncrt = QLineEdit()
        layout = QGridLayout()
        layout.addWidget(lbl_iline, 0, 0)
        layout.addWidget(widget.le_il_frst, 0, 1)
        layout.addWidget(widget.le_il_last, 0, 2)
        layout.addWidget(widget.le_il_ncrt, 0, 3)
        layout.addWidget(lbl_xline, 1, 0)
        layout.addWidget(widget.le_xl_frst, 1, 1)
        layout.addWidget(widget.le_xl_last, 1, 2)
        layout.addWidget(widget.le_xl_ncrt, 1, 3)
        layout.addWidget(lbl_depth, 2, 0)
        layout.addWidget(widget.le_dp_frst, 2, 1)
        layout.addWidget(widget.le_dp_last, 2, 2)
        layout.addWidget(widget.le_dp_ncrt, 2, 3)
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)
        return widget

    def create_combobox(self, text, choices=None, tip=None):
        """Create a combo box.

        :param text: label
        :type text: str
        :param choices: selection choices
        :type choices: dict
        :param tip: tool tip
        :type tip: str
        :return: QWidget
        """
        label = QLabel(text)
        combobox = QComboBox()
        # combobox.setMinimumContentsLength(10)
        combobox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        if tip is not None:
            combobox.setToolTip(tip)
        if choices is not None:
            for name, key in choices:
                if not (name is None and key is None):
                    # combobox.addItem(name, to_qvariant(key))
                    combobox.addItem(name, key)
        # Insert separators
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(combobox)
        layout.addStretch(1)
        layout.setContentsMargins(0, 0, 0, 0)
        widget = QWidget(self)
        widget.label = label
        widget.combobox = combobox
        widget.setLayout(layout)
        return widget

    def create_grabob(self, text, default=None, tip=None, geom=None):
        """Create grab object widget.

        :param text: key
        :type text: str
        :param default: default value
        :type default: str
        :param tip: tool tip
        :type tip: str
        :param geom: geometry of the object to grab
        :type geom: list
        :return: QWidget
        """
        widget = self.create_lineedit(text, default=default, tip=tip)
        edit = widget.edit
        browse_btn = QPushButton(ima.icon('grab_object'), '', self)
        browse_btn.setToolTip(_("Grab object from tree"))
        browse_btn.clicked.connect(lambda: self.grab_object(edit, geom))
        layout = QHBoxLayout()
        layout.addWidget(widget)
        layout.addWidget(browse_btn)
        layout.setContentsMargins(0, 0, 0, 0)
        grabob = QWidget(self)
        grabob.lineedit = widget
        grabob.setLayout(layout)
        return grabob

    def grab_object(self, edit, geom):
        """Grab object from tree to dialog."""
        self.object = self.treebase.grab_object(geom)
        edit.setText(self.object.name)
        self.load_object()

    def load_object(self):
        pass

    def create_browsedir(self, text, default=None, tip=None):
        """Create browse directory widget.

        :param text: key
        :type text: str
        :param default: default value
        :type default: str
        :param tip: tool tip
        :type tip: str
        :return: QWidget
        """
        widget = self.create_lineedit(text, default=default, tip=tip)
        edit = widget.edit
        browse_btn = QPushButton(ima.icon('DirOpenIcon'), '', self)
        browse_btn.setToolTip(_("Select directory"))
        browse_btn.clicked.connect(lambda: self.select_directory(edit))
        layout = QHBoxLayout()
        layout.addWidget(widget)
        layout.addWidget(browse_btn)
        layout.setContentsMargins(0, 0, 0, 0)
        browsedir = QWidget(self)
        browsedir.lineedit = widget
        browsedir.setLayout(layout)
        return browsedir

    def create_browsefile(self, text, default=None, tip=None,
                          filters=None, new=False):
        """Create browse file widget.

        :param text: key
        :type text: str
        :param default: default value
        :type default: str
        :param tip: tool tip
        :type tip: str
        :param filters: filters by filename extension
        :type filters: str
        :param new: select existing or create new file.
        :type new: bool
        :return: QWidget
        """
        widget = self.create_lineedit(text, default=default, tip=tip)
        edit = widget.edit
        browse_btn = QPushButton(ima.icon('FileIcon'), '', self)
        browse_btn.setToolTip(_("Select file"))
        browse_btn.clicked.connect(lambda: self.select_file(edit, filters, new))
        layout = QHBoxLayout()
        layout.addWidget(widget)
        layout.addWidget(browse_btn)
        layout.setContentsMargins(0, 0, 0, 0)
        browsefile = QWidget(self)
        browsefile.lineedit = widget
        browsefile.setLayout(layout)
        return browsefile

    def create_lineedit(self, text, default=None, tip=None,
                        alignment=Qt.Horizontal, regex=None, wrap=True):
        """Create line-edit widget.

        :param text: key
        :type text: str
        :param default: default value
        :type default: str
        :param tip: tool tip
        :type tip: str
        :param alignment: alignment, horizontal or vertical
        :type alignment: Qt
        :param regex: regular expression
        :type regex: str
        :param wrap: wrap text
        :type wrap: bool
        :return: QWidget
        """
        label = QLabel(text)
        label.setWordWrap(wrap)
        edit = QLineEdit()
        layout = QHBoxLayout() if alignment == Qt.Horizontal else QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(edit)
        layout.setContentsMargins(0, 0, 0, 0)
        if default:
            edit.setText(default)
        if tip:
            edit.setToolTip(tip)
        if regex:
            edit.setValidator(QRegExpValidator(QRegExp(regex)))
        widget = QWidget(self)
        widget.label = label
        widget.edit = edit
        widget.setLayout(layout)
        return widget

    def create_tab(self, *widgets):
        """Create simple tab widget page, widgets added in vertical layout.

        :return: QWidget
        """
        tab_widget = QWidget()
        layout = QVBoxLayout()
        for widget in widgets:
            layout.addWidget(widget)
        layout.addStretch(1)
        tab_widget.setLayout(layout)
        return tab_widget

    def select_file(self, edit, filters=None, new=False):
        """Select file.

        :param edit: box to display the selected file.
        :type edit: QLineEdit
        :param filters: filters by filename extension
        :type filters: str
        :param new: select existing or create new file.
        :type new: bool
        """
        initdir = to_text_string(edit.text())
        if osp.isdir(initdir):
            basedir = initdir
        else:
            basedir = osp.dirname(initdir)
            if not osp.isdir(basedir):
                basedir = getcwd_or_home()
        if filters is None:
            filters = _("All files (*)")
        title = _("Select file")
        if new:
            filename, _selfilter = getsavefilename(self, title, basedir, filters)
        else:
            filename, _selfilter = getopenfilename(self, title, basedir, filters)
        if filename:
            edit.setText(filename)
            self.load_lines()
        # Push default object name
        if self.object_name is not None:
            path, fn = osp.split(filename)
            object_name = osp.splitext(fn)[0]
            self.object_name.edit.setText(object_name)

    def select_directory(self, edit):
        """Select directory.

        :param edit: box to display the selected file.
        :type edit: QLineEdit
        """
        basedir = to_text_string(edit.text())
        if not osp.isdir(basedir):
            basedir = getcwd_or_home()
        title = _("Select directory")
        directory = getexistingdirectory(self, title, basedir)
        if directory:
            edit.setText(directory)
            self.load_lines()
        # Push default object name
        # if hasattr(self, 'object_name'): this is not enough because
        # after EasyDialog init, self.object_name is a built-in method.
        if self.object_name is not None:
            path, fn = osp.split(directory)
            object_name = osp.splitext(fn)[0]
            self.object_name.edit.setText(object_name)

    def apply(self):
        raise NotImplementedError

    def load_lines(self):
        pass


def main():
    from qtpy.QtWidgets import QApplication
    app = QApplication([])
    test = EasyDialog(test=True)
    test.show()
    app.exec_()


if __name__ == '__main__':
    main()
