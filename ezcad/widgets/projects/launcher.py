# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

"""
Dialogs before launch project
"""

import os
from qtpy.QtCore import Qt, Signal
from qtpy.QtWidgets import (QLabel, QPushButton, QRadioButton, QGroupBox,
                            QVBoxLayout, QHBoxLayout)

from ezcad.config.base import _
from ezcad.widgets.ezdialog import EasyDialog


class ProjectLauncher(EasyDialog):
    NAME = _("Select project")
    sigOpenProject = Signal(bool, str)

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent)
        self.setup_page()

    def setup_page(self):
        lbl_select = QLabel(_('Select method:'))
        self.rb_new = QRadioButton(_('Create a new project'))
        self.rb_old = QRadioButton(_('Open an existing project'))

        hbox = QHBoxLayout()
        hbox.addWidget(self.rb_new)
        hbox.addWidget(self.rb_old)

        self.layout.addWidget(lbl_select)
        self.layout.addLayout(hbox)

        self.new_group = QGroupBox(_("New project"))
        self.new_project_name = self.create_lineedit("Project name",
            alignment=Qt.Horizontal)
        self.new_project_name.edit.setText(_("test"))
        self.new_project_path = self.create_browsedir("Project path")
        self.new_project_path.lineedit.edit.setText(os.getcwd())
        new_layout = QVBoxLayout()
        new_layout.addWidget(self.new_project_name)
        new_layout.addWidget(self.new_project_path)
        self.new_group.setLayout(new_layout)

        self.old_group = QGroupBox(_("Existing project"))
        self.old_project_name = self.create_browsefile("Project name",
            filters="EZD files (*.ezd);;All Files (*)")
        text = os.path.join(os.getcwd(), 'fake.ezd')
        self.old_project_name.lineedit.edit.setText(text)
        old_layout = QVBoxLayout()
        old_layout.addWidget(self.old_project_name)
        self.old_group.setLayout(old_layout)

        btnApply = QPushButton(_('Next'))
        btnApply.clicked.connect(self.apply)
        btnClose = QPushButton(_('Exit'))
        btnClose.clicked.connect(self.stop)
        hbox = QHBoxLayout()
        hbox.addWidget(btnApply)
        hbox.addWidget(btnClose)

        self.layout.addWidget(self.new_group)
        self.layout.addWidget(self.old_group)
        self.layout.addLayout(hbox)

        self.rb_new.toggled.connect(self.toggle)
        self.rb_old.toggled.connect(self.toggle)
        self.rb_old.setChecked(True)

    def toggle(self):
        if self.rb_new.isChecked():
            self.new_group.setEnabled(True)
            self.old_group.setEnabled(False)
        elif self.rb_old.isChecked():
            self.new_group.setEnabled(False)
            self.old_group.setEnabled(True)
        else:
            raise ValueError("Unknown value")

    def apply(self):
        if self.rb_new.isChecked():
            new = True
            name = self.new_project_name.edit.text()
            path = self.new_project_path.lineedit.edit.text()
            afn = os.path.join(path, name)
        elif self.rb_old.isChecked():
            new = False
            afn = self.old_project_name.lineedit.edit.text()
        else:
            raise ValueError("Unknown value")
        self.sigOpenProject.emit(new, afn)
        self.close()

    def stop(self):
        self.close()
        if self.parent is not None:
            self.parent.force_exit()


def main():
    from qtpy.QtWidgets import QApplication
    app = QApplication([])
    test = ProjectLauncher()
    test.show()
    app.exec_()


if __name__ == '__main__':
    main()
