# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

import os
from qtpy.QtCore import Signal
from qtpy.QtWidgets import QGroupBox, QVBoxLayout, QTabWidget, QMessageBox
from ezcad.config.base import _
from ezcad.widgets.ezdialog import EasyDialog


class ProjectConfig(EasyDialog):
    NAME = _("Project settings")
    sigWorkDirChanged = Signal(str)

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent)
        self.setup_page()

    def setup_page(self):
        text = _("Working directory")
        default = os.getcwd()
        self.setdir = self.create_browsedir(text, default=default)

        gpPath = QGroupBox(_("Path"))
        pathLayout = QVBoxLayout()
        pathLayout.addWidget(self.setdir)
        gpPath.setLayout(pathLayout)

        gpGeneral = QGroupBox(_("TODO"))
        gpStatus = QGroupBox(_("TODO"))

        tabs = QTabWidget()
        tabs.addTab(self.create_tab(gpPath), _("Basic"))
        tabs.addTab(self.create_tab(gpGeneral, gpStatus),
                    _("Advanced Settings"))
        self.layout.addWidget(tabs)

        action = self.create_action()
        self.layout.addWidget(action)

    def load_state(self, workdir=None):
        if workdir is not None:
            self.workdirOld = workdir
            self.setdir.lineedit.edit.setText(workdir)

    def apply(self):
        workdir = self.setdir.lineedit.edit.text()
        if not os.path.isdir(workdir):
            QMessageBox.critical(self, _('Error'),
                'The working directory does not exist. Please reset.')
        else:
            if workdir != self.workdirOld:
                self.sigWorkDirChanged.emit(workdir)


def main():
    from qtpy.QtWidgets import QApplication
    app = QApplication([])
    test = ProjectConfig()
    test.show()
    app.exec_()


if __name__ == '__main__':
    main()
