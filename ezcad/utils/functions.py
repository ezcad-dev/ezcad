# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

import sys
import locale
import numpy as np
from ezcad.utils.envars import DELIMITER2CHAR
from ezcad.utils.logger import logger


def table2array(table, comment, delimiter):
    """Convert textual table to numeric array.

    :param table: textual table, usually from GUI text box
    :type table: str
    :param comment: character denoting comment line, such as #, !
    :type comment: char
    :param delimiter: delimiter for columns
    :type delimiter: str
    :returns: numeric data array
    :rtype: array
    """
    delim = DELIMITER2CHAR[delimiter]
    data_list = []
    lines = table.split('\n')
    for line in lines:
        line = line.strip()  # remove heading/tailing spaces
        if len(line) == 0:  # skip blank line
            continue
        if line[0] == comment:  # skip comment line
            continue
        p = line.split(delim)
        p = [float(v) for v in p]
        data_list.append(p)
    return np.array(data_list)


def save_display_state(dpState, object_name, childName, grandchildName,
                       state):
    """
    -i- dpState : dictionary, save the state.
    -i- object_name : string, the name of the data object.
    -i- childName : string, the level below dob, e.g. properties, sections.
    -i- grandchildName : string, name of property or section.
    -i- state : bool, True means the item display on, False means off.
    The caller is viewer. The state is saved one for each viewer.
    The state is used to refresh the data tree when switch between viewers.

    An example entry is...
    {'cube2018' :
        'object' :
            { 'self': True }
        'properties' :
            { 'vavg': True, 'vint': False, 'vrms': False }
        'sections' :
            { 'iline': True, 'xline': True, 'depth': False, 'aline1': True }}

    """
    lev1, lev2, lev3 = object_name, childName, grandchildName

    if state:  # save checked item
        if lev1 in dpState:
            if lev2 in dpState[lev1]:
                dpState[lev1][lev2][lev3] = state
            else:
                dpState[lev1][lev2] = {}
                dpState[lev1][lev2][lev3] = state
        else:
            dpState[lev1] = {}
            dpState[lev1][lev2] = {}
            dpState[lev1][lev2][lev3] = state
    else:  # save unchecked item
        if len(dpState) == 0:  # at launch
            return
        else:
            if lev1 in dpState:
                if lev2 in dpState[lev1]:
                    if lev3 in dpState[lev1][lev2]:
                        dpState[lev1][lev2][lev3] = state

    # refresh to remove turned-off keys
    # After refresh, there should be no False entry and all entries are True.

    # clear level 3
    for obj in dpState:
        for child in dpState[obj]:
            basedict = dpState[obj][child]
            for key, value in basedict.copy().items():
                if not value:  # value is False
                    basedict.pop(key)

    # clear level 2
    for obj in dpState:
        for key, value in dpState[obj].copy().items():
            if len(value) == 0:  # empty dictionary
                dpState[obj].pop(key)

    # clear level 1
    for key, value in dpState.copy().items():
        if len(value) == 0:  # empty dictionary
            dpState.pop(key)


def to_text_string(obj, encoding=None):
    """Convert `obj` to (unicode) text string"""
    if encoding is None:
        return str(obj)
    elif isinstance(obj, str):
        # In case this function is not used properly, this could happen
        return obj
    else:
        return str(obj, encoding)


def to_unicode_from_fs(string):
    """
    Return a unicode version of string decoded using the file system encoding.
    """
    if not is_string(string):  # string is a QString
        string = to_text_string(string.toUtf8(), 'utf-8')
    else:
        if isinstance(string, bytes):
            FS_ENCODING = get_file_system_encoding()
            try:
                unic = string.decode(FS_ENCODING)
            except (UnicodeError, TypeError):
                pass
            else:
                return unic
    return string


def is_string(obj):
    """Return True if `obj` is a text or binary Python string object,
    False if it is anything else, like a QString (Python 2, PyQt API #1)"""
    return isinstance(obj, str) or isinstance(obj, bytes)


# The default encoding for file paths and environment variables should be set
# to match the default encoding that the OS is using.
def get_file_system_encoding():
    """
    Query the filesystem for the encoding used to encode filenames
    and environment variables.
    """
    encoding = sys.getfilesystemencoding()
    if encoding is None:
        # Must be Linux or Unix and nl_langinfo(CODESET) failed.
        encoding = locale.getpreferredencoding()
    return encoding


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    """
    Returns the angle in radians between vectors 'v1' and 'v2':
        angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
        angle_between((1, 0, 0), (1, 0, 0))
            0.0
        angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def is_orthogonal(v1, v2, tolerance=0.1):
    a = angle_between(v1, v2) / np.pi * 180.0 - 90.0
    if abs(a) < tolerance:
        return True
    return False


def myprint(*args, **kwargs):
    """My custom print() function."""
    # TODO what about the kwargs?
    strArgs = [str(arg) for arg in args]
    text = ' '.join(strArgs)
    logger.info(text)


# Overload the print() is ok with Python, but not Cython.
# Cython.Compiler.Errors.CompileError
# def print(*args, **kwargs):
#     myprint(*args, **kwargs)


def split_array(array, byteLimit):
    size = array.shape[0]
    byte = array.nbytes
    if byte >= byteLimit:
        if byte % byteLimit == 0:
            nsplit = int(byte / byteLimit)
        else:
            nsplit = int(byte / byteLimit) + 1
        nvCellSize = int(size / nsplit)
        splitIndex = np.arange(nvCellSize, size, nvCellSize).tolist()
        splitArray = np.split(array, splitIndex)
    else:
        splitArray = [array]
    cellSize = [a.shape[0] for a in splitArray]
    cellByte = [a.nbytes for a in splitArray]
    assert sum(cellSize) == size, "Lost element in split"
    assert sum(cellByte) == byte, "Lost byte in split"
    if byte >= byteLimit:
        logger.info('input array size = {}'.format(size))
        logger.info('input array bytes = {}'.format(byte))
        logger.info('output arrays size = {}'.format(cellSize))
        logger.info('output arrays bytes = {}'.format(cellByte))
    return splitArray


def split_array_test():
    import sqlite3
    from ezcad.utils.sqlite_array import adapt_array, convert_array
    # Converts np.array to TEXT when inserting
    sqlite3.register_adapter(np.ndarray, adapt_array)
    # Converts TEXT to np.array when selecting
    sqlite3.register_converter("ARRAY", convert_array)

    SQLITE_LIMIT_LENGTH = 30 # test
    print('array byte limit =', SQLITE_LIMIT_LENGTH)

    n = 12
    x = np.arange(n, dtype='float32') # 1D array
#    x = np.arange(n*3, dtype='float32').reshape(n,3) # 2D array
    splitArray = split_array(x, SQLITE_LIMIT_LENGTH)

    object_name = 'mypoint'
    prop_name = 'vint'
    values = []
    for i in range(len(splitArray)):
        chunkArray = splitArray[i]
        value = (object_name, prop_name, i+1, chunkArray)
        values.append(value)

    con = sqlite3.connect("test.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    cur.execute("CREATE TABLE test (object_name TEXT, prop_name TEXT, \
        chunkID INTEGER, arr ARRAY, PRIMARY KEY (object_name, prop_name, chunkID))")
    cur.executemany("INSERT INTO test VALUES (?,?,?,?)", values)

    propID = (object_name, prop_name)
    cur.execute("SELECT chunkID, arr FROM test \
                WHERE object_name = ? AND prop_name = ?", propID)
    fetchData = cur.fetchall()
    print('fetch data type =', type(fetchData))
    print('fetch data length =', len(fetchData))

    for i in range(len(fetchData)):
        chunkID = fetchData[i][0]
        assert chunkID == (i+1), "Chunk order is wrong"

    chunkArrays = [d[1] for d in fetchData]
    out = np.concatenate(chunkArrays)
    print('retrieved array shape =', out.shape)
    print('retrieved array dtype =', out.dtype)
    print('retrieved array =', out)
