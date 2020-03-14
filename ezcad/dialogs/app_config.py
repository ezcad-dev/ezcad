# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License

"""
Configuration dialog / Preferences.
"""

# Standard library imports
import os.path as osp

# Third party imports
from qtpy import API
from qtpy.compat import (getexistingdirectory, getopenfilename, from_qvariant,
                         to_qvariant)
from qtpy.QtCore import Qt, Signal, Slot, QRegExp
from qtpy.QtGui import QRegExpValidator
from qtpy.QtWidgets import (QButtonGroup, QCheckBox, QComboBox, QLineEdit,
                            QDoubleSpinBox, QFontComboBox, QSpinBox,
                            QGridLayout, QGroupBox, QHBoxLayout, QLabel,
                            QMessageBox, QPushButton, QRadioButton,
                            QTabWidget, QVBoxLayout, QWidget)

# Local imports
from ezcad.config.base import _, LANGUAGE_CODES, save_lang_conf, getcwd_or_home
from ezcad.config.gui import get_font, set_font
from ezcad.config.main import CONF as CONF_APP
from ezcad.config.user import NoDefault
from ezcad.utils import icon_manager as ima
from ezcad.utils.functions import to_text_string


class ConfigAccessMixin(object):
    """Namespace for methods that access config storage"""
    CONF = None
    CONF_SECTION = None

    def set_option(self, option, value):
        self.CONF.set(self.CONF_SECTION, option, value)

    def get_option(self, option, default=NoDefault):
        return self.CONF.get(self.CONF_SECTION, option, default)


class ConfigPage(QWidget):
    """Base class for configuration page in Preferences"""

    # Signals
    apply_button_enabled = Signal(bool)
    show_this_page = Signal()

    def __init__(self, parent, apply_callback=None):
        QWidget.__init__(self, parent)
        self.apply_callback = apply_callback
        self.is_modified = False

    def initialize(self):
        """
        Initialize configuration page:
            * setup GUI widgets
            * load settings and change widgets accordingly
        """
        self.setup_page()
        self.load_from_conf()

    def get_name(self):
        """Return configuration page name"""
        raise NotImplementedError

    def get_icon(self):
        """Return configuration page icon (24x24)"""
        raise NotImplementedError

    def setup_page(self):
        """Setup configuration page widget"""
        raise NotImplementedError

    def set_modified(self, state):
        self.is_modified = state
        self.apply_button_enabled.emit(state)

    def is_valid(self):
        """Return True if all widget contents are valid"""
        raise NotImplementedError

    def apply_changes(self):
        """Apply changes callback"""
        if self.is_modified:
            self.save_to_conf()
            if self.apply_callback is not None:
                self.apply_callback()

            # Since the language cannot be retrieved by CONF and the language
            # is needed before loading CONF, this is an extra method needed to
            # ensure that when changes are applied, they are copied to a
            # specific file storing the language value. This only applies to
            # the main section config.
            if self.CONF_SECTION == u'main':
                self._save_lang()

            for restart_option in self.restart_options:
                if restart_option in self.changed_options:
                    self.prompt_restart_required()
                    break  # Ensure a single popup is displayed
            self.set_modified(False)

    def load_from_conf(self):
        """Load settings from configuration file"""
        raise NotImplementedError

    def save_to_conf(self):
        """Save settings to configuration file"""
        raise NotImplementedError


class EzcadConfigPage(ConfigPage, ConfigAccessMixin):
    """Plugin configuration dialog box page widget"""
    CONF_SECTION = None

    def __init__(self, parent):
        ConfigPage.__init__(self, parent,
                            apply_callback=lambda:
                            self.apply_settings(self.changed_options))
        self.checkboxes = {}
        self.radiobuttons = {}
        self.lineedits = {}
        self.validate_data = {}
        self.spinboxes = {}
        self.comboboxes = {}
        self.fontboxes = {}
        self.coloredits = {}
        self.scedits = {}
        self.changed_options = set()
        self.restart_options = dict()  # Dict to store name and localized text
        self.default_button_group = None

    def apply_settings(self, options):
        raise NotImplementedError

    def check_settings(self):
        """This method is called to check settings after configuration
        dialog has been shown"""
        pass

    def set_modified(self, state):
        ConfigPage.set_modified(self, state)
        if not state:
            self.changed_options = set()

    def is_valid(self):
        """Return True if all widget contents are valid"""
        for lineedit in self.lineedits:
            if lineedit in self.validate_data and lineedit.isEnabled():
                validator, invalid_msg = self.validate_data[lineedit]
                text = to_text_string(lineedit.text())
                if not validator(text):
                    QMessageBox.critical(self, self.get_name(),
                                     "%s:<br><b>%s</b>" % (invalid_msg, text),
                                     QMessageBox.Ok)
                    return False
        return True

    def load_from_conf(self):
        """Load settings from configuration file"""
        for checkbox, (option, default) in list(self.checkboxes.items()):
            checkbox.setChecked(self.get_option(option, default))
            # QAbstractButton works differently for PySide and PyQt
            if not API == 'pyside':
                checkbox.clicked.connect(lambda _foo, opt=option:
                                         self.has_been_modified(opt))
            else:
                checkbox.clicked.connect(lambda opt=option:
                                         self.has_been_modified(opt))
        for radiobutton, (option, default) in list(self.radiobuttons.items()):
            radiobutton.setChecked(self.get_option(option, default))
            radiobutton.toggled.connect(lambda _foo, opt=option:
                                        self.has_been_modified(opt))
            if radiobutton.restart_required:
                self.restart_options[option] = radiobutton.label_text
        for lineedit, (option, default) in list(self.lineedits.items()):
            lineedit.setText(self.get_option(option, default))
            lineedit.textChanged.connect(lambda _foo, opt=option:
                                         self.has_been_modified(opt))
            if lineedit.restart_required:
                self.restart_options[option] = lineedit.label_text
        for spinbox, (option, default) in list(self.spinboxes.items()):
            spinbox.setValue(self.get_option(option, default))
            spinbox.valueChanged.connect(lambda _foo, opt=option:
                                         self.has_been_modified(opt))
        for combobox, (option, default) in list(self.comboboxes.items()):
            value = self.get_option(option, default)
            for index in range(combobox.count()):
                data = from_qvariant(combobox.itemData(index), to_text_string)
                # For PyQt API v2, it is necessary to convert `data` to
                # unicode in case the original type was not a string, like an
                # integer for example (see qtpy.compat.from_qvariant):
                if to_text_string(data) == to_text_string(value):
                    break
            combobox.setCurrentIndex(index)
            combobox.currentIndexChanged.connect(lambda _foo, opt=option:
                                                 self.has_been_modified(opt))
            if combobox.restart_required:
                self.restart_options[option] = combobox.label_text

        for (fontbox, sizebox), option in list(self.fontboxes.items()):
            font = self.get_font(option)
            fontbox.setCurrentFont(font)
            sizebox.setValue(font.pointSize())
            if option is None:
                property = 'plugin_font'
            else:
                property = option
            fontbox.currentIndexChanged.connect(lambda _foo, opt=property:
                                                self.has_been_modified(opt))
            sizebox.valueChanged.connect(lambda _foo, opt=property:
                                         self.has_been_modified(opt))
        for clayout, (option, default) in list(self.coloredits.items()):
            property = to_qvariant(option)
            edit = clayout.lineedit
            btn = clayout.colorbtn
            edit.setText(self.get_option(option, default))
            # QAbstractButton works differently for PySide and PyQt
            if not API == 'pyside':
                btn.clicked.connect(lambda _foo, opt=option:
                                    self.has_been_modified(opt))
            else:
                btn.clicked.connect(lambda opt=option:
                                    self.has_been_modified(opt))
            edit.textChanged.connect(lambda _foo, opt=option:
                                     self.has_been_modified(opt))
        for (clayout, cb_bold, cb_italic
             ), (option, default) in list(self.scedits.items()):
            edit = clayout.lineedit
            btn = clayout.colorbtn
            color, bold, italic = self.get_option(option, default)
            edit.setText(color)
            cb_bold.setChecked(bold)
            cb_italic.setChecked(italic)
            edit.textChanged.connect(lambda _foo, opt=option:
                                     self.has_been_modified(opt))
            # QAbstractButton works differently for PySide and PyQt
            if not API == 'pyside':
                btn.clicked.connect(lambda _foo, opt=option:
                                    self.has_been_modified(opt))
                cb_bold.clicked.connect(lambda _foo, opt=option:
                                        self.has_been_modified(opt))
                cb_italic.clicked.connect(lambda _foo, opt=option:
                                          self.has_been_modified(opt))
            else:
                btn.clicked.connect(lambda opt=option:
                                    self.has_been_modified(opt))
                cb_bold.clicked.connect(lambda opt=option:
                                        self.has_been_modified(opt))
                cb_italic.clicked.connect(lambda opt=option:
                                          self.has_been_modified(opt))

    def save_to_conf(self):
        """Save settings to configuration file"""
        for checkbox, (option, _default) in list(self.checkboxes.items()):
            self.set_option(option, checkbox.isChecked())
        for radiobutton, (option, _default) in list(self.radiobuttons.items()):
            self.set_option(option, radiobutton.isChecked())
        for lineedit, (option, _default) in list(self.lineedits.items()):
            self.set_option(option, to_text_string(lineedit.text()))
        for spinbox, (option, _default) in list(self.spinboxes.items()):
            self.set_option(option, spinbox.value())
        for combobox, (option, _default) in list(self.comboboxes.items()):
            data = combobox.itemData(combobox.currentIndex())
            self.set_option(option, from_qvariant(data, to_text_string))
        for (fontbox, sizebox), option in list(self.fontboxes.items()):
            font = fontbox.currentFont()
            font.setPointSize(sizebox.value())
            self.set_font(font, option)
        for clayout, (option, _default) in list(self.coloredits.items()):
            self.set_option(option, to_text_string(clayout.lineedit.text()))
        for (clayout, cb_bold, cb_italic), (option, _default) in list(self.scedits.items()):
            color = to_text_string(clayout.lineedit.text())
            bold = cb_bold.isChecked()
            italic = cb_italic.isChecked()
            self.set_option(option, (color, bold, italic))

    @Slot(str)
    def has_been_modified(self, option):
        self.set_modified(True)
        self.changed_options.add(option)

    def create_checkbox(self, text, option, default=NoDefault,
                        tip=None, msg_warning=None, msg_info=None,
                        msg_if_enabled=False):
        checkbox = QCheckBox(text)
        if tip is not None:
            checkbox.setToolTip(tip)
        self.checkboxes[checkbox] = (option, default)
        if msg_warning is not None or msg_info is not None:
            def show_message(is_checked=False):
                if is_checked or not msg_if_enabled:
                    if msg_warning is not None:
                        QMessageBox.warning(self, self.get_name(),
                                            msg_warning, QMessageBox.Ok)
                    if msg_info is not None:
                        QMessageBox.information(self, self.get_name(),
                                                msg_info, QMessageBox.Ok)
            checkbox.clicked.connect(show_message)
        return checkbox

    def create_radiobutton(self, text, option, default=NoDefault,
                           tip=None, msg_warning=None, msg_info=None,
                           msg_if_enabled=False, button_group=None,
                           restart=False):
        radiobutton = QRadioButton(text)
        if button_group is None:
            if self.default_button_group is None:
                self.default_button_group = QButtonGroup(self)
            button_group = self.default_button_group
        button_group.addButton(radiobutton)
        if tip is not None:
            radiobutton.setToolTip(tip)
        self.radiobuttons[radiobutton] = (option, default)
        if msg_warning is not None or msg_info is not None:
            def show_message(is_checked):
                if is_checked or not msg_if_enabled:
                    if msg_warning is not None:
                        QMessageBox.warning(self, self.get_name(),
                                            msg_warning, QMessageBox.Ok)
                    if msg_info is not None:
                        QMessageBox.information(self, self.get_name(),
                                                msg_info, QMessageBox.Ok)
            radiobutton.toggled.connect(show_message)
        radiobutton.restart_required = restart
        radiobutton.label_text = text
        return radiobutton

    def create_lineedit(self, text, option, default=NoDefault,
                        tip=None, alignment=Qt.Vertical, regex=None,
                        restart=False):
        label = QLabel(text)
        label.setWordWrap(True)
        edit = QLineEdit()
        layout = QVBoxLayout() if alignment == Qt.Vertical else QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(edit)
        layout.setContentsMargins(0, 0, 0, 0)
        if tip:
            edit.setToolTip(tip)
        if regex:
            edit.setValidator(QRegExpValidator(QRegExp(regex)))
        self.lineedits[edit] = (option, default)
        widget = QWidget(self)
        widget.label = label
        widget.textbox = edit
        widget.setLayout(layout)
        edit.restart_required = restart
        edit.label_text = text
        return widget

    def create_browsedir(self, text, option, default=NoDefault, tip=None):
        widget = self.create_lineedit(text, option, default,
                                      alignment=Qt.Horizontal)
        for edit in self.lineedits:
            if widget.isAncestorOf(edit):
                break
        msg = _("Invalid directory path")
        self.validate_data[edit] = (osp.isdir, msg)
        browse_btn = QPushButton(ima.icon('DirOpenIcon'), '', self)
        browse_btn.setToolTip(_("Select directory"))
        browse_btn.clicked.connect(lambda: self.select_directory(edit))
        layout = QHBoxLayout()
        layout.addWidget(widget)
        layout.addWidget(browse_btn)
        layout.setContentsMargins(0, 0, 0, 0)
        browsedir = QWidget(self)
        browsedir.lineedit = widget
        browsedir.setLayout(layout)
        return browsedir

    def select_directory(self, edit):
        """Select directory"""
        basedir = to_text_string(edit.text())
        if not osp.isdir(basedir):
            basedir = getcwd_or_home()
        title = _("Select directory")
        directory = getexistingdirectory(self, title, basedir)
        if directory:
            edit.setText(directory)

    def create_browsefile(self, text, option, default=NoDefault, tip=None,
                          filters=None):
        widget = self.create_lineedit(text, option, default,
                                      alignment=Qt.Horizontal)
        for edit in self.lineedits:
            if widget.isAncestorOf(edit):
                break
        msg = _('Invalid file path')
        self.validate_data[edit] = (osp.isfile, msg)
        browse_btn = QPushButton(ima.icon('FileIcon'), '', self)
        browse_btn.setToolTip(_("Select file"))
        browse_btn.clicked.connect(lambda: self.select_file(edit, filters))
        layout = QHBoxLayout()
        layout.addWidget(widget)
        layout.addWidget(browse_btn)
        layout.setContentsMargins(0, 0, 0, 0)
        browsefile = QWidget(self)
        browsefile.lineedit = widget
        browsefile.setLayout(layout)
        return browsefile

    def select_file(self, edit, filters=None):
        """Select File"""
        basedir = osp.dirname(to_text_string(edit.text()))
        if not osp.isdir(basedir):
            basedir = getcwd_or_home()
        if filters is None:
            filters = _("All files (*)")
        title = _("Select file")
        filename, _selfilter = getopenfilename(self, title, basedir, filters)
        if filename:
            edit.setText(filename)

    def create_spinbox(self, prefix, suffix, option, default=NoDefault,
                       min_=None, max_=None, step=None, tip=None):
        widget = QWidget(self)
        if prefix:
            plabel = QLabel(prefix)
            widget.plabel = plabel
        else:
            plabel = None
        if suffix:
            slabel = QLabel(suffix)
            widget.slabel = slabel
        else:
            slabel = None
        if step is not None:
            if type(step) is int:
                spinbox = QSpinBox()
            else:
                spinbox = QDoubleSpinBox()
                spinbox.setDecimals(1)
            spinbox.setSingleStep(step)
        else:
            spinbox = QSpinBox()
        if min_ is not None:
            spinbox.setMinimum(min_)
        if max_ is not None:
            spinbox.setMaximum(max_)
        if tip is not None:
            spinbox.setToolTip(tip)
        self.spinboxes[spinbox] = (option, default)
        layout = QHBoxLayout()
        for subwidget in (plabel, spinbox, slabel):
            if subwidget is not None:
                layout.addWidget(subwidget)
        layout.addStretch(1)
        layout.setContentsMargins(0, 0, 0, 0)
        widget.spinbox = spinbox
        widget.setLayout(layout)
        return widget

    def create_combobox(self, text, choices, option, default=NoDefault,
                        tip=None, restart=False):
        """choices: couples (name, key)"""
        label = QLabel(text)
        combobox = QComboBox()
        if tip is not None:
            combobox.setToolTip(tip)
        for name, key in choices:
            if not (name is None and key is None):
                combobox.addItem(name, to_qvariant(key))
        # Insert separators
        count = 0
        for index, item in enumerate(choices):
            name, key = item
            if name is None and key is None:
                combobox.insertSeparator(index + count)
                count += 1
        self.comboboxes[combobox] = (option, default)
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(combobox)
        layout.addStretch(1)
        layout.setContentsMargins(0, 0, 0, 0)
        widget = QWidget(self)
        widget.label = label
        widget.combobox = combobox
        widget.setLayout(layout)
        combobox.restart_required = restart
        combobox.label_text = text
        return widget

    def create_fontgroup(self, option=None, text=None, title=None,
                         tip=None, fontfilters=None, without_group=False):
        """Option=None -> setting plugin font"""

        if title:
            fontlabel = QLabel(title)
        else:
            fontlabel = QLabel(_("Font: "))
        fontbox = QFontComboBox()

        if fontfilters is not None:
            fontbox.setFontFilters(fontfilters)

        sizelabel = QLabel("  "+_("Size: "))
        sizebox = QSpinBox()
        sizebox.setRange(7, 100)
        self.fontboxes[(fontbox, sizebox)] = option
        layout = QHBoxLayout()

        for subwidget in (fontlabel, fontbox, sizelabel, sizebox):
            layout.addWidget(subwidget)
        layout.addStretch(1)

        widget = QWidget(self)
        widget.fontlabel = fontlabel
        widget.sizelabel = sizelabel
        widget.fontbox = fontbox
        widget.sizebox = sizebox
        widget.setLayout(layout)

        if not without_group:
            if text is None:
                text = _("Font style")

            group = QGroupBox(text)
            group.setLayout(layout)

            if tip is not None:
                group.setToolTip(tip)

            return group
        else:
            return widget

    def create_button(self, text, callback):
        btn = QPushButton(text)
        btn.clicked.connect(callback)
        btn.clicked.connect(lambda checked=False, opt='': self.has_been_modified(opt))
        return btn

    def create_tab(self, *widgets):
        """Create simple tab widget page: widgets added in a vertical layout"""
        widget = QWidget()
        layout = QVBoxLayout()
        for widg in widgets:
            layout.addWidget(widg)
        layout.addStretch(1)
        widget.setLayout(layout)
        return widget


class GeneralConfigPage(EzcadConfigPage):
    """Config page that maintains reference to main Ezcad window
       and allows to specify page name and icon declaratively
    """
    CONF_SECTION = None

    NAME = None    # configuration page name, e.g. _("General")
    ICON = None    # name of icon resource (24x24)

    def __init__(self, parent, main):
        EzcadConfigPage.__init__(self, parent)
        self.main = main

    def get_name(self):
        """Configuration page name"""
        return self.NAME

    def get_icon(self):
        """Loads page icon named by self.ICON"""
        return self.ICON

    def apply_settings(self, options):
        raise NotImplementedError

    def prompt_restart_required(self):
        """Prompt the user with a request to restart."""
        restart_opts = self.restart_options
        changed_opts = self.changed_options
        options = [restart_opts[o] for o in changed_opts if o in restart_opts]

        if len(options) == 1:
            msg_start = _("EZCAD needs to restart to change the following "
                          "setting:")
        else:
            msg_start = _("EZCAD needs to restart to change the following "
                          "settings:")
        msg_end = _("Do you wish to restart now?")

        msg_options = u""
        for option in options:
            msg_options += u"<li>{0}</li>".format(option)

        msg_title = _("Information")
        msg = u"{0}<ul>{1}</ul><br>{2}".format(msg_start, msg_options, msg_end)
        answer = QMessageBox.information(self, msg_title, msg,
                                         QMessageBox.Yes | QMessageBox.No)
        if answer == QMessageBox.Yes:
            self.restart()

    def restart(self):
        """Restart Ezcad."""
        self.main.restart()


class MainConfigPage(GeneralConfigPage):
    CONF = CONF_APP
    CONF_SECTION = "main"
    NAME = _("General")

    def setup_page(self):
        self.ICON = ima.icon('genprefs')
        newcb = self.create_checkbox

        # --- Interface
        general_group = QGroupBox(_("General"))
        languages = LANGUAGE_CODES.items()
        language_choices = sorted([(val, key) for key, val in languages])
        language_combo = self.create_combobox(_('Language'), language_choices,
                                              'interface_language',
                                              restart=True)

        general_layout = QVBoxLayout()
        general_layout.addWidget(language_combo)
        general_group.setLayout(general_layout)

        # --- Status bar
        sbar_group = QGroupBox(_("Status bar"))
        show_status_bar = newcb(_("Show status bar"), 'show_status_bar')

        memory_box = newcb(_("Show memory usage every"), 'memory_usage/enable',
                           tip=self.main.mem_status.toolTip())
        memory_spin = self.create_spinbox("", _(" ms"), 'memory_usage/timeout',
                                          min_=100, max_=1000000, step=100)
        memory_box.toggled.connect(memory_spin.setEnabled)
        memory_spin.setEnabled(self.get_option('memory_usage/enable'))
        memory_box.setEnabled(self.main.mem_status.is_supported())
        memory_spin.setEnabled(self.main.mem_status.is_supported())

        cpu_box = newcb(_("Show CPU usage every"), 'cpu_usage/enable',
                        tip=self.main.cpu_status.toolTip())
        cpu_spin = self.create_spinbox("", _(" ms"), 'cpu_usage/timeout',
                                       min_=100, max_=1000000, step=100)
        cpu_box.toggled.connect(cpu_spin.setEnabled)
        cpu_spin.setEnabled(self.get_option('cpu_usage/enable'))

        cpu_box.setEnabled(self.main.cpu_status.is_supported())
        cpu_spin.setEnabled(self.main.cpu_status.is_supported())

        status_bar_o = self.get_option('show_status_bar')
        show_status_bar.toggled.connect(memory_box.setEnabled)
        show_status_bar.toggled.connect(memory_spin.setEnabled)
        show_status_bar.toggled.connect(cpu_box.setEnabled)
        show_status_bar.toggled.connect(cpu_spin.setEnabled)
        memory_box.setEnabled(status_bar_o)
        memory_spin.setEnabled(status_bar_o)
        cpu_box.setEnabled(status_bar_o)
        cpu_spin.setEnabled(status_bar_o)

        # Layout status bar
        cpu_memory_layout = QGridLayout()
        cpu_memory_layout.addWidget(memory_box, 0, 0)
        cpu_memory_layout.addWidget(memory_spin, 0, 1)
        cpu_memory_layout.addWidget(cpu_box, 1, 0)
        cpu_memory_layout.addWidget(cpu_spin, 1, 1)

        sbar_layout = QVBoxLayout()
        sbar_layout.addWidget(show_status_bar)
        sbar_layout.addLayout(cpu_memory_layout)
        sbar_group.setLayout(sbar_layout)

        # --- Path
        path_group = QGroupBox(_("TODO"))

        tabs = QTabWidget()
        tabs.addTab(self.create_tab(path_group), _("Basic"))
        tabs.addTab(self.create_tab(general_group, sbar_group),
                    _("Advanced Settings"))

        vlayout = QVBoxLayout()
        vlayout.addWidget(tabs)
        self.setLayout(vlayout)

    def get_font(self, option):
        """Return global font used in Ezcad."""
        return get_font(option=option)

    def set_font(self, font, option):
        """Set global font used in Ezcad."""
        # Update fonts in all plugins
        set_font(font, option=option)
        plugins = self.main.widgetlist + self.main.thirdparty_plugins
        for plugin in plugins:
            plugin.update_font()

    def apply_settings(self, options):
        self.main.apply_settings()

    def _save_lang(self):
        """
        Get selected language setting and save to language configuration file.
        """
        for combobox, (option, _default) in list(self.comboboxes.items()):
            if option == 'interface_language':
                data = combobox.itemData(combobox.currentIndex())
                value = from_qvariant(data, to_text_string)
                break
        save_lang_conf(value)
        self.set_option('interface_language', value)
