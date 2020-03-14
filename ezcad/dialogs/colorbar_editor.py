# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
"""
"""

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (QLabel, QLineEdit, QRadioButton,
    QSplitter, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QSlider)

from ezcad.config.base import _
from ezcad.widgets.ezdialog import EasyDialog
from ezcad.utils.logger import logger
from ezcad.utils.colorbar_gradients import Gradients as customGradients
from ezcad.utils.plotting import set_gradient_alpha
from ezcad.widgets.histogram_lut_widget import HistogramLUTWidget


class ColorbarEditor(EasyDialog):
    NAME = _("Colorbar editor")
    HELP_BODY = _("Click a triangle to change its color. <br>"
    "Drag triangles to move. <br>"
    "Click in an empty area to add a new color. <br>"
    "Right click a triangle to remove. <br>"
    "Right click axis or region, click View All, to zoom. <br>"
    "Mouse wheel zoom in/out when cursor on axis or region. <br>"
    "After zoom out, drag the region to move along the axis. <br>"
    "Right click the colorbar to select different colormap. <br>"
    "One of the four bars can be enabled by set Orientation. <br>"
    "The bar widgets can be resized by the move the splitter. <br>")

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent=parent, set_tree=True, set_db=True)

        self.dob = None
        self.clip_min = 0
        self.clip_max = 1
        self.setup_page()

    def setup_page(self):
        vbox = QVBoxLayout()
        btnWidget = QWidget(self)
        btnWidget.setLayout(vbox)

        text = _("Object")
        geom = ['Point', 'Line', 'Tsurface', 'Gsurface', 'Cube']
        self.grabob = self.create_grabob(text, geom=geom)
        vbox.addWidget(self.grabob)

        text = _("Property")
        self.prop = self.create_combobox(text)

        btn_load_property = QPushButton(_('Load'))
        btn_load_property.clicked.connect(self.load_property)
        hbox = QHBoxLayout()
        hbox.addWidget(self.prop)
        hbox.addWidget(btn_load_property)
        vbox.addLayout(hbox)

        lbl_orientation = QLabel(_('Orientation'))
        rb_top = QRadioButton('Top')
        rb_bottom = QRadioButton('Bottom')
        rb_left = QRadioButton('Left')
        rb_right = QRadioButton('Right')
        hbox = QHBoxLayout()
        hbox.addWidget(lbl_orientation)
        hbox.addWidget(rb_top)
        hbox.addWidget(rb_bottom)
        hbox.addWidget(rb_left)
        hbox.addWidget(rb_right)
        vbox.addLayout(hbox)

        lbl_clip_min = QLabel(_('Clip minimum'))
        lbl_clip_max = QLabel(_('Clip maximum'))
        self.le_clip_min = QLineEdit('0')
        self.le_clip_max = QLineEdit('1')
        hbox = QHBoxLayout()
        hbox.addWidget(lbl_clip_min)
        hbox.addWidget(self.le_clip_min)
        hbox.addWidget(lbl_clip_max)
        hbox.addWidget(self.le_clip_max)
        vbox.addLayout(hbox)

        opacity = QLabel(_('Opacity'))
        self.opacity = QSlider(Qt.Horizontal)
        self.opacity.setTracking(False)
        self.opacity.setTickPosition(QSlider.TicksBelow)
        self.opacity.setSingleStep(1)
        self.opacity.setRange(0, 255)
        self.opacity.setValue(255)
        self.opacity.valueChanged.connect(self.opacity_changed)
        hbox = QHBoxLayout()
        hbox.addWidget(opacity)
        hbox.addWidget(self.opacity)
        vbox.addLayout(hbox)

        action = self.create_action()
        vbox.addWidget(action)

        hlut_right = HistogramLUTWidget(orientation='right',
                                        gradients=customGradients)
        hlut_left = HistogramLUTWidget(orientation='left',
                                       gradients=customGradients)
        hlut_bottom = HistogramLUTWidget(orientation='bottom',
                                         gradients=customGradients)
        hlut_top = HistogramLUTWidget(orientation='top',
                                      gradients=customGradients)
        lbl_hlut_help = QLabel("You can activate any one of the four.")

        split1 = QSplitter(Qt.Vertical)
        split1.addWidget(hlut_top)
        split1.addWidget(lbl_hlut_help)
        split1.addWidget(hlut_bottom)
        # split1.setStretchFactor(0, 0)
        # split1.setStretchFactor(1, 1)
        # split1.setStretchFactor(2, 0)
        # split1.setSizes([50, 400, 50])

        split2 = QSplitter(Qt.Horizontal)
        split2.addWidget(hlut_left)
        split2.addWidget(split1)
        split2.addWidget(hlut_right)

        split3 = QSplitter(Qt.Vertical)
        split3.addWidget(btnWidget)
        split3.addWidget(split2)
        self.layout.addWidget(split3)

        # self.le_clip_min.editingFinished.connect(self.clip_changed)
        # self.le_clip_max.editingFinished.connect(self.clip_changed)

        self.hlut_list = [hlut_top, hlut_bottom, hlut_left, hlut_right]

        rb_top.toggled.connect(lambda:self.set_orientation(rb_top))
        rb_bottom.toggled.connect(lambda:self.set_orientation(rb_bottom))
        rb_left.toggled.connect(lambda:self.set_orientation(rb_left))
        rb_right.toggled.connect(lambda:self.set_orientation(rb_right))
        rb_right.setChecked(True)

    def opacity_changed(self):
        """
        Potentially can use non-constant opacity e.g. user can define
        any opacity gradient, linear interpolate on the color gradient
        ticks and set Alpha in the RGBA.
        """
        opacity = self.opacity.value()
        gradient = self.hlut_active.gradient.saveState()
        set_gradient_alpha(gradient, opacity)
        prop_name = self.prop_name
        self.dob.set_gradient(prop_name, gradient)
        self.dob.make_colormap(prop_name)
        self.dob.update_plots_by_prop()

    def set_orientation(self, rb):
        if rb.isChecked():
            if rb.text() == "Top":
                index = 0
            elif rb.text() == "Bottom":
                index = 1
            elif rb.text() == "Left":
                index = 2
            elif rb.text() == "Right":
                index = 3
            else:
                raise ValueError("Unknown value")

            self.hlut_active = self.hlut_list[index]
            self.hlut_active.setEnabled(True)
            for i in range(len(self.hlut_list)):
                if i != index:
                    self.hlut_list[i].setEnabled(False)

            self.hlut_active.sigLevelChangeFinished.connect(self.level_changed)
            self.hlut_active.sigLevelChangeFinished.connect(self.apply)
            # self.hlut_active.sigLookupTableChanged.connect(self.apply)

            if self.dob is not None:
                self.load_hlut()

    def level_changed(self):
        """
        Level is changed in the hlut by mouse dragging, now sync textbox.
        """
        self.clip_min, self.clip_max = self.hlut_active.getLevels()
        self.le_clip_min.setText(str(self.clip_min))
        self.le_clip_max.setText(str(self.clip_max))

    def clip_changed(self):
        """
        Clip is changed in the textbox by user typing, now sync hlut.
        """
        self.clip_min = float(self.le_clip_min.text())
        self.clip_max = float(self.le_clip_max.text())
        self.hlut_active.setLevels(self.clip_min, self.clip_max)

    def apply(self):
        if self.dob is None:
            logger.warning('No data object is loaded yet')
            return
        self.clip_changed()
        prop_name = self.prop_name
        # save to dob for updating plots of the object
        clip = self.hlut_active.getLevels()
        self.dob.set_clip(prop_name, clip)
        # save the colorbar/gradient as a dictionary
        gradient = self.hlut_active.gradient.saveState()
        opacity = self.opacity.value()
        set_gradient_alpha(gradient, opacity)
        self.dob.set_gradient(prop_name, gradient)
        self.dob.make_colormap(prop_name)
        self.dob.update_plots_by_prop()

        # TODO handle points multiple properties

    def grab_object_rc(self):
        """ Used when dialog is brought up by right click in tree. """
        geom = ['Point', 'Line', 'Tsurface', 'Gsurface', 'Cube']
        self.dob = self.treebase.grab_object(geom)
        self.grabob.lineedit.edit.setText(self.dob.name)
        self.propList = list(self.dob.prop.keys())
        self.prop.combobox.clear()
        self.prop.combobox.addItems(self.propList)
        self.grab_property()

    def load_object(self):
        self.dob = self.object  # from EasyDialog grab_object
        self.propList = list(self.dob.prop.keys())
        self.prop.combobox.clear()
        self.prop.combobox.addItems(self.propList)
        self.grab_property()

    def grab_property(self):
        prop_name = self.dob.current_property
        index = self.propList.index(prop_name)
        self.prop.combobox.setCurrentIndex(index)

    def load_property(self):
        """
        """
        object_name = self.grabob.lineedit.edit.text()
        self.prop_name = self.prop.combobox.currentText()
        self.dob = self.database[object_name]
        self.load_hlut()

    def load_hlut(self):
        prop_name = self.prop_name
        cg = self.dob.prop[prop_name]['colorGradient']
        if cg is not None:
            self.hlut_active.gradient.restoreState(cg)

        self.clip_min, self.clip_max = self.dob.prop[prop_name]['colorClip']
        self.hlut_active.setLevels(self.clip_min, self.clip_max)

        # Assume constant alpha, so use the first value
        alpha = cg['ticks'][0][1][3]
        self.opacity.setValue(alpha)


def main():
    from qtpy.QtWidgets import QApplication
    app = QApplication([])
    test = ColorbarEditor()
    test.show()
    app.exec_()


if __name__ == '__main__':
    main()
