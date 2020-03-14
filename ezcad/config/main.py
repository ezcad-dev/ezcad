# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License

"""
EZCAD configuration options

Note: Leave this file free of Qt related imports, so that it can be used to
quickly load a user config file
"""

import os
import sys

# Local import
from ezcad.config.base import SUBFOLDER, TEST
from ezcad.config.fonts import BIG, MEDIUM, MONOSPACE, SANS_SERIF
from ezcad.config.user import UserConfig


# ==============================================================================
# Main constants
# ==============================================================================
# Port used to detect if there is a running instance and to communicate with
# it to open external files
OPEN_FILES_PORT = 21128

# OS Specific
WIN = os.name == 'nt'
MAC = sys.platform == 'darwin'
CTRL = "Meta" if MAC else "Ctrl"

# Run cell shortcuts
if sys.platform == 'darwin':
    RUN_CELL_SHORTCUT = 'Meta+Return'
else:
    RUN_CELL_SHORTCUT = 'Ctrl+Return'
RE_RUN_LAST_CELL_SHORTCUT = 'Alt+Return'
RUN_CELL_AND_ADVANCE_SHORTCUT = 'Shift+Return'


# =============================================================================
#  Defaults
# =============================================================================
DEFAULTS_APP = [
    ('main',
        {
            'icon_theme': 'ezcad 3',
            'single_instance': True,
            'open_files_port': OPEN_FILES_PORT,
            'tear_off_menus': False,
            'normal_screen_resolution': True,
            'high_dpi_scaling': False,
            'high_dpi_custom_scale_factor': False,
            'high_dpi_custom_scale_factors': '1.5',
            'vertical_dockwidget_titlebars': False,
            'vertical_tabs': False,
            'animated_docks': True,
            'prompt_on_exit': True,
            'panes_locked': True,
            'window/size': (1260, 740),
            'window/position': (10, 10),
            'window/is_maximized': False,
            'window/is_fullscreen': False,
            'window/prefs_dialog_size': (745, 411),
            'show_status_bar': True,
            'use_custom_margin': True,
            'custom_margin': 0,
            'use_custom_cursor_blinking': False,
            'show_internal_console_if_traceback': False,
            'check_updates_on_startup': True,
            'toolbars_visible': True,
            # Global EZCAD fonts
            'font/family': MONOSPACE,
            'font/size': MEDIUM,
            'font/italic': False,
            'font/bold': False,
            'rich_font/family': SANS_SERIF,
            'rich_font/size': BIG,
            'rich_font/italic': False,
            'rich_font/bold': False,
            'cursor/width': 2,
            'completion/size': (300, 180),
        }),
    ('quick_layouts',
        {
            'place_holder': '',
            'names': ['Petrel layout', 'Gocad layout', 'Vertical split', 'Horizontal split'],
            'order': ['Petrel layout', 'Gocad layout', 'Vertical split', 'Horizontal split'],
            'active': ['Petrel layout', 'Gocad layout', 'Vertical split', 'Horizontal split'],
        }),
    ('image_viewer',
        {
            'padding_left_width':   (5, 10), # (min, max)
            'padding_right_width':  (5, 10),
            'padding_bottom_height': (5, 10),
            'cbar_top_height':      (0, 1),
            'cbar_bottom_height':   (0, 1),
            'cbar_left_width':      (0, 1),
            'cbar_right_width':     (0, 1),
            'title_widget_height':  (10, 20),
            'xlabel_widget_height': (40, 50),
            'ylabel_widget_width':  (60, 70),
            'xaxis_widget_height':  (20, 40),
            'yaxis_widget_width':   (20, 40),
        }),
    ('process_log',
        {
            'enable': True,
        }),
    ('data_explorer',
        {
            'enable': True,
        }),
    ('project_console',
        {
            'enable': True,
        }),
    ('historylog',
        {
            'enable': True,
            'max_entries': 100,
            'wrap': True,
            'go_to_eof': True,
            'line_numbers': False,
        }),
    ('plotter',
        {
            'enable': True,
        }),
    ('viewer',
        {
            'enable': True,
        }),
    ('shortcuts',
        {
            # ---- Global ----
            # -- In app/ezcad.py
            '_/close pane': "Shift+Ctrl+F4",
            '_/lock unlock panes': "Shift+Ctrl+F5",
            '_/use next layout': "Shift+Alt+PgDown",
            '_/use previous layout': "Shift+Alt+PgUp",
            '_/preferences': "Ctrl+Alt+Shift+P",
            '_/maximize pane': "Ctrl+Alt+Shift+M",
            '_/fullscreen mode': "F11",
            '_/save current layout': "Shift+Alt+S",
            '_/layout preferences': "Shift+Alt+P",
            '_/show toolbars': "Alt+Shift+T",
            '_/ezcad documentation': "F1",
            '_/restart': "Shift+Alt+R",
            '_/quit': "Ctrl+Q",
            '_/application preferences': "Ctrl+Shift+A",
            '_/project preferences': "Ctrl+Shift+P",
            # ---- EZCAD widget ----
            '_/open project': "Ctrl+O",
            '_/new project': "Ctrl+N",
            '_/save project': "Ctrl+S",
            '_/save project as': "Ctrl+Shift+S",
        })
]

# ==============================================================================
# Config instance
# ==============================================================================
# IMPORTANT NOTES:
# 1. If you want to *change* the default value of a current option, you need to
#    do a MINOR update in config version, e.g. from 3.0.0 to 3.1.0
# 2. If you want to *remove* options that are no longer needed in our codebase,
#    or if you want to *rename* options, then you need to do a MAJOR update in
#    version, e.g. from 3.0.0 to 4.0.0
# 3. You don't need to touch this value if you're just adding a new option
CONF_VERSION = '41.0.0'

# Main configuration instance
try:
    CONF = UserConfig('ezcad', defaults=DEFAULTS_APP, load=(not TEST),
                      version=CONF_VERSION, subfolder=SUBFOLDER, backup=True,
                      raw_mode=True)
except:
    CONF = UserConfig('ezcad', defaults=DEFAULTS_APP, load=False,
                      version=CONF_VERSION, subfolder=SUBFOLDER, backup=True,
                      raw_mode=True)
