# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

import copy
from qtpy.QtCore import Qt, Signal
from qtpy.QtWidgets import QTreeWidget, QTreeWidgetItem

from ezcad.config.base import _
from ezcad.widgets.ezdialog import EasyDialog
from ezcad.widgets.projects.config import EXTMODULES_DEFAULTS_DICT
from ezcad.utils.logger import logger


class SelectModules(EasyDialog):
    NAME = _("Select modules")
    sigExtModules = Signal(dict)

    def __init__(self, parent=None, test=False):
        EasyDialog.__init__(self, parent)
        self.setup_page()
        if test:
            self.add_items()
            self.treeWidget.expandAll()

    def setup_page(self):
        self.treeWidget = QTreeWidget(self)
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.itemChanged.connect (self.check_changed)
        self.layout.addWidget(self.treeWidget)

        action = self.create_action()
        self.layout.addWidget(action)

    def check_changed(self, item, column):
        key = item.text(column)
        subitemName = item.text(column)
        try:
            itemName = item.parent().text(0)
            key = itemName + '/' + subitemName
            if item.checkState(column) == Qt.Checked:
                self.extmodules[key] = True
            elif item.checkState(column) == Qt.Unchecked:
                self.extmodules[key] = False
            else:
                pass
        except AttributeError:
            pass

    def add_items(self, defaults=None):
        """
        -i- defaults : dict, current selection of modules
        """
        if defaults is None:
            self.extmodules = copy.deepcopy(EXTMODULES_DEFAULTS_DICT)
        else:
            self.extmodules = defaults
        itemNameOld = None
        for option in sorted(self.extmodules.keys()):
            itemName, subitemName = option.split('/')
            checkState = self.extmodules[option]
            if itemName != itemNameOld:
                item = QTreeWidgetItem(self.treeWidget)
                item.setText(0, _(itemName))
                item.setFlags(item.flags() | Qt.ItemIsTristate |
                      Qt.ItemIsUserCheckable)
                itemNameOld = itemName
            subitem = QTreeWidgetItem(item)
            subitem.setText(0, subitemName)
            subitem.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if checkState == 'True':
                subitem.setCheckState(0, Qt.Checked)
            else:
                subitem.setCheckState(0, Qt.Unchecked)

    def apply(self):
        logger.info("External modules: {}".format(str(self.extmodules)))
        self.sigExtModules.emit(self.extmodules)


def main():
    from qtpy.QtWidgets import QApplication
    app = QApplication([])
    test = SelectModules(test=True)
    test.show()
    app.exec_()


if __name__ == '__main__':
    main()
