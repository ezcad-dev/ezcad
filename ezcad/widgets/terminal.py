# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

# Standard library imports
import os

# Third party imports
from qtpy.QtCore import Signal, QSize, Qt
from qtpy.QtWidgets import (QWidget, QLabel, QLineEdit, QMessageBox,
                            QHBoxLayout, QVBoxLayout, QPlainTextEdit,
                            QFileDialog, QFormLayout)

# Local imports
from ezcad.utils.syntax import PythonHighlighter
from ezcad.utils.qthelpers import (create_plugin_layout, create_toolbutton,
                                   create_toolbutton_help)
from ezcad.utils import icon_manager as ima
from ezcad.config.base import _


class Terminal(QWidget):
    sigRunScript = Signal(str)

    def __init__(self, parent=None, options_button=None):
        QWidget.__init__(self, parent)

        self.setup_mainwidget()

        btn_layout = QHBoxLayout()
        for btn in self.setup_buttons():
            btn.setIconSize(QSize(16, 16))
            btn_layout.addWidget(btn)
        if options_button:
            btn_layout.addStretch()
            btn_layout.addWidget(options_button, Qt.AlignRight)

        layout = create_plugin_layout(btn_layout, self.mainwidget)
        self.setLayout(layout)

    def setup_mainwidget(self):
        lblRunFile = QLabel('Run File')
        self.lineRunFile = QLineEdit()

        lblOpenFile = QLabel('Open File')
        self.lineOpenFile = QLineEdit()

        fbox = QFormLayout()
        fbox.addRow(lblRunFile, self.lineRunFile)
        fbox.addRow(lblOpenFile, self.lineOpenFile)

        text = "# myprint(self.database) \n" +\
               "# myprint(self.treebase)"
        self.code_view = QPlainTextEdit(text, self)
        # font = QFont()
        # font.setFamily(_fromUtf8("FreeMono"))
        # self.code_view.setFont(font)

        vbox = QVBoxLayout()
        vbox.addLayout(fbox)
        vbox.addWidget(self.code_view)

        self.mainwidget = QWidget(self)
        self.mainwidget.setLayout(vbox)

        # connect syntax highlighter
        self.pyhigh = PythonHighlighter(self.code_view.document())
        self.code_view.textChanged.connect(self.highlightWhileTyping)

    def setup_buttons(self):

        # TODO how to fix this bug?
        # shortcut in plugin conflicts with shortcut in mainwindow
        # QAction::eventFilter: Ambiguous shortcut overload: Ctrl+O

        openfile_btn = create_toolbutton(self,
                             icon=ima.icon('fileopen'),
                             tip=_('Open file'),
                             shortcut="Ctrl+O",
                             triggered=self.open_file)
        savefile_btn = create_toolbutton(self,
                             icon=ima.icon('filesave'),
                             tip=_('Save to new file'),
                             shortcut="Ctrl+S",
                             triggered=self.save_file)
        runfile_btn = create_toolbutton(self,
                             icon=ima.icon('run_file'),
                             tip=_('Run code in file'),
                             triggered=self.run_file)
        run_btn = create_toolbutton(self,
                             icon=ima.icon('run'),
                             tip=_('Run code in view'),
                             shortcut="Ctrl+R",
                             triggered=self.emit_script)
        help_btn = create_toolbutton_help(self, triggered=self.show_help)
        buttons = (openfile_btn, savefile_btn, runfile_btn, run_btn, help_btn)
        return buttons

    def show_help(self):
        QMessageBox.information(self, _('How to use'),
            _("The project console provides API to the project.<br>"
              "For example, try run myprint(self.database).<br>"
              "Due to Cython compiler, use myprint() for print().<br>"
              "<b>TODO</b> add more.<br>"))

    def highlightWhileTyping(self):
        # Instantiate class PythonHighlighter everytime text is changed
        # RecursionError: maximum recursion depth exceeded...
        # text = self.code_view.toPlainText()
        # highlight = PythonHighlighter(self.code_view.document())
        # self.code_view.setPlainText(text)
        text = self.code_view.toPlainText()
        self.pyhigh.highlightBlock(text)

    def run_file(self):
        """Run a script file without open it. Assume edited in a
        user-favorite text editor. """
        fn = self.lineRunFile.text()
        text = open(fn).read()
        self.sigRunScript.emit(text)

    def open_file(self):
        if hasattr(self, 'workdir') :
            workdir = self.workdir
        else :
            workdir = os.getcwd()
        fn = QFileDialog.getOpenFileName(self, 'Open File', workdir)
        # If hit Cancel at dialog, fn is string of length zero.
        # If still go ahead open(fn), receive FileNotFoundError.
        if len(fn) > 0 :
            # Windows returns tuple
            fn = fn[0] if isinstance(fn, tuple) else fn
            self.lineOpenFile.setText(fn)
            text = open(fn).read()
            self.code_view.setPlainText(text)

    def save_file(self):
        if hasattr(self, 'workdir') :
            workdir = self.workdir
        else :
            workdir = os.getcwd()
        fn = QFileDialog.getSaveFileName(self, 'Save File', workdir)
        if len(fn) > 0 :
            text = self.code_view.toPlainText()
            with open(fn, 'w') as f:
                f.write(text)

    def emit_script(self):
        """
        Send script text to parent to run.
        """
        text = self.code_view.toPlainText()
        print2logger = 'from ezcad.utils.functions import myprint \n'
        text = print2logger + text
        self.sigRunScript.emit(text)

    def run_script(self):
        """ Deprecated run at local with limited data access"""
        text = self.code_view.toPlainText()
        try :
            eval(text)
        except SyntaxError :
            exec(text)

    def set_work_dir(self, workdir):
        self.workdir = workdir


def main():
    import sys
    from qtpy.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = Terminal()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
