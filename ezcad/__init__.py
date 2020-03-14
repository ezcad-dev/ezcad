# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

version_info = (0, 2, 2)

__version__ = '.'.join(map(str, version_info))
__license__ = __doc__
__project_url__ = 'http://ezcad.org'
# __forum_url__   = 'http://groups.google.com/group/ezcad'

# Dear (Debian, RPM, ...) package makers, please feel free to customize the
# following path to module's data (images) and translations:
DATAPATH = LOCALEPATH = DOCPATH = MATHJAXPATH = JQUERYPATH = ''


import os
# Directory of the current file
__dir__ = os.path.dirname(os.path.abspath(__file__))


def get_versions():
    """Get version information for components used by ezcad"""
    import sys
    import platform

    import qtpy.QtCore

    revision = None
    # from ezcad.utils import vcs
    # revision, branch = vcs.get_git_revision(os.path.dirname(__dir__))

    if not sys.platform == 'darwin':  # To avoid a crash with our Mac app
        system = platform.system()
    else:
        system = 'Darwin'

    return {
        'ezcad': __version__,
        'python': platform.python_version(),
        'bitness': 64 if sys.maxsize > 2**32 else 32,
        'qt': qtpy.QtCore.__version__,
        'qt_api': qtpy.API_NAME,      # PyQt5 or PyQt4
        'qt_api_ver': qtpy.PYQT_VERSION,
        'system': system,   # Linux, Windows, ...
        'revision': revision,  # '9fdf926eccce'
    }
