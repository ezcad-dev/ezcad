# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
"""
Vispy canvas base, to be inherited by vs1d, vs2d, vs3d viewers.
"""

from qtpy.QtCore import Signal, Qt
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QWidget, QVBoxLayout, QColorDialog
import numpy as np
import vispy as vp
import vispy.plot as vpp

from ezcad.config.base import _
from ezcad.utils.logger import logger
from ezcad.utils.functions import save_display_state
from ezcad.utils.copy_to_clipboard import copy_to_clipboard
from ezcad.widgets.dialogs import AspectRatioDialog, CanvasExportDialog
from ezcad.utils.convert_grid import xy2ln


def display_selection(fig, selected, pos):
    """
    -i- fig : vispy fig
    -i- selected : vispy visual
    -i- pos : list, [x,y] pixel position of event
    """
    logger.info("Mouse pressed at pixel ({}, {})".format(pos[0], pos[1]))
    # Range of pixels to detect selected data
    posMin = [x-5 for x in pos] # 5 pixels range
    posMax = [x+5 for x in pos]
    # map the mouse position to data coordinates
    tr = fig.scene.node_transform(selected)
    pos = tr.map(pos)
    posMin = tr.map(posMin)
    posMax = tr.map(posMax)
    # handle y+ axis pointing downward
    xMin = min(posMin[0], posMax[0])
    xMax = max(posMin[0], posMax[0])
    yMin = min(posMin[1], posMax[1])
    yMax = max(posMin[1], posMax[1])
    logger.info("Clicked at {}".format(pos)) # [x,y,z,mb]
    logger.info("Object name: {}".format(selected.name))
    if not hasattr(selected, 'vertexes'):
        return
    index = np.where((selected.vertexes['xyz'][:,0] >= xMin) &
                     (selected.vertexes['xyz'][:,0] <= xMax) &
                     (selected.vertexes['xyz'][:,1] >= yMin) &
                     (selected.vertexes['xyz'][:,1] <= yMax))
    if len(index[0]) >= 1: # index is tuple (array,)
        index = index[0][0]
    logger.info("Data index = {}".format(index))
    for prop_name in sorted(selected.prop):
        prop = selected.prop[prop_name]
        array = prop['array1d']
        logger.info("{} = {}".format(prop_name, array[index]))


class VispyCanvas(QWidget):
    sig_hide_all = Signal()
    sigPickedPoint = Signal(tuple)
    NAME = _('vispy canvas')
    HELP = _("TODO")

    def __init__(self, parent=None, name=None):
        super(VispyCanvas, self).__init__(parent=parent)
        self.parent = parent
        self.main = self.parent.parent.parent.main
        self.treebase = self.main.treebase
        self.database = self.main.database
        self.dpState = {}
        self.opts = None
        self.hasState = False
        self._name = name

        self.canvas = vpp.Fig(show=False)
        self.canvas00 = self.canvas[0, 0]
        self.canvas.unfreeze()
        self.canvas.visuals = []
        self.canvas.pick_mode = False
        self.canvas.sigPickedPoint = self.sigPickedPoint
        self.canvas.freeze()
        self.toggle_pick_mode(False)
        self.sigPickedPoint.connect(self.print_coord)

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas.native)
        self.setLayout(vbox)

        @self.canvas.connect
        def on_mouse_press(event):
            if not self.canvas.pick_mode:
                return
            if len(self.canvas.visuals) == 0:
                return # canvas is empty

            #if event.handled or event.button != 1:
            #    return
            if event.button == 2:
                queried = None
                for v in self.canvas.visuals_at(event.pos):
                    if isinstance(v, vp.scene.widgets.viewbox.ViewBox):
                        continue
                    queried = v
                    break
                if queried is not None:
                    logger.info("Object name {}".format(queried.name))
                return

            # emit signal of coordinate of picked point
            vis = self.canvas.visuals[0]
            tr = self.canvas.scene.node_transform(vis)
            pos = tr.map(event.pos)
            x, y, z = pos[:3]
            xy = np.array([x, y])
            survey = self.treebase.survey
            if survey is None:
                ilno, xlno = (0, 0)
            else:
                ilno, xlno = xy2ln(xy, survey=survey)
            self.canvas.sigPickedPoint.emit((ilno, xlno, x, y, z))

            selected = None
            for v in self.canvas.visuals_at(event.pos):
                if isinstance(v, vp.scene.widgets.viewbox.ViewBox):
                    continue
                selected = v
                break
            if selected is not None:
                display_selection(self.canvas, selected, event.pos)

    def print_coord(self, point):
        logger.info("Mouse pressed at coordinate {}".format(point))

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        
    @property
    def bgcolor(self):
        return self.view._bgcolor

    @bgcolor.setter
    def bgcolor(self, value):
        self.view.bgcolor = value
        
    def remove_item(self, item):
        item.parent = None
        if item in self.canvas.visuals:
            self.canvas.visuals.remove(item)

    def save_display_state(self, *args):
        save_display_state(self.dpState, *args)

    def add_item_prop(self, dob, prop):
        self.save_display_state(dob.name, 'properties', prop, True)

    def remove_item_prop(self, dob, prop):
        self.save_display_state(dob.name, 'properties', prop, False)

    def add_cube_section(self, dob, section):
        pass

    def remove_cube_section(self, dob, section):
        pass

    def set_background_color(self):
        r, g, b, a = self.bgcolor.RGBA
        oldColor = QColor(r, g, b, a)
        newColor = QColorDialog.getColor(oldColor)
        color = newColor.getRgbF()
        self.bgcolor = color

    def export_canvas(self):
        dialog = CanvasExportDialog(self)
        dialog.sig_start.connect(self.export_canvas_worker)
        dialog.show()

    def export_canvas_worker(self, fn, copy2clipboard):
        img = self.canvas.render()
        # If not full directory path, the relative path starts from CWD.
        logger.info("Save picture to {}".format(fn))
        vp.io.write_png(fn, img)
        if copy2clipboard:
            copy_to_clipboard(fn)

    def hide_all(self):
        # Uncheck all items in the data explorer tree
        self.sig_hide_all.emit()

    def clear(self):
        pass

    def clear_all(self):
        """
        This method is slot for signal of tree.sig_unchecked_all, which
        is emitted after the data tree has unchecked all items, and force
        clear the viewer.
        """
        # Remove all items from the ViewBox
        self.clear()
        self.dpState = {}

    def set_aspect(self, state=None):
        """
        The kwargs allow call by API in addition to GUI.
        """
        if state is None or state is False:  # set via GUI
            dialog = AspectRatioDialog(self)
            dialog.load_state(self.state)
            dialog.show()
            dialog.sigApply.connect(self.apply_aspect)
        else:
            # self.state = state
            method = state['aspect_method']
            ratio = state['aspect_ratio']
            self.apply_aspect(method, ratio)

    def apply_aspect(self, method, ratio=1.0):
        if method == 'Auto':
            r = None
        elif method == 'Equal':
            r = 1.0
        elif method == 'Fixed':
            r = ratio
        else:
            logger.error('Unknown value')
        self.aspect_method = method
        self.aspect_ratio = r

    def toggle_pick_mode(self, checked):
        if checked:
            self.canvas.pick_mode = True
            self.setCursor(Qt.ArrowCursor)
        else:
            self.canvas.pick_mode = False
            self.setCursor(Qt.OpenHandCursor)
