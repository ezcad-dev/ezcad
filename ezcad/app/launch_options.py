# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

import argparse


def get_options(argv=None):
    """
    Convert options into commands
    return commands, message
    """
    parser = argparse.ArgumentParser(usage="ezcad [options]")
    parser.add_argument('--new-instance', action='store_true',
        default=False, help="Run a new instance of Ezcad, even if "
        "the single instance mode has been turned on (default)")
    parser.add_argument('--defaults', dest="reset_to_defaults",
        action='store_true', default=False,
        help="Reset configuration settings to defaults")
    parser.add_argument('--reset', dest="reset_config_files",
        action='store_true', default=False,
        help="Remove all configuration files!")
    parser.add_argument('--debug', action='store_true', default=False,
        help="In debug mode, print standard output to system "
        "default, otherwise print to the app log window.")
    parser.add_argument('--env', dest="dot_env_file",
        default=None, help="The environment .env file")
    parser.add_argument('-w', '--workdir', dest="working_directory",
        default=None, help="Default working directory")
    parser.add_argument('--plugins', dest="plugins_paths", default=None,
        help="Default plugins paths")
    parser.add_argument('-p', '--project', dest="project_file",
        default=None, type=str, help="Path to a EZCAD project file")
    options = parser.parse_args(argv)
    return options
