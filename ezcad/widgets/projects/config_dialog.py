# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
"""
Configuration dialog for project.
"""

import os.path as osp
from qtpy.QtWidgets import QGroupBox, QVBoxLayout, QTabWidget, QMessageBox
from ezcad.config.base import _
from ezcad.config.user import NoDefault
from ezcad.utils import icon_manager as ima
from ezcad.widgets.dialogs import ConfigDialog
from ezcad.dialogs.app_config import GeneralConfigPage


class ProjectPreferences(ConfigDialog):
    """ """
    def __init__(self, parent, project):
        super(ProjectPreferences, self).__init__()

        self._main = parent
        self._project = project
        self._project_preferences = [WorkspaceConfigPage]

        self.setWindowTitle(_("Project preferences"))
        self.setWindowIcon(ima.icon('configure'))

        self.setup_dialog()

    def setup_dialog(self):
        """ """
        # Move to ezcad.py
#        dlg = ConfigDialog(self)
#        dlg.size_change.connect(self.set_prefs_size)
#        if self.prefs_dialog_size is not None:
#            dlg.resize(self.prefs_dialog_size)
        for PrefPageClass in self._project_preferences:
            page = PrefPageClass(self, self._main, self._project)
            page.initialize()
            self.add_page(page)


class ProjectConfigPage(GeneralConfigPage):
    """General config page that redefines the configuration accessors."""
    CONF_SECTION = None
    NAME = None
    ICON = None

    def __init__(self, parent, main, project):
        self._project = project
#        self._conf_files = project.get_conf_files()
#        self._conf = self._conf_files[self.CONF_SECTION]
        self._conf = project.CONF

        GeneralConfigPage.__init__(self, parent, main)

    def set_option(self, option, value):
        """ """
        CONF = self._conf
        CONF.set(self.CONF_SECTION, option, value)

    def get_option(self, option, default=NoDefault):
        """" """
        CONF = self._conf
        return CONF.get(self.CONF_SECTION, option, default)


class WorkspaceConfigPage(ProjectConfigPage):
    CONF_SECTION = "workspace"
    NAME = _("General")
    ICON = ima.icon('genprefs')

    def setup_page(self):
        # --- Interface
        general_group = QGroupBox(_("TODO"))

        # --- Status bar
        sbar_group = QGroupBox(_("TODO"))

        # --- Path
        self.set_workdir = self.create_browsedir("Project working directory",
                                'project_working_directory')

        path_group = QGroupBox(_("Path"))
        path_layout = QVBoxLayout()
        path_layout.addWidget(self.set_workdir)
        path_group.setLayout(path_layout)

        tabs = QTabWidget()
        tabs.addTab(self.create_tab(path_group), _("Basic"))
        tabs.addTab(self.create_tab(general_group, sbar_group),
                    _("Advanced Settings"))

        vlayout = QVBoxLayout()
        vlayout.addWidget(tabs)
        self.setLayout(vlayout)

    def apply_settings(self, options):
        """
        Click apply button in configDialog, calls configPage.apply_changes,
        which saves the changes and calls configPage.apply_settings.
        """
        workdir = self.set_workdir.lineedit.textbox.text()
        if not osp.isdir(workdir):
            QMessageBox.critical(self, _('Error'),
                'The project work directory does not exist. Please reset.')

        # TODO Even with this check, the non-existing dir still gets saved
        # into the config file, e.g. /home/joe/.config/ezcad-py3/ezcad.ini
        # Cannot move save_conf behind configPage.apply_settings,
        # because the latter calls main.apply_settings which read the saved
        # conf to take proper actions, so must save before apply...

        # fname = self.set_sgmtfn.lineedit.textbox.text()
        # if not osp.isfile(fname):
        #     QMessageBox.critical(self, _('Error'),
        #         'The survey geometry file does not exist. Please reset.')

        self.main.apply_project_settings()


def main():
    import os.path as osp
    import tempfile
    from ezcad.utils.qthelpers import qapplication
    from ezcad.widgets.projects import EmptyProject
    app = qapplication()
    proj_dir = tempfile.mkdtemp() + osp.sep + '.zpyproject'
    print('The temporary proejct directory is', proj_dir)
    proj = EmptyProject(proj_dir)
    dlg = ProjectPreferences(None, proj)
    dlg.show()
    app.exec_()


if __name__ == "__main__":
    main()
