# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License

"""
Ezcad GUI-related configuration management
(for non-GUI configuration, see ezcad/config/base.py)

Important note regarding shortcuts:
    For compatibility with QWERTZ keyboards, one must avoid using the following
    shortcuts:
        Ctrl + Alt + Q, W, F, G, Y, X, C, V, B, N
"""

# Standard library imports
try:
    from collections.abc import namedtuple
except ImportError:
    from collections import namedtuple

# Third party imports
from qtpy.QtCore import Qt
from qtpy.QtGui import QFont, QFontDatabase, QKeySequence
from qtpy.QtWidgets import QShortcut

# Local imports
from ezcad.config.main import CONF
from ezcad.utils.functions import to_text_string


# To save metadata about widget shortcuts (needed to build our
# preferences page)
Shortcut = namedtuple('Shortcut', 'data')


def font_is_installed(font):
    """Check if font is installed"""
    return [fam for fam in QFontDatabase().families()
            if to_text_string(fam) == font]


def get_family(families):
    """Return the first installed font family in family list"""
    if not isinstance(families, list):
        families = [families]
    for family in families:
        if font_is_installed(family):
            return family
    else:
        print("Warning: None of the following fonts is installed: %r" % families)  # ezcad: test-skip
        return QFont().family()


FONT_CACHE = {}


def get_font(section='main', option='font', font_size_delta=0):
    """Get console font properties depending on OS and user options"""
    font = FONT_CACHE.get((section, option))

    if font is None:
        families = CONF.get(section, option+"/family", None)

        if families is None:
            return QFont()

        family = get_family(families)
        weight = QFont.Normal
        italic = CONF.get(section, option+'/italic', False)

        if CONF.get(section, option+'/bold', False):
            weight = QFont.Bold

        size = CONF.get(section, option+'/size', 9) + font_size_delta
        font = QFont(family, size, weight)
        font.setItalic(italic)
        FONT_CACHE[(section, option)] = font

    size = CONF.get(section, option+'/size', 9) + font_size_delta
    font.setPointSize(size)
    return font


def set_font(font, section='main', option='font'):
    """Set font"""
    CONF.set(section, option+'/family', to_text_string(font.family()))
    CONF.set(section, option+'/size', float(font.pointSize()))
    CONF.set(section, option+'/italic', int(font.italic()))
    CONF.set(section, option+'/bold', int(font.bold()))
    FONT_CACHE[(section, option)] = font


def get_shortcut(context, name):
    """Get keyboard shortcut (key sequence string)"""
    return CONF.get('shortcuts', '%s/%s' % (context, name))


def set_shortcut(context, name, keystr):
    """Set keyboard shortcut (key sequence string)"""
    CONF.set('shortcuts', '%s/%s' % (context, name), keystr)


def fixed_shortcut(keystr, parent, action):
    """
    DEPRECATED: This function will be removed in Ezcad 4.0

    Define a fixed shortcut according to a keysequence string
    """
    sc = QShortcut(QKeySequence(keystr), parent, action)
    sc.setContext(Qt.WidgetWithChildrenShortcut)
    return sc


def config_shortcut(action, context, name, parent):
    """
    Create a Shortcut namedtuple for a widget

    The data contained in this tuple will be registered in
    our shortcuts preferences page
    """
    keystr = get_shortcut(context, name)
    qsc = QShortcut(QKeySequence(keystr), parent, action)
    qsc.setContext(Qt.WidgetWithChildrenShortcut)
    sc = Shortcut(data=(qsc, context, name))
    return sc


def iter_shortcuts():
    """Iterate over keyboard shortcuts"""
    for option in CONF.options('shortcuts'):
        context, name = option.split("/", 1)
        yield context, name, get_shortcut(context, name)


def reset_shortcuts():
    """Reset keyboard shortcuts to default values"""
    CONF.reset_to_defaults(section='shortcuts')
