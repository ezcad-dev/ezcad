# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

# Third party imports
from qtpy.QtCore import Qt, QSize, Signal
from qtpy.QtGui import QColor
from qtpy.QtWidgets import (QWidget, QHBoxLayout, QMessageBox, QVBoxLayout,
    QColorDialog)

import vispy as vp
from vispy import scene

# Local imports
from ezcad.utils.qthelpers import (create_plugin_layout, create_toolbutton,
    create_toolbutton_help)
from ezcad.utils import icon_manager as ima
from ezcad.utils.logger import logger
from ezcad.config.base import _
from ezcad.config.main import CONF

from ezcad.utils.functions import save_display_state
from ezcad.utils.copy_to_clipboard import copy_to_clipboard
from ezcad.widgets.dialogs import AspectRatioDialog, CanvasExportDialog


class VispyImage(QWidget):

    def __init__(self, parent=None, options_button=None, name=None):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.base = CanvasWidget(parent=self, name=name)

        btn_layout = QHBoxLayout()
        for btn in self.setup_buttons():
            btn.setIconSize(QSize(16, 16))
            btn_layout.addWidget(btn)
        if options_button:
            btn_layout.addStretch()
            btn_layout.addWidget(options_button, Qt.AlignRight)

        layout = create_plugin_layout(btn_layout, self.base)
        self.setLayout(layout)

    def setup_buttons(self):
        hide_all_btn = create_toolbutton(self,
            icon=ima.icon('hide_all'),
            tip=_('Hide all'),
            shortcut="Ctrl+L",
            triggered=self.base.hide_all)
        self.pick_btn = create_toolbutton(self,
            icon=ima.icon('pick_mode'),
            tip=_('Pick mode'), shortcut="P",
            toggled=self.base.toggle_pick_mode)
        color_btn = create_toolbutton(self,
            icon=ima.icon('bkgd_color'),
            tip=_('Background color'),
            triggered=self.base.set_background_color)
        export_btn = create_toolbutton(self,
            icon=ima.icon('photo'),
            tip=_('Export canvas to picture'),
            triggered=self.base.export_canvas)
        help_btn = create_toolbutton_help(self,
            triggered=self.show_help)
        return (hide_all_btn, self.pick_btn, color_btn, export_btn, help_btn)

    def show_help(self):
        QMessageBox.information(self, _('How to use'), self.base.HELP)


class CanvasWidget(QWidget):
    NAME = _('vispy image')
    HELP = _("<b>TODO</b> <br>")

    sig_hide_all = Signal()
    sigPickedImageIndex = Signal(tuple)

    def __init__(self, parent=None, name=None):
        super(CanvasWidget, self).__init__(parent=parent)
        self.parent = parent
        self.main = self.parent.parent.parent.main
        self.treebase = self.main.treebase
        self.database = self.main.database
        self.dpState = {}
        self.opts = None
        self.hasState = False
        self._name = name

        self.canvas = Canvas(parent=self, show=False)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.canvas.native)

        self.toggle_pick_mode(False)
        self.sigPickedImageIndex.connect(self.print_coord)
        #self.hasState = True # enable save viewer status
        self.canvas00 = self.canvas[0,0]
        self.view = self.canvas[0,0].view
        self.camera = self.canvas[0,0].view.camera
        
        # PanZoomCamera, by default, has its +y axis pointing upward
        # flip +y axis to make it point downward (depth axis)
        self.camera.flip = (False, True, False)
        
        self.aspect_method = "Auto"
        self.apply_aspect(self.aspect_method)

    def print_coord(self, point):
        logger.info("Mouse pressed at image index {}".format(point))
        self.dob.print_section_val(self.section_type, point)

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

    @property
    def aspect_ratio(self):
        return self.camera.aspect

    @aspect_ratio.setter
    def aspect_ratio(self, value):
        self.camera.aspect = value

    @property
    def state(self):
        """
        -o- state : dict, used for save viewer to database
        """
        state = {}
        state['aspect_method'] = self.aspect_method
        state['aspect_ratio'] = self.aspect_ratio
        state['bgcolor'] = self.bgcolor.rgba
        return state

    @state.setter
    def state(self, state):
        if 'aspect_method' in state:
            self.aspect_method = state['aspect_method']
        if 'aspect_ratio' in state:
            self.aspect_ratio = state['aspect_ratio']
        if 'bgcolor' in state:
            self.bgcolor = state['bgcolor']

    def add_item_agent(self, dob):
        logger.warning('{} can only display section'.format(self._name))
        return

    def add_item(self, item):
        # TODO signal tree uncheck the existing section?
        # TODO display 2+ images in this viewer...?
        self.clear() # remove existing item
        self.view.add(item)
        #self.view.camera.set_range()
        self.canvas.visuals.append(item)

    def remove_item_agent(self, dob):
        name = dob.name
        key = 'object'
        if name in self.dpState:
            if key in self.dpState[name]:
                if self.dpState[name][key]['self']:
                    logger.info('{} is removing {}'.format(self._name, name))
                    self.save_display_state(name, 'object', 'self', False)
                    self.clear()

    def clear(self):
        if len(self.canvas.visuals) > 0:
            self.canvas.visuals[0].parent = None
            self.canvas.visuals.pop(0)
        if len(self.canvas.visuals) != 0:
            raise ValueError("Image view is not empty")

    def add_cube_section(self, dob, section_name):
        self.dob = dob
        self.section_type = section_name[:5]
        parent = self._name
        if section_name[:5] in ['iline', 'xline', 'depth']:
            section_type = section_name[:5]
            if parent not in dob.section_image[section_type]:
                dob.plot_image_vs(section_type, parent=parent)
            image = dob.section_image[section_type][parent]
            xr, yr = dob.section_image_info[section_type]["range"]
            xlabel, ylabel = dob.section_image_info[section_type]["label"]
            section_name = section_type # for save display state
        else:
            section = dob.aline_section[section_name]
            if parent not in dob.aline_image[section_name]:
                dob.plot_aline_image(section, parent=parent)
            image = dob.aline_image[section_name][parent]
            xr, yr = section['info']['range']
            xlabel, ylabel = section['info']['label']
        self.add_item(image)
        self.camera.set_range(x=xr, y=yr)
        self.canvas00.xlabel.text = xlabel
        self.canvas00.ylabel.text = ylabel
        self.canvas00.xlabel._text_visual.font_size = 7
        self.canvas00.ylabel._text_visual.font_size = 7
        self.save_display_state(dob.name, 'sections', section_name, True)

    def remove_cube_section(self, dob, section_name):
        name = dob.name
        if name in self.dpState:
            if 'sections' in self.dpState[name]:
                if section_name in self.dpState[name]['sections']:
                    if self.dpState[name]['sections'][section_name]:
                        self.save_display_state(name, 'sections',
                            section_name, False)
                        self.clear()


# vispy/plot/fig.py
# vispy/plot/plotwidget.py
class Canvas(scene.SceneCanvas):
    def __init__(self, parent=None, bgcolor='w', size=(800, 600),
        show=True, **kwargs):
        self._plot_widgets = []
        self._grid = None  # initialize before the freeze occurs
        super(Canvas, self).__init__(bgcolor=bgcolor, keys='interactive',
             show=show, size=size, **kwargs)
        self._grid = self.central_widget.add_grid()
        self._grid._default_class = PlotWidget
        
        self.unfreeze()
        self.visuals = []
        self.pick_mode = False
        self.parent = parent
        self.freeze()

    @property
    def plot_widgets(self):
        """List of the associated PlotWidget instances"""
        return tuple(self._plot_widgets)

    def __getitem__(self, idxs):
        """Get an axis"""
        pw = self._grid.__getitem__(idxs)
        self._plot_widgets += [pw]
        return pw

    def on_mouse_press(self, event):
        if not self.pick_mode:
            return
        if len(self.visuals) == 0:
            return # canvas is empty

        # emit signal of coordinate of picked point
        vis = self.visuals[0]
        tr = self.scene.node_transform(vis)
        pos = tr.map(event.pos)
        xidx, yidx = pos[:2]
        self.parent.sigPickedImageIndex.emit((xidx, yidx))


class PlotWidget(scene.Widget):
    """This code is from Vispy and under the new BSD license."""
    def __init__(self, *args, **kwargs):
        self._fg = kwargs.pop('fg_color', 'k')
        self.grid = None
        self.camera = None
        self.title = None
        self.title_widget = None
        self.yaxis = None
        self.xaxis = None
        self.xlabel = None
        self.ylabel = None
        self._configured = False
        self.visuals = []
        self.section_y_x = None

        self.cbar_top = None
        self.cbar_bottom = None
        self.cbar_left = None
        self.cbar_right = None

        super(PlotWidget, self).__init__(*args, **kwargs)
        self.grid = self.add_grid(spacing=0, margin=10)

        self.title = scene.Label("", font_size=16, color="#ff0000")
        self._configure_2d()

    def _configure_2d(self, fg_color=None):
        if self._configured:
            return

        if fg_color is None:
            fg = self._fg
        else:
            fg = fg_color

        #     c0        c1      c2      c3      c4      c5         c6
        #  r0 +---------+-------+-------+-------+-------+---------+---------+
        #     |         |                       | title |         |         |
        #  r1 |         +-----------------------+-------+---------+         |
        #     |         |                       | cbar  |         |         |
        #  r2 |         +-------+-------+-------+-------+---------+         |
        #     |         | cbar  | ylabel| yaxis |  view | cbar    | padding |
        #  r3 | padding +-------+-------+-------+-------+---------+         |
        #     |         |                       | xaxis |         |         |
        #  r4 |         +-----------------------+-------+---------+         |
        #     |         |                       | xlabel|         |         |
        #  r5 |         +-----------------------+-------+---------+         |
        #     |         |                       | cbar  |         |         |
        #  r6 |---------+-----------------------+-------+---------+---------|
        #     |                           padding                           |
        #     +---------+-----------------------+-------+---------+---------+

        default = False
        get_func = CONF.get_default if default else CONF.get
        section = 'image_viewer'
        padding_left_width = get_func(section, 'padding_left_width')
        padding_right_width = get_func(section, 'padding_right_width')
        padding_bottom_height = get_func(section, 'padding_bottom_height')
        cbar_top_height = get_func(section, 'cbar_top_height')
        cbar_bottom_height = get_func(section, 'cbar_bottom_height')
        cbar_left_width = get_func(section, 'cbar_left_width')
        cbar_right_width = get_func(section, 'cbar_right_width')
        title_widget_height = get_func(section, 'title_widget_height')
        xlabel_widget_height = get_func(section, 'xlabel_widget_height')
        ylabel_widget_width = get_func(section, 'ylabel_widget_width')
        xaxis_widget_height = get_func(section, 'xaxis_widget_height')
        yaxis_widget_width = get_func(section, 'yaxis_widget_width')

        # padding left
        padding_left = self.grid.add_widget(None, row=0, row_span=5, col=0)
        padding_left.width_min = padding_left_width[0]
        padding_left.width_max = padding_left_width[1]

        # padding right
        padding_right = self.grid.add_widget(None, row=0, row_span=5, col=6)
        padding_right.width_min = padding_right_width[0]
        padding_right.width_max = padding_right_width[1]

        # padding right
        padding_bottom = self.grid.add_widget(None, row=6, col=0, col_span=6)
        padding_bottom.height_min = padding_bottom_height[0]
        padding_bottom.height_max = padding_bottom_height[1]

        # row 0
        # title - column 4 to 5
        self.title_widget = self.grid.add_widget(self.title, row=0, col=4)
        self.title_widget.height_min = title_widget_height[0]
        self.title_widget.height_max = title_widget_height[1]

        # row 1
        # colorbar - column 4 to 5
        self.cbar_top = self.grid.add_widget(None, row=1, col=4)
        self.cbar_top.height_max = cbar_top_height[1]

        # row 2, xlabel
        # xlabel - column 4
        self.xlabel = scene.Label("xlabel")
        xlabel_widget = self.grid.add_widget(self.xlabel, row=2, col=4)
        xlabel_widget.height_min = xlabel_widget_height[0]
        xlabel_widget.height_max = xlabel_widget_height[1]

        # row 3, xaxis

        # row 4
        # colorbar_left - column 1
        # ylabel - column 2
        # yaxis - column 3
        # view - column 4
        # colorbar_right - column 5
        self.cbar_left = self.grid.add_widget(None, row=4, col=1)
        self.cbar_left.width_max = cbar_left_width[1]

        self.ylabel = scene.Label("ylabel", rotation=-90)
        ylabel_widget = self.grid.add_widget(self.ylabel, row=4, col=2)
        ylabel_widget.width_min = ylabel_widget_width[0]
        ylabel_widget.width_max = ylabel_widget_width[1]

        self.yaxis = scene.AxisWidget(orientation='left',
                                      text_color=fg,
                                      axis_color=fg, tick_color=fg)

        yaxis_widget = self.grid.add_widget(self.yaxis, row=4, col=3)
        yaxis_widget.width_min = yaxis_widget_width[0]
        yaxis_widget.width_max = yaxis_widget_width[0]

        self.view = self.grid.add_view(row=4, col=4,
                                       border_color='grey', bgcolor="#efefef")
        self.view.camera = 'panzoom'
        self.camera = self.view.camera

        self.cbar_right = self.grid.add_widget(None, row=4, col=5)
        self.cbar_right.width_max = cbar_right_width[1]

        # row 3
        # xaxis - column 4
        self.xaxis = scene.AxisWidget(orientation='top', text_color=fg,
                                      axis_color=fg, tick_color=fg)
        xaxis_widget = self.grid.add_widget(self.xaxis, row=3, col=4)
        xaxis_widget.height_min = xaxis_widget_height[0]
        xaxis_widget.height_max = xaxis_widget_height[1]

        # row 4
        # xlabel - column 4
#        self.xlabel = scene.Label("xlabel")
#        xlabel_widget = self.grid.add_widget(self.xlabel, row=4, col=4)
#        xlabel_widget.height_min = 20
#        xlabel_widget.height_max = 40

        # row 5
        self.cbar_bottom = self.grid.add_widget(None, row=5, col=4)
        self.cbar_bottom.height_max = cbar_bottom_height[1]

        self._configured = True
        self.xaxis.link_view(self.view)
        self.yaxis.link_view(self.view)
