# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

from functools import partial
import numpy as np
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (QLabel, QTableWidget, QTableWidgetItem,
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton)
from ezcad.config.base import _


def add_array_percentile(prop):
    """
    -i- prop : dict, for example cube.prop[prop]
    """
    if 'array1d' in prop:
        data = prop['array1d']
    elif 'array2d' in prop:
        data = prop['array2d']
    elif 'array3d' in prop:
        data = prop['array3d']
    else:
        raise ValueError("Unknown value")
    ps = [0, 10, 50, 90, 100]
    vs = []
    for p in ps:
        vs.append(np.percentile(data, p))
    prop['arrayPercentiles'] = vs


def PropertyDistribtionTable(dict_prop):
    """
    -i- dict_prop : dictionary, properties.
    -o- table : QTableWidget, for use in PyQt GUI.
    Return a table widget of properties data value distribution.
    """
    props = [prop for prop in dict_prop]
    nrow = len(props)
    columnNames = ['Name', 'Min', 'P10', 'P50', 'P90', 'Max']
    ncol = len(columnNames)
    table = QTableWidget()
    table.setRowCount(nrow)
    table.setColumnCount(ncol)
    table.setHorizontalHeaderLabels(columnNames)
    key = 'arrayPercentiles'
    for i in range(nrow):
        prop = props[i]
        if not key in dict_prop[prop]:
            add_array_percentile(dict_prop[prop])
        p0, p10, p50, p90, p100 = dict_prop[prop][key]
        state = [prop, p0, p10, p50, p90, p100]
        state = [str(a) for a in state]  # convert to string
        for j in range(ncol):
            table.setItem(i, j, QTableWidgetItem(state[j]))
    table.sortItems(0, Qt.AscendingOrder)
    return table


def refresh(table, dict_prop):
    props = [prop for prop in dict_prop]
    nrow = len(props)
    columnNames = ['Name', 'Min', 'P10', 'P50', 'P90', 'Max']
    ncol = len(columnNames)
    table.setRowCount(nrow)
    table.setColumnCount(ncol)
    table.setHorizontalHeaderLabels(columnNames)
    key = 'arrayPercentiles'
    for i in range(nrow):
        prop = props[i]
        add_array_percentile(dict_prop[prop])
        p0, p10, p50, p90, p100 = dict_prop[prop][key]
        state = [prop, p0, p10, p50, p90, p100]
        state = [str(a) for a in state]  # convert to string
        for j in range(ncol):
            table.setItem(i, j, QTableWidgetItem(state[j]))
    table.sortItems(0, Qt.AscendingOrder)


def dict_prop_table(dict_prop):
    """ table with label """
    tableName = _("Property value distribution")
    label = QLabel(tableName)
    btn_refresh = QPushButton(_('Refresh'))
    table = PropertyDistribtionTable(dict_prop)
    btn_refresh.clicked.connect(partial(refresh, table, dict_prop))
    hbox = QHBoxLayout()
    hbox.addWidget(label)
    hbox.addWidget(btn_refresh)
    widget = QWidget()
    layout = QVBoxLayout()
    layout.addLayout(hbox)
    layout.addWidget(table)
    widget.setLayout(layout)
    return widget
