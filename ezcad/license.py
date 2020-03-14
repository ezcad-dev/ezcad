# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
"""
License file
"""

from datetime import datetime


EXPIRATION_DATE = datetime(2020, 12, 31, 23, 59)


def check_license():
    """
    Check if the license is expired
    One way to grant license is provide a new ezcad/utils/envars.so file
    which has the extended EXPIRATION_DATE.
    """
    now = datetime.now()
    if now > EXPIRATION_DATE:
        print("Your license was expired at {}".format(EXPIRATION_DATE))
        # mainwindow.ask_before_exit = False
        # mainwindow.close()
        exit()
    else:
        print("Your license is live till {}".format(EXPIRATION_DATE))
