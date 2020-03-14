# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

import os

from datetime import timedelta
LMT_LST_DELTA = timedelta(seconds=1)

NCORE = os.cpu_count()

# import sys
# sys.path.append('/home/zhu/code/python')

# https://www.sqlite.org/limits.html
# The maximum size of any string or BLOB or table row, in bytes.
SQLITE_LIMIT_LENGTH = 1000000000  # 1 billion bytes

# 2018/8/18 I tried 90 million vertexes and too slow.
# PLOT2D_LIMIT = 10000000  # pyqtgraph.PlotWidget

# Primary and secondary disks for JavaSeis dataset
JAVASEIS_DATA_HOME = os.getenv('JAVASEIS_DATA_HOME')
JAVASEIS_DATA_SECONDARIES = [os.getenv('JAVASEIS_DATA_SECONDARIES')]

SURVEY_BOX_LINE = 'SURVEY_BOX_LINE'
SURVEY_BOX_LABEL = 'SURVEY_BOX_LABEL'

GEOMETRY_TYPES = ['Point', 'Line', 'Tsurface', 'Gsurface', 'Cube',
                  'Label', 'Survey']

SECTION_TYPES = ('iline', 'xline', 'depth')

FILTER_ALL_FILES = ";;All files (*)"

COORDINATE_PROPERTY_NAMES = ('X', 'Y', 'Z')
DEFAULT_PROPERTY_NAMES = ('X', 'Y', 'Z', 'A', 'B', 'C', 'D', 'E', 'F',
                          'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O')

DELIMITER2CHAR = {
    "comma": ",",
    ",": ",",
    "space": " ",
    " ": " ",
}
