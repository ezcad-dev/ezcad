# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License

"""
Ezcad font variables
"""

import os
import sys

from ezcad.config.utils import is_ubuntu


#==============================================================================
# Main fonts
#==============================================================================
# Rich text fonts
SANS_SERIF = ['Sans Serif', 'DejaVu Sans', 'Bitstream Vera Sans',
              'Bitstream Charter', 'Lucida Grande', 'MS Shell Dlg 2',
              'Calibri', 'Verdana', 'Geneva', 'Lucid', 'Arial',
              'Helvetica', 'Avant Garde', 'Times', 'sans-serif']

# Plan text fonts
MONOSPACE = ['Monospace', 'DejaVu Sans Mono', 'Consolas',
             'Bitstream Vera Sans Mono', 'Andale Mono', 'Liberation Mono',
             'Courier New', 'Courier', 'monospace', 'Fixed', 'Terminal']


#==============================================================================
# Adjust font size per OS
#==============================================================================
if sys.platform == 'darwin':
    MONOSPACE = ['Menlo'] + MONOSPACE
    BIG = MEDIUM = SMALL = 12
elif os.name == 'nt':
    BIG = MEDIUM = 10
    SMALL = 9
elif is_ubuntu():
    SANS_SERIF = ['Ubuntu'] + SANS_SERIF
    MONOSPACE = ['Ubuntu Mono'] + MONOSPACE
    BIG = MEDIUM = SMALL = 11
else:
    BIG = 10
    MEDIUM = SMALL = 9

DEFAULT_SMALL_DELTA = SMALL - MEDIUM
DEFAULT_LARGE_DELTA = SMALL - BIG
