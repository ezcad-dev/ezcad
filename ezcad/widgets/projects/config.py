# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
# -----------------------------------------------------------------------------
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# -----------------------------------------------------------------------------
"""Configuration options for projects"""

import os
from ezcad.config.user import UserConfig

# Project configuration defaults

WORKSPACE = 'workspace'
WORKSPACE_DEFAULTS = [
    (WORKSPACE,
        {'restore_data_on_startup': 'True',
         'save_data_on_exit': 'True',
         'save_history': 'True',
         'save_non_project_files': 'False',
         'project_working_directory': 'None',
        }
    )]
WORKSPACE_VERSION = '0.1.0'


EXTMODULES_DEFAULTS_DICT = {
    # 'languages/julia': 'False',
    # 'languages/java': 'False',
    # 'languages/cpp': 'False',
    # 'languages/fortran': 'False',
    'data_io/javaseis': 'False',
    'data_io/segy': 'False'}

EXTMODULES = 'extmodules'
EXTMODULES_DEFAULTS = [(EXTMODULES, EXTMODULES_DEFAULTS_DICT)]
EXTMODULES_VERSION = '0.1.0'


PROJECT_DEFAULTS = [
    ('workspace',
        {'project_working_directory': 'None'}),
    ('extmodules', EXTMODULES_DEFAULTS_DICT)]
PROJECT_VERSION = '0.1.0'


class ProjectConfig(UserConfig):
    """ProjectConfig class, based on UserConfig.

    Parameters
    ----------
    name: str
        name of the config
    defaults: tuple
        dictionnary containing options *or* list of tuples
        (section_name, options)
    version: str
        version of the configuration file (X.Y.Z format)
    filename: str
        configuration file will be saved in %home%/subfolder/%name%.ini
    """
    DEFAULT_SECTION_NAME = 'main'

    def __init__(self, name, root_path, filename, defaults=None, load=True,
                 version=None):
        # Config root path
        # self._root_path = os.path.join(root_path, PROJECT_FOLDER)
        self._root_path = root_path
        self._filename = filename

        # Create folder if non existent
        if not os.path.isdir(self._root_path):
            os.makedirs(self._root_path)

        # Add file
        # NOTE: We have to think better about the uses of this file
        # with open(os.path.join(root_path, PROJECT_FILENAME), 'w') as f:
        #    f.write('ezcad-ide project\n')

        UserConfig.__init__(self, name, defaults=defaults, load=load,
                            version=version, subfolder=None, backup=False,
                            raw_mode=True, remove_obsolete=True)
