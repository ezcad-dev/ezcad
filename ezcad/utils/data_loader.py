# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

"""
This class does these tasks:
    1) Take user input - filenames etc. - from dialog or script
    2) Route load job to multi threads
    3) Load data from file and create data object of ezcad
    4) Transmit the data object to data tree for add to ezcad
"""

import os
from qtpy.QtCore import Signal, Qt
from qtpy.QtWidgets import QWidget, QFileDialog, QApplication
from qtpy.compat import getexistingdirectory


class DataLoader(QWidget):
    sigDataObjectLoaded = Signal(object)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # This is to keep a window to the parent, thus can use
        # the settings from the main window such as project sgmtfn.
        self.main = parent

        self.workerThreads = []
        self.set_work_dir()

    def select_file(self, flt=''):
        """Select file dialog.

        :param flt: filters
        :type flt: str
        :return: filename
        :rtype: str
        """
        # flt = "SGMT files (*.sgmt);;All Files (*)"
        filename = QFileDialog.getOpenFileName(self, "Open files",
            self.workdir, flt)
        print('Selected file:', filename)
        return filename

    def select_folder(self):
        """Select folder dialog.

        :return: foldername
        :rtype: str
        """
        # foldername = QFileDialog.getExistingDirectory(self,
        #              "Select folder", self.workdir)
        title = "Select directory"
        basedir = self.workdir
        foldername = getexistingdirectory(self, title, basedir)
        print('Selected folder:', foldername)
        return foldername

    def select_files(self, flt=''):
        """Select files dialog.

        :param flt: filters
        :type flt: str
        :return: filenames, each element is a string
        :rtype: list
        """
        # flt = "All Files (*);;CSV files (*.csv)"
        files = QFileDialog.getOpenFileNames(self, "Open files",
                                             self.workdir, flt)
        print('Selected files:', files)
        if type(files) is list:
            # Linux, [fn1, fn2]
            return files
        elif type(files) is tuple:
            # Windows, ([fn1, fn2], 'filter')
            return files[0]
        else:
            raise ValueError

    def set_work_dir(self, workdir=None):
        if workdir is None:
            self.workdir = os.getcwd()
        else:
            self.workdir = workdir

    def todo(self):
        raise NotImplementedError
