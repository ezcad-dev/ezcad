# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

from qtpy.QtCore import Signal, QSize, Qt, Slot
from qtpy.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QPlainTextEdit, \
    QTextEdit, QRadioButton, QButtonGroup, QCheckBox, QDialog, \
    QStackedWidget, QListWidget, QPushButton, QDialogButtonBox, QListView, \
    QSplitter, QVBoxLayout, QScrollArea, QListWidgetItem
from ezcad.config.base import _, load_lang_conf
from ezcad.config.main import CONF
from ezcad.widgets.ezdialog import EasyDialog
from ezcad.utils.envars import GEOMETRY_TYPES, FILTER_ALL_FILES
from ezcad.utils import icon_manager as ima


class RemoveObjectDialog(EasyDialog):
    NAME = _("Remove object")
    sig_start = Signal(str)

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent)
        self.setup_page()

    def setup_page(self):
        text = _("Object")
        self.grabob = self.create_grabob(text, geom=GEOMETRY_TYPES)
        self.layout.addWidget(self.grabob)

        action = self.create_action()
        self.layout.addWidget(action)

    def apply(self):
        object_name = self.grabob.lineedit.edit.text()
        self.sig_start.emit(object_name)


class RenameObjectDialog(EasyDialog):
    NAME = _("Rename object")
    sig_start = Signal(str, str)

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent)
        self.setup_page()

    def setup_page(self):
        text = _("Object")
        self.grabob = self.create_grabob(text, geom=GEOMETRY_TYPES)
        self.layout.addWidget(self.grabob)

        text = _("New name")
        self.new_name = self.create_lineedit(text)
        self.layout.addWidget(self.new_name)

        action = self.create_action()
        self.layout.addWidget(action)

    def grab_object_rc(self):
        """ Used when dialog is brought up by right click in tree. """
        dob = self.treebase.grab_object(GEOMETRY_TYPES)
        self.grabob.lineedit.edit.setText(dob.name)

    def apply(self):
        object_name = self.grabob.lineedit.edit.text()
        new_name = self.new_name.edit.text()
        # self.treebase.rename_object(object_name, new_name)
        self.sig_start.emit(object_name, new_name)


class RemovePropertyDialog(EasyDialog):
    NAME = _("Remove property")
    sig_start = Signal(str, str)

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent)
        self.setup_page()

    def setup_page(self):
        text = _("Object")
        self.grabob = self.create_grabob(text, geom=GEOMETRY_TYPES)
        self.layout.addWidget(self.grabob)

        text = _("Property")
        self.prop = self.create_combobox(text)
        self.layout.addWidget(self.prop)

        action = self.create_action()
        self.layout.addWidget(action)

    def grab_object_rc(self):
        """ Used when dialog is brought up by right click in tree. """
        geom = ['Point', 'Line', 'Tsurface', 'Gsurface', 'Cube']
        self.dob = self.treebase.grab_object(geom)
        self.grabob.lineedit.edit.setText(self.dob.name)
        self.propList = list(self.dob.prop.keys())
        self.prop.combobox.clear()
        self.prop.combobox.addItems(self.propList)
        self.grab_property()

    def load_object(self):
        self.dob = self.object  # from EasyDialog grab_object
        self.propList = list(self.dob.prop.keys())
        self.prop.combobox.clear()
        self.prop.combobox.addItems(self.propList)
        self.grab_property()

    def grab_property(self):
        prop_name = self.dob.current_property
        index = self.propList.index(prop_name)
        self.prop.combobox.setCurrentIndex(index)

    def apply(self):
        object_name = self.grabob.lineedit.edit.text()
        property_name = self.prop.combobox.currentText()
        self.sig_start.emit(object_name, property_name)


class RenamePropertyDialog(EasyDialog):
    NAME = _("Rename property")
    sig_start = Signal(str, str, str)

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent)
        self.setup_page()

    def setup_page(self):
        text = _("Object")
        self.grabob = self.create_grabob(text, geom=GEOMETRY_TYPES)
        self.layout.addWidget(self.grabob)

        text = _("Property")
        self.prop = self.create_combobox(text)
        self.layout.addWidget(self.prop)

        text = _("New name")
        self.new_name = self.create_lineedit(text)
        self.layout.addWidget(self.new_name)

        action = self.create_action()
        self.layout.addWidget(action)

    def grab_object_rc(self):
        """ Used when dialog is brought up by right click in tree. """
        geom = ['Point', 'Line', 'Tsurface', 'Gsurface', 'Cube']
        self.dob = self.treebase.grab_object(geom)
        self.grabob.lineedit.edit.setText(self.dob.name)
        self.propList = list(self.dob.prop.keys())
        self.prop.combobox.clear()
        self.prop.combobox.addItems(self.propList)
        self.grab_property()

    def load_object(self):
        self.dob = self.object  # from EasyDialog grab_object
        self.propList = list(self.dob.prop.keys())
        self.prop.combobox.clear()
        self.prop.combobox.addItems(self.propList)
        self.grab_property()

    def grab_property(self):
        prop_name = self.dob.current_property
        index = self.propList.index(prop_name)
        self.prop.combobox.setCurrentIndex(index)

    def apply(self):
        object_name = self.grabob.lineedit.edit.text()
        property_name = self.prop.combobox.currentText()
        new_name = self.new_name.edit.text()
        self.sig_start.emit(object_name, property_name, new_name)


class LoadObjectDialog(EasyDialog):
    NAME = _("Load object")
    HELP_BODY = _("The original object name was saved into the db file, "
        "so you don't have to supply it, in which case, just leave it "
        "blank or DEFAULT.")
    sig_start = Signal(str, str)

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent)
        self.setup_page()

    def setup_page(self):
        filters = "DB files (*.db)" + FILTER_ALL_FILES
        self.input = self.create_browsefile(_("Object file"), filters=filters)
        self.layout.addWidget(self.input)

        # Avoid use self.object_name so not set filename as default
        # The desired default is blank, so use the name saved in db.
        self.name = self.create_lineedit("Object name", default="DEFAULT")
        self.layout.addWidget(self.name)

        action = self.create_action()
        self.layout.addWidget(action)

    def apply(self):
        fn = self.input.lineedit.edit.text()
        object_name = self.name.edit.text()
        self.sig_start.emit(fn, object_name)


class SaveObjectDialog(EasyDialog):
    NAME = _("Save object")
    HELP_BODY = _("The recommended filename extension is db (e.g. myobj.db), "
        "which is the default filter at load object. But the filename can "
        "have any extension, and you'd switch the filter to \"All files\".")
    sig_start = Signal(str, str)

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent)
        self.setup_page()

    def setup_page(self):
        text = _("Object")
        self.grabob = self.create_grabob(text, geom=GEOMETRY_TYPES)
        self.layout.addWidget(self.grabob)

        self.output = self.create_browsefile(_("File"), new=True)
        self.layout.addWidget(self.output)

        action = self.create_action()
        self.layout.addWidget(action)

    def apply(self):
        fn = self.output.lineedit.edit.text()
        object_name = self.grabob.lineedit.edit.text()
        self.sig_start.emit(object_name, fn)


class CopyObjectDialog(EasyDialog):
    NAME = _("Copy object")
    sig_start = Signal(str, str)

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent)
        self.setup_page()

    def setup_page(self):
        text = _("Object")
        self.grabob = self.create_grabob(text, geom=GEOMETRY_TYPES)
        self.layout.addWidget(self.grabob)

        text = _("New name")
        self.new_name = self.create_lineedit(text)
        self.layout.addWidget(self.new_name)

        action = self.create_action()
        self.layout.addWidget(action)

    def grab_object_rc(self):
        """ Used when dialog is brought up by right click in tree. """
        dob = self.treebase.grab_object(GEOMETRY_TYPES)
        self.grabob.lineedit.edit.setText(dob.name)

    def apply(self):
        object_name = self.grabob.lineedit.edit.text()
        new_name = self.new_name.edit.text()
        self.sig_start.emit(object_name, new_name)


class CreatePropertyDialog(EasyDialog):
    NAME = _("Create property")
    HELP_BODY = _("The new property is initialized with zeros.<br>")
    sig_start = Signal(str, str)

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent)
        self.setup_page()

    def setup_page(self):
        text = _("Object")
        self.grabob = self.create_grabob(text, geom=GEOMETRY_TYPES)
        self.layout.addWidget(self.grabob)

        text = _("Property name")
        self.prop_name = self.create_lineedit(text)
        self.layout.addWidget(self.prop_name)

        action = self.create_action()
        self.layout.addWidget(action)

    def grab_object_rc(self):
        """ Used when dialog is brought up by right click in tree. """
        dob = self.treebase.grab_object(GEOMETRY_TYPES)
        self.grabob.lineedit.edit.setText(dob.name)

    def apply(self):
        object_name = self.grabob.lineedit.edit.text()
        prop_name = self.prop_name.edit.text()
        # self.treebase.create_property(object_name, prop_name)
        self.sig_start.emit(object_name, prop_name)


class PropertyOperatorDialog(EasyDialog):
    NAME = _("Property operator")
    HELP_BODY = _("Example script<br><br>"
        "propA = - propA <br><br>"
        "import numpy as np <br>"
        "propB = np.log10(abs(propA))")
    sig_start = Signal(str, str)

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent)
        self.setup_page()

    def setup_page(self):
        text = _('Object')
        geom = ['Point', 'Line', 'Tsurface', 'Gsurface', 'Cube']
        self.grabob = self.create_grabob(text, geom=geom)
        self.layout.addWidget(self.grabob)

        text = _('Region')
        default = _("Not available yet")
        self.region = self.create_lineedit(text, default=default)
        self.layout.addWidget(self.region)

        lblScript = QLabel(_('Script'))
        self.layout.addWidget(lblScript)

        self.pteScript = QPlainTextEdit()
        self.layout.addWidget(self.pteScript)

        action = self.create_action()
        self.layout.addWidget(action)

    def apply(self):
        object_name = self.grabob.lineedit.edit.text()
        script = self.pteScript.toPlainText()
        self.sig_start.emit(object_name, script)


class ReportBugDialog(EasyDialog):
    NAME = _("Report bug")
    HELP_BODY = _("Please copy-n-paste the error message in the "
        "Process log (if any). Please explain briefly what you were "
        "doing when the bug occurred. Please add anything that can "
        "help me reproduce the error. Thanks for your time and "
        "contribution to improving ezcad.")
    sig_start = Signal(str, str, str, str, str)

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent)
        self.setup_page()

    def setup_page(self):
        text = _("Email server")
        default = 'localhost'
        self.server = self.create_lineedit(text, default=default)
        self.layout.addWidget(self.server)

        text = _("Sender")
        default = 'email address e.g. joe@gmail.com'
        self.sender = self.create_lineedit(text, default=default)
        self.layout.addWidget(self.sender)

        text = _("Receivers")
        default = 'email addresses separated by comma'
        self.receivers = self.create_lineedit(text, default=default)
        self.layout.addWidget(self.receivers)

        text = _("Subject")
        self.subject = self.create_lineedit(text)
        self.layout.addWidget(self.subject)

        self.body = QTextEdit(self)
        self.body.setFontFamily("monospace")
        self.body.setText(self.helpMessage)
        self.layout.addWidget(self.body)

        action = self.create_action()
        self.layout.addWidget(action)

    def apply(self):
        server = self.server.edit.text()
        sender = self.sender.edit.text()
        receivers = self.receivers.edit.text()
        subject = self.subject.edit.text()
        body = self.body.toPlainText()
        receivers = [x.strip() for x in receivers.split(',')]
        self.sig_start.emit(sender, receivers, subject, body, server)


class AspectRatioDialog(EasyDialog):
    NAME = _("Set viewer aspect ratio")
    sigApply = Signal(str, float)

    def __init__(self, parent=None, state=None):
        EasyDialog.__init__(self, parent=parent)
        self.setup_page()
        if state is not None:
            self.load_state(state)

    def setup_page(self):
        lblMethod = QLabel(_("Method"))
        self.rbAuto = QRadioButton(_("Auto"))
        self.rbEqual = QRadioButton(_("Equal"))
        self.rbFixed = QRadioButton(_("Fixed"))
        bgSystem = QButtonGroup()
        bgSystem.addButton(self.rbAuto)
        bgSystem.addButton(self.rbEqual)
        bgSystem.addButton(self.rbFixed)
        hbox = QHBoxLayout()
        hbox.addWidget(lblMethod)
        hbox.addWidget(self.rbAuto)
        hbox.addWidget(self.rbEqual)
        hbox.addWidget(self.rbFixed)
        self.layout.addLayout(hbox)

        text = _("Fixed ratio Y/X")
        self.ratio = self.create_lineedit(text, default='1.0')
        self.layout.addWidget(self.ratio)

        action = self.create_action()
        self.layout.addWidget(action)

        self.rbAuto.toggled.connect(lambda: self.set_method(self.rbAuto))
        self.rbEqual.toggled.connect(lambda: self.set_method(self.rbEqual))
        self.rbFixed.toggled.connect(lambda: self.set_method(self.rbFixed))
        self.rbEqual.setChecked(True)
        self.ratio.setEnabled(False)

    def set_method(self, rb):
        if rb.isChecked():
            if rb.text() == _("Auto"):
                self.method = 'Auto'
            elif rb.text() == _("Equal"):
                self.method = 'Equal'
            elif rb.text() == _("Fixed"):
                self.method = 'Fixed'
                self.ratio.setEnabled(True)
            else:
                raise ValueError("unknown value {}".format(rb.text()))

    def load_state(self, state):
        """
        -i- state : dictionary.
        Load current state and show it in dialog.
        """
        method = state['aspect_method']
        ratio = state['aspect_ratio']
        if method == 'Auto':
            self.rbAuto.setChecked(True)
        elif method == 'Equal':
            self.rbEqual.setChecked(True)
        elif method == 'Fixed':
            self.rbFixed.setChecked(True)
            self.ratio.edit.setText(str(ratio))
        else:
            raise ValueError("Unknown value")

    def apply(self):
        method = self.method
        ratio = float(self.ratio.edit.text())

        # self.state was from the parent and changes had been applied to
        # the parent settings, i.e. they share the same memory address.
        # Thus, no need to emit the self.state dictionary to the caller.
        # The above design is bad in that the dialog is entangled.
        # Use signal/slot to make the dialog simple in its task.
        self.sigApply.emit(method, ratio)


class CanvasExportDialog(EasyDialog):
    NAME = _("Export canvas to PNG picture")
    sig_start = Signal(str, bool)

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent)
        self.setup_page()

    def setup_page(self):
        self.output = self.create_browsefile(_("File"),
            default="canvas.png", new=True)
        self.layout.addWidget(self.output)

        self.cbClipboard = QCheckBox("Copy to clipboard")
        self.cbClipboard.setChecked(True)
        self.layout.addWidget(self.cbClipboard)

        action = self.create_action()
        self.layout.addWidget(action)

    def apply(self):
        fn = self.output.lineedit.edit.text()
        copy2cb = True if self.cbClipboard.isChecked() else False
        self.sig_start.emit(fn, copy2cb)


class ConfigDialog(QDialog):
    """Configuration or preferences dialog box"""

    # Signals
    check_settings = Signal()
    size_change = Signal(QSize)

    def __init__(self, parent=None, objname=None):
        QDialog.__init__(self, parent)

        # If used for data object in tree, the main is the tree widget.
        self.parent = parent
        self.objname = objname

        # Widgets
        self.pages_widget = QStackedWidget()
        self.contents_widget = QListWidget()
        self.button_reset = QPushButton(_('Reset to defaults'))

        bbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Apply |
                                QDialogButtonBox.Cancel)
        self.apply_btn = bbox.button(QDialogButtonBox.Apply)

        # Widgets setup
        # Destroying the C++ object right after closing the dialog box,
        # otherwise it may be garbage-collected in another QThread
        # (e.g. the editor's analysis thread in Ezcad), thus leading to
        # a segmentation fault on UNIX or an application crash on Windows
        self.setAttribute(Qt.WA_DeleteOnClose)
        if self.objname is None:
            self.setWindowTitle(_('Preferences'))
        else:
            self.setWindowTitle(_('Preferences of ') + self.objname)
        self.setWindowIcon(ima.icon('configure'))
        self.contents_widget.setMovement(QListView.Static)
        self.contents_widget.setSpacing(1)
        self.contents_widget.setCurrentRow(0)

        # Layout
        hsplitter = QSplitter()
        hsplitter.addWidget(self.contents_widget)
        hsplitter.addWidget(self.pages_widget)
        hsplitter.setSizes([150,500])

        btnlayout = QHBoxLayout()
        btnlayout.addWidget(self.button_reset)
        btnlayout.addStretch(1)
        btnlayout.addWidget(bbox)

        vlayout = QVBoxLayout()
        vlayout.addWidget(hsplitter)
        vlayout.addLayout(btnlayout)

        self.setLayout(vlayout)

        # Signals and slots
        self.pages_widget.currentChanged.connect(self.current_page_changed)
        self.contents_widget.currentRowChanged.connect(
            self.pages_widget.setCurrentIndex)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)
        bbox.clicked.connect(self.button_clicked)

        # Ensures that the config is present on ezcad first run
        CONF.set('main', 'interface_language', load_lang_conf())

    def get_current_index(self):
        """Return current page index"""
        return self.contents_widget.currentRow()

    def set_current_index(self, index):
        """Set current page index"""
        self.contents_widget.setCurrentRow(index)

    def get_page(self, index=None):
        """Return page widget"""
        if index is None:
            widget = self.pages_widget.currentWidget()
        else:
            widget = self.pages_widget.widget(index)
        return widget.widget()

    @Slot()
    def accept(self):
        """Reimplement Qt method"""
        for index in range(self.pages_widget.count()):
            configpage = self.get_page(index)
            configpage.apply_changes()
        QDialog.accept(self)

    def button_clicked(self, button):
        if button is self.apply_btn:
            # Apply button was clicked
            configpage = self.get_page()
            configpage.apply_changes()

    def current_page_changed(self, index):
        # widget = self.get_page(index)
        self.apply_btn.setVisible(True)
        self.apply_btn.setEnabled(True)

    def add_page(self, widget):
        scrollarea = QScrollArea(self)
        scrollarea.setWidgetResizable(True)
        scrollarea.setWidget(widget)
        self.pages_widget.addWidget(scrollarea)
        item = QListWidgetItem(self.contents_widget)
        try:
            item.setIcon(widget.get_icon())
        except TypeError:
            pass
        item.setText(widget.get_name())
        item.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        item.setSizeHint(QSize(0, 25))

    def check_all_settings(self):
        """This method is called to check all configuration page settings
        after configuration dialog has been shown"""
        self.check_settings.emit()

    def resizeEvent(self, event):
        """
        Reimplement Qt method to be able to save the widget's size from the
        main application
        """
        QDialog.resizeEvent(self, event)
        self.size_change.emit(self.size())


def main():
    from qtpy.QtWidgets import QApplication
    app = QApplication([])
    test = RemoveObjectDialog()
    test.show()
    app.exec_()


if __name__ == '__main__':
    main()
