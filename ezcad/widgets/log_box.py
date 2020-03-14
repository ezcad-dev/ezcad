# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

# Third party imports
from qtpy.QtCore import QSize, Qt
from qtpy.QtWidgets import QTextBrowser, QWidget, QHBoxLayout, QMessageBox

# Local imports
from ezcad.utils.qthelpers import (create_plugin_layout, create_toolbutton,
                                   create_toolbutton_help)
from ezcad.utils import icon_manager as ima
from ezcad.config.base import _


class LogBox(QWidget):
    def __init__(self, parent=None, options_button=None):
        QWidget.__init__(self, parent)

        # central widget
        self.textBrowser = QTextBrowser(self)
        # self.textBrowser = TextBrowserBase(self)

        btn_layout = QHBoxLayout()
        for btn in self.setup_buttons():
            btn.setIconSize(QSize(16, 16))
            btn_layout.addWidget(btn)
        if options_button:
            btn_layout.addStretch()
            btn_layout.addWidget(options_button, Qt.AlignRight)

        layout = create_plugin_layout(btn_layout, self.textBrowser)
        self.setLayout(layout)

    def setup_buttons(self):
        clear_btn = create_toolbutton(self,
                             icon=ima.icon('clear_text'),
                             tip=_('Clear text'),
                             shortcut="Ctrl+L",
                             triggered=self.textBrowser.clear)
        dummy_btn = create_toolbutton(self,
                             icon=ima.icon('fromcursor'),
                             tip=_('Do nothing'))
        help_btn = create_toolbutton_help(self, triggered=self.show_help)
        return clear_btn, dummy_btn, help_btn

    def show_help(self):
        QMessageBox.information(self, _('How to use'),
            _("Double click a word to highlight then Ctrl+F to find.<br>"
              "<b>TODO</b> add more.<br>"))


# class TextBrowserBase(QTextBrowser, BaseEditMixin):
#     """ Text browser with find/search support """
#     def __init__(self, parent=None):
#         QTextBrowser.__init__(self, parent)
#         BaseEditMixin.__init__(self)
