# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

# import os
import logging
from qtpy.QtCore import QObject, Signal
# from ezcad.config.base import get_home_dir


class QtHandler(logging.Handler, QObject):
    sigLog = Signal(str)
    def __init__(self):
        QObject.__init__(self)
        logging.Handler.__init__(self)

    def emit(self, logRecord):
        #message = str(logRecord.getMessage()) # no level
        message = self.format(logRecord)
        self.sigLog.emit(message)


formatter = logging.Formatter("%(levelname)s: %(message)s")
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - <%(module)s : %(lineno)d> - %(message)s')

qtHandler = QtHandler()
qtHandler.setFormatter(formatter)
# qtHandler.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
# diff of logger.setLevel() and Handler.setLevel()?
logger.setLevel(logging.DEBUG)
logger.addHandler(qtHandler)

# Before 2018/8/31, the stream flows as following:
#   logger.info() > logger handlers > qtHangler > emit > XStream write >
#   messageWritten signal emit > mainwindow.set_print connects to slot >
#   print2 > process_log.logbox.textBrowser > cursor insert text >
#   QApplication.processEvents update GUI, which is not safe.
# After Change the QtHandler to signal/slot mechanism, the flow is:
#   logger.info() > logger handlers > qtHangler > emit > textBrowser

# home = get_home_dir()
# logfn = os.path.join(home, 'ezcad.log')
# fh = logging.FileHandler(logfn, mode='w')
# fh.setLevel(logging.DEBUG)
# fh.setFormatter(formatter)
# logger.addHandler(fh)

# import sys
# def my_handler(type, value, tb):
#     logger.exception("Uncaught exception: {0}".format(str(value)))
# sys.excepthook = my_handler # install exception handler
