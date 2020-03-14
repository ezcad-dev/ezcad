# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

from qtpy.QtCore import QThread


class WorkerThread(QThread):
    def __init__(self, func, args):
        super(WorkerThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)


def some_process():
    print('in thread')


def main():
    print('start')
    # some_process()
    worker = WorkerThread(some_process, ())
    worker.start()
    # let the worker thread finish before mother thread finish
    import time
    time.sleep(5)
    print('end')


if __name__ == '__main__':
    main()
