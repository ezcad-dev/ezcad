# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License

import os
import os.path as osp

from ezcad.config.base import _
from ezcad.utils.functions import to_text_string
from ezcad.widgets.projects.config import (ProjectConfig,
        PROJECT_DEFAULTS, PROJECT_VERSION)


class BaseProject(object):
    """Ezcad base project.

    This base class must not be used directly, but inherited from. It does not
    assume that python is specific to this project.
    """
    PROJECT_TYPE_NAME = None

    def __init__(self, root_path):
        self.name = None
        self.root_path = root_path # caller supply project folder
        self.open_project_files = []
        self.open_non_project_files = []
        self.config_files = []
        # self.CONF = {}
        self.CONF = None

        # Configuration files

        self.related_projects = []  # storing project path, not project objects
        # self.pythonpath = []
        self.opened = True

        self.ioerror_flag = False
        self.create_project_config_files()

    def create_project_config_files(self):
        name = 'project'
        filename = 'project.ini'
        defaults = PROJECT_DEFAULTS
        version = PROJECT_VERSION
        self.CONF = ProjectConfig(name, self.root_path, filename,
                defaults=defaults, load=True, version=version)

    def get_conf_files(self):
        return self.CONF

    def set_root_path(self, root_path):
        """Set project root path."""
        if self.name is None:
            self.name = osp.basename(root_path)
        self.root_path = to_text_string(root_path)
        config_path = self.__get_project_config_path()
        if osp.exists(config_path):
            self.load()
        else:
            if not osp.isdir(self.root_path):
                os.mkdir(self.root_path)
            self.save()

    def rename(self, new_name):
        """Rename project and rename its root path accordingly."""
        old_name = self.name
        self.name = new_name
        pypath = self.relative_pythonpath  # ??
        self.root_path = self.root_path[:-len(old_name)]+new_name
        self.relative_pythonpath = pypath  # ??
        self.save()

    def __get_project_config_folder(self):
        """Return project configuration folder."""
#        return osp.join(self.root_path, self.PROJECT_FOLDER)
        return self.root_path

    def __get_project_config_path(self):
        """Return project configuration path"""
        return osp.join(self.root_path, self.CONFIG_NAME)


class EmptyProject(BaseProject):
    """Empty Project"""
    PROJECT_TYPE_NAME = _('Empty project')
