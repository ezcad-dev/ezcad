# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

"""
https://stackoverflow.com/questions/18621513/python-insert-numpy-array-into-sqlite3-database
"""

import sqlite3
import numpy as np
import io


def adapt_array(arr):
    """
    http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
    """
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())


def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)


def main():
    # Converts np.array to TEXT when inserting
    sqlite3.register_adapter(np.ndarray, adapt_array)

    # Converts TEXT to np.array when selecting
    sqlite3.register_converter("ARRAY", convert_array)

    # x = np.arange(12).reshape(2,6)
    x = np.zeros((10,10,20), dtype='float32')
    # x = np.zeros((100,1000,2000), dtype='float32')
    # OverflowError: BLOB longer than INT_MAX bytes
    # x = np.zeros((1000,1000,2000), dtype='float32')

    con = sqlite3.connect("debug.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    cur.execute("CREATE TABLE test (arr ARRAY)")

    # With this setup, you can simply insert the NumPy array with no change in syntax:
    cur.execute("INSERT INTO test (arr) VALUES (?)", (x,))

    # And retrieve the array directly from sqlite as a NumPy array:
    cur.execute("SELECT arr FROM test")
    data = cur.fetchone()[0]

    print(type(data))
    print(data.shape)
    print(data.dtype)


if __name__ == '__main__':
    main()
