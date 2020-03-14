# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License

# Standard library imports
import os.path as osp

# Third party imports
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QStyle, QWidget

# Local imports
from ezcad.config.base import get_image_path, get_module_data_path
from ezcad.config.main import CONF
import qtawesome as qta

_resource = {
    # 'directory': osp.join(osp.dirname(osp.realpath(__file__)), '../fonts'),
    'directory': get_module_data_path('ezcad', relpath='fonts'),
    'loaded': False,
}

_qtaargs = {
    'bkgd_color':              [('fa.adjust',), {}],
    'cbar_editor':             [('fa5s.palette',), {'color': 'blue'}],
    'survey_info':             [('fa.slack',), {}],
    'section_player':          [('fa.sliders',), {}],
    'face_change':             [('fa.play-circle-o',), {}],
    'target_line':             [('fa.heart',), {}],
    'prop_operator':           [('fa.plus',), {}],
    'cam_operator':            [('fa.camera',), {}],
    'clear_text':              [('fa.square-o',), {}],
    'hide_all':                [('fa.square-o',), {}],
    'run_file':                [('fa.play-circle-o',), {}],
    'aspect_ratio':            [('fa.arrows',), {}],
    'log':                     [('fa.file-text-o',), {}],
    'configure':               [('fa.wrench',), {}],
    'app_config':              [('fa.wrench',), {}],
    'prj_config':              [('fa.gear',), {}],
    'view_all':                [('fa.eye',), {}],
    'view_none':               [('fa.eye-slash',), {}],
    'view_top':                [('fa.thumbs-o-down',), {}],
    'view_bottom':             [('fa.thumbs-o-up',), {}],
    'view_north':              [('fa.hand-o-down',), {}],
    'view_south':              [('fa.hand-o-up',), {}],
    'view_west':               [('fa.hand-o-right',), {}],
    'view_east':               [('fa.hand-o-left',), {}],
    'view_orthogonal':         [('ezcad.ortho',), {}],
    'view_perspective':        [('fa.dot-circle-o',), {}],
    'view_restrictive':        [('fa.scissors',), {}],
    'grab_object':             [('fa.hand-grab-o',), {}],
    'pick_mode':               [('fa.mouse-pointer',), {}],
    'gopoint':                 [('ezcad.point',), {}],
    'goline':                  [('ezcad.line',), {}],
    'gotsurf':                 [('ezcad.tsurf',), {}],
    'gogsurf':                 [('ezcad.gsurf',), {}],
    'gocube':                  [('ezcad.cube',), {}],
    # 'golabel':                 [('ezcad.label',), {}],
    'golabel':                 [('fa.tag',), {}],
    'photo':                   [('fa.photo',), {}],
    'download':                [('fa.download',), {}],
    'upload':                  [('fa.upload',), {}],
    'bold':                    [('fa.bold',), {}],
    'italic':                  [('fa.italic',), {}],
    'genprefs':                [('fa.cogs',), {}],
    'exit':                    [('fa.power-off',), {'color': 'darkred'}],
    'run_small':               [('fa.play',), {'color': 'green'}],
    'filenew':                 [('fa.file-o',), {}],
    'fileopen':                [('fa.folder-open',), {}],
    'syspath':                 [('fa.cogs',), {}],
    'tooloptions':             [('fa.cog',), {'color': '#333333'}],
    'edit':                    [('fa.edit',), {}],
    'filesave':                [('fa.save',), {}],
    'filesaveas':              [('fa.save', 'fa.pencil'), {'options': [{'offset': (-0.2, -0.2), 'scale_factor': 0.6}, {'offset': (0.2, 0.2), 'scale_factor': 0.6}]}],
    'run':                     [('fa.play',), {'color': 'green'}],
    'todo_list':               [('fa.th-list', 'fa.check'), {'options': [{'color': '#999999'}, {'offset': (0.0, 0.2), 'color': '#3775a9', 'color_disabled': '#748fa6'}]}],
    'warning':                 [('fa.warning',), {'color': 'orange'}],
    'todo':                    [('fa.check',), {'color': '#3775a9'}],
    'python':                  [('spyder.python-logo-up', 'spyder.python-logo-down'), {'options': [{'color': '#3775a9'}, {'color': '#ffd444'}]}],
    'help':                    [('fa.question-circle',), {}],
    'outline_explorer':        [('spyder.treeview',), {}],
    'dictedit':                [('fa.th-list',), {}],
    'previous':                [('fa.arrow-left',), {}],
    'next':                    [('fa.arrow-right',), {}],
    'up':                      [('fa.arrow-up',), {}],
    'restart':                 [('fa.repeat',), {'çolor': '#3775a9'}],
    'editcopy':                [('fa.copy',), {}],
    'editcut':                 [('fa.scissors',), {}],
    'editpaste':               [('fa.clipboard',), {}],
    'editdelete':              [('fa.eraser',), {}],
    'editclear':               [('fa.times',), {}],
    'selectall':               [('spyder.text-select-all',), {}],
    'advanced':                [('fa.gear',), {}],
    'bug':                     [('fa.bug',), {}],
    'maximize':                [('spyder.maximize-pane',), {}],
    'unmaximize':              [('spyder.minimize-pane',), {}],
    'window_nofullscreen':     [('spyder.inward',), {}],
    'window_fullscreen':       [('fa.arrows-alt',), {}],
    'MessageBoxWarning':       [('fa.warning',), {}],
    'arredit':                 [('fa.table',), {}],
    'plot':                    [('fa.line-chart',), {}],
    'hist':                    [('fa.bar-chart',), {}],
    'imshow':                  [('fa.image',), {}],
    'insert':                  [('fa.sign-in',), {}],
    'rename':                  [('fa.pencil',), {}],
    'edit_add':                [('fa.plus',), {}],
    'edit_remove':             [('fa.minus',), {}],
    'newwindow':               [('spyder.window',), {}],
    'fromcursor':              [('fa.hand-o-right',), {}],
    'filter':                  [('fa.filter',), {}],
    'folder_new':              [('fa.folder-o', 'fa.plus'), {'options': [{}, {'scale_factor': 0.5, 'offset': (0.0, 0.1)}]}],
    'package_new':             [('fa.folder-o', 'spyder.python-logo'), {'options': [{'offset': (0.0, -0.125)}, {'offset': (0.0, 0.125)}]}],
    'fileimport':              [('fa.download',), {}],
    'environ':                 [('fa.th-list',), {}],
    'ArrowDown':               [('fa.arrow-circle-down',), {}],
    'ArrowUp':                 [('fa.arrow-circle-up',), {}],
    'ArrowBack':               [('fa.arrow-circle-left',), {}],
    'ArrowForward':            [('fa.arrow-circle-right',), {}],
    'DialogApplyButton':       [('fa.check',), {}],
    'DialogCloseButton':       [('fa.close',), {}],
    'DialogHelpButton':        [('fa.life-ring',), {'color': 'darkred'}],
    'MessageBoxInformation':   [('fa.info',), {'color': '3775a9'}],
    'DataInformation':         [('fa.info-circle',), {}],
    'DirOpenIcon':             [('fa.folder-open',), {}],
    'FileIcon':                [('fa.file-o',), {}],
    'ExcelFileIcon':           [('fa.file-excel-o',), {}],
    'WordFileIcon':            [('fa.file-word-o',), {}],
    'PowerpointFileIcon':      [('fa.file-powerpoint-o',), {}],
    'PDFIcon':                 [('fa.file-pdf-o',), {}],
    'AudioFileIcon':           [('fa.file-audio-o',), {}],
    'ImageFileIcon':           [('fa.file-image-o',), {}],
    'ArchiveFileIcon':         [('fa.file-archive-o',), {}],
    'VideoFileIcon':           [('fa.file-video-o',), {}],
    'TextFileIcon':            [('fa.file-text-o',), {}],
    'copywop':                 [('fa.terminal',), {}],
    'no_match':                [('fa.circle',), {'color': 'gray'}],
}


def get_std_icon(name, size=None):
    """Get standard platform icon
    Call 'show_std_icons()' for details"""
    if not name.startswith('SP_'):
        name = 'SP_' + name
    icon = QWidget().style().standardIcon(getattr(QStyle, name))
    if size is None:
        return icon
    else:
        return QIcon(icon.pixmap(size, size))


def get_icon(name, default=None, resample=False):
    """Return image inside a QIcon object.

    default: default image name or icon
    resample: if True, manually resample icon pixmaps for usual sizes
    (16, 24, 32, 48, 96, 128, 256). This is recommended for QMainWindow icons
    created from SVG images on non-Windows platforms due to a Qt bug (see
    Issue 1314).
    """

    icon_path = get_image_path(name, default=None)
    if icon_path is not None:
        icon = QIcon(icon_path)
    elif isinstance(default, QIcon):
        icon = default
    elif default is None:
        try:
            icon = get_std_icon(name[:-4])
        except AttributeError:
            icon = QIcon(get_image_path(name, default))
    else:
        icon = QIcon(get_image_path(name, default))
    if resample:
        icon0 = QIcon()
        for size in (16, 24, 32, 48, 96, 128, 256, 512):
            icon0.addPixmap(icon.pixmap(size, size))
        return icon0
    else:
        return icon


def icon(name, resample=False, icon_path=None):
    theme = CONF.get('main', 'icon_theme')
    if theme == 'ezcad 3':
        if not _resource['loaded']:
            print('Loading iconic fonts...')
            qta.load_font('spyder', 'spyder.ttf', 'spyder-charmap.json',
                          directory=_resource['directory'])
            qta.load_font('ezcad', 'ezcad.ttf', 'ezcad-charmap.json',
                          directory=_resource['directory'])
            _resource['loaded'] = True
        args, kwargs = _qtaargs[name]
        return qta.icon(*args, **kwargs)
    elif theme == 'ezcad 2':
        icon = get_icon(name + '.png', resample=resample)
        if icon_path:
            icon_path = osp.join(icon_path, name + '.png')
            if osp.isfile(icon_path):
                icon = QIcon(icon_path)
        return icon if icon is not None else QIcon()
    else:
        raise ValueError("Unknown icon theme.")
