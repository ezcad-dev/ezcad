# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

from qtpy.QtCore import Qt, Signal
from qtpy.QtWidgets import QDoubleSpinBox, QHBoxLayout, QLabel, QSlider
from ezcad.config.base import _
from ezcad.widgets.ezdialog import EasyDialog


class DoubleSlider(QSlider):

    # create our our signal that we can connect to if necessary
    doubleValueChanged = Signal(float)

    def __init__(self, *args, **kargs):
        super(DoubleSlider, self).__init__( *args, **kargs)
        self.setDecimals()
        self.valueChanged.connect(self.emitDoubleValueChanged)

    def setDecimals(self, decimals=3):
        self._multi = 10 ** decimals

    def emitDoubleValueChanged(self):
        value = float(super(DoubleSlider, self).value())/self._multi
        self.doubleValueChanged.emit(value)

    def value(self):
        return float(super(DoubleSlider, self).value()) / self._multi

    def setMinimum(self, value):
        return super(DoubleSlider, self).setMinimum(value * self._multi)

    def setMaximum(self, value):
        return super(DoubleSlider, self).setMaximum(value * self._multi)

    def setRange(self, minValue, maxValue):
        self.setMinimum(minValue)
        self.setMaximum(maxValue)

    def setTickInterval(self, ti):
        super(DoubleSlider, self).setTickInterval(int(ti * self._multi))

    def setSingleStep(self, value):
        return super(DoubleSlider, self).setSingleStep(value * self._multi)

    def singleStep(self):
        return float(super(DoubleSlider, self).singleStep()) / self._multi

    def setValue(self, value):
        super(DoubleSlider, self).setValue(int(value * self._multi))


class Dialog(EasyDialog):
    NAME = _("Camera operator")
    HELP_BODY = _("Work for the vispy 3D viewer.<br>")

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent)
        if parent is not None:
            mainwindow = parent.main # parent is treebase
            self.camera = mainwindow.current_viewer
        self.setup_page()

    def setup_page(self):
        lblAzimuth = QLabel(_('Azimuth'))
        # self.sldAzimuth = QSlider(Qt.Horizontal) # only takes integer
        self.sldAzimuth = DoubleSlider(Qt.Horizontal)
        self.spAzimuth = QDoubleSpinBox()
        hbox = QHBoxLayout()
        hbox.addWidget(lblAzimuth)
        hbox.addWidget(self.sldAzimuth)
        hbox.addWidget(self.spAzimuth)
        self.layout.addLayout(hbox)

        lblElevation = QLabel(_('Elevation'))
        self.sldElevation = DoubleSlider(Qt.Horizontal)
        self.spElevation = QDoubleSpinBox()
        hbox = QHBoxLayout()
        hbox.addWidget(lblElevation)
        hbox.addWidget(self.sldElevation)
        hbox.addWidget(self.spElevation)
        self.layout.addLayout(hbox)

        lblFov = QLabel(_('Fov'))
        self.sldFov = DoubleSlider(Qt.Horizontal)
        self.spFov = QDoubleSpinBox()
        hbox = QHBoxLayout()
        hbox.addWidget(lblFov)
        hbox.addWidget(self.sldFov)
        hbox.addWidget(self.spFov)
        self.layout.addLayout(hbox)

        lblDistance = QLabel(_('Distance'))
        self.sldDistance = DoubleSlider(Qt.Horizontal)
        self.spDistance = QDoubleSpinBox()
        hbox = QHBoxLayout()
        hbox.addWidget(lblDistance)
        hbox.addWidget(self.sldDistance)
        hbox.addWidget(self.spDistance)
        self.layout.addLayout(hbox)

        lblCenterX = QLabel(_('CenterX'))
        self.sldCenterX = DoubleSlider(Qt.Horizontal)
        self.spCenterX = QDoubleSpinBox()
        hbox = QHBoxLayout()
        hbox.addWidget(lblCenterX)
        hbox.addWidget(self.sldCenterX)
        hbox.addWidget(self.spCenterX)
        self.layout.addLayout(hbox)

        lblCenterY = QLabel(_('CenterY'))
        self.sldCenterY = DoubleSlider(Qt.Horizontal)
        self.spCenterY = QDoubleSpinBox()
        hbox = QHBoxLayout()
        hbox.addWidget(lblCenterY)
        hbox.addWidget(self.sldCenterY)
        hbox.addWidget(self.spCenterY)
        self.layout.addLayout(hbox)

        lblCenterZ = QLabel(_('CenterZ'))
        self.sldCenterZ = DoubleSlider(Qt.Horizontal)
        self.spCenterZ = QDoubleSpinBox()
        hbox = QHBoxLayout()
        hbox.addWidget(lblCenterZ)
        hbox.addWidget(self.sldCenterZ)
        hbox.addWidget(self.spCenterZ)
        self.layout.addLayout(hbox)

        action = self.create_action(ok=False, apply_label='Load')
        self.layout.addWidget(action)

        vmin, vmax, step = 0, 360, 0.1
        self.sldAzimuth.setDecimals(1)
        self.sldAzimuth.setRange(vmin, vmax)
        self.sldAzimuth.setTickInterval(30)
        self.sldAzimuth.setTracking(False)
        self.sldAzimuth.setTickPosition(DoubleSlider.TicksBelow)
        self.sldAzimuth.setSingleStep(step)
        self.sldAzimuth.doubleValueChanged.connect(
            self.slider_value_changed_azimuth)
        self.spAzimuth.setRange(vmin, vmax)
        self.spAzimuth.setSingleStep(step)
        self.spAzimuth.editingFinished.connect(
            self.spinbox_editing_finished_azimuth)

        vmin, vmax, step = 0, 360, 0.1
        self.sldElevation.setDecimals(1)
        self.sldElevation.setRange(vmin, vmax)
        self.sldElevation.setTickInterval(30)
        self.sldElevation.setTracking(False)
        self.sldElevation.setTickPosition(DoubleSlider.TicksBelow)
        self.sldElevation.setSingleStep(step)
        self.sldElevation.doubleValueChanged.connect(
            self.slider_value_changed_elevation)
        self.spElevation.setRange(vmin, vmax)
        self.spElevation.setSingleStep(step)
        self.spElevation.editingFinished.connect(
            self.spinbox_editing_finished_elevation)

        vmin, vmax, step = 1, 90, 1
        self.sldFov.setDecimals(1)
        self.sldFov.setRange(vmin, vmax)
        self.sldFov.setTickInterval(30)
        self.sldFov.setTracking(False)
        self.sldFov.setTickPosition(DoubleSlider.TicksBelow)
        self.sldFov.setSingleStep(step)
        self.sldFov.doubleValueChanged.connect(
            self.slider_value_changed_fov)
        self.spFov.setRange(vmin, vmax)
        self.spFov.setSingleStep(step)
        self.spFov.editingFinished.connect(
            self.spinbox_editing_finished_fov)

        vmin, vmax, step =0, 1000000, 10000
        ti = (vmax - vmin) / 10
        self.sldDistance.setDecimals(0)
        self.sldDistance.setRange(vmin, vmax)
        self.sldDistance.setTickInterval(ti)
        self.sldDistance.setTracking(False)
        self.sldDistance.setTickPosition(DoubleSlider.TicksBelow)
        self.sldDistance.setSingleStep(step)
        self.sldDistance.doubleValueChanged.connect(
            self.slider_value_changed_distance)
        self.spDistance.setRange(vmin, vmax)
        self.spDistance.setSingleStep(step)
        self.spDistance.editingFinished.connect(
            self.spinbox_editing_finished_distance)

        vmin, vmax, step = -1000000, 1000000, 10000
        ti = (vmax - vmin) / 10
        self.sldCenterX.setDecimals(0)
        self.sldCenterX.setRange(vmin, vmax)
        self.sldCenterX.setTickInterval(ti)
        self.sldCenterX.setTracking(False)
        self.sldCenterX.setTickPosition(DoubleSlider.TicksBelow)
        self.sldCenterX.setSingleStep(step)
        self.sldCenterX.doubleValueChanged.connect(
            self.slider_value_changed_centerx)
        self.spCenterX.setRange(vmin, vmax)
        self.spCenterX.setSingleStep(step)
        self.spCenterX.editingFinished.connect(
            self.spinbox_editing_finished_centerx)

        vmin, vmax, step = -1000000, 1000000, 10000
        ti = (vmax - vmin) / 10
        self.sldCenterY.setDecimals(0)
        self.sldCenterY.setRange(vmin, vmax)
        self.sldCenterY.setTickInterval(ti)
        self.sldCenterY.setTracking(False)
        self.sldCenterY.setTickPosition(DoubleSlider.TicksBelow)
        self.sldCenterY.setSingleStep(step)
        self.sldCenterY.doubleValueChanged.connect(
            self.slider_value_changed_centery)
        self.spCenterY.setRange(vmin, vmax)
        self.spCenterY.setSingleStep(step)
        self.spCenterY.editingFinished.connect(
            self.spinbox_editing_finished_centery)

        vmin, vmax, step = -1000000, 1000000, 10000
        ti = (vmax - vmin) / 10
        self.sldCenterZ.setDecimals(0)
        self.sldCenterZ.setRange(vmin, vmax)
        self.sldCenterZ.setTickInterval(ti)
        self.sldCenterZ.setTracking(False)
        self.sldCenterZ.setTickPosition(DoubleSlider.TicksBelow)
        self.sldCenterZ.setSingleStep(step)
        self.sldCenterZ.doubleValueChanged.connect(
            self.slider_value_changed_centerz)
        self.spCenterZ.setRange(vmin, vmax)
        self.spCenterZ.setSingleStep(step)
        self.spCenterZ.editingFinished.connect(
            self.spinbox_editing_finished_centerz)

    def apply(self):
        self.load_from_viewer()

    def slider_value_changed_azimuth(self, sliderValue):
        """
        """
        self.spAzimuth.setValue(sliderValue) # sync spinbox
        self.camera.azimuth = sliderValue

    def spinbox_editing_finished_azimuth(self):
        """
        """
        azimuth = self.spAzimuth.value()
        self.sldAzimuth.setValue(azimuth) # sync slider
        self.camera.azimuth = azimuth

    def slider_value_changed_elevation(self, sliderValue):
        """
        """
        self.spElevation.setValue(sliderValue) # sync spinbox
        self.camera.elevation = sliderValue

    def spinbox_editing_finished_elevation(self):
        """
        """
        elevation = self.spElevation.value()
        self.sldElevation.setValue(elevation) # sync slider
        self.camera.elevation = elevation

    def slider_value_changed_fov(self, sliderValue):
        """
        """
        self.spFov.setValue(sliderValue) # sync spinbox
        self.camera.fov = sliderValue

    def spinbox_editing_finished_fov(self):
        """
        """
        fov = self.spFov.value()
        self.sldFov.setValue(fov) # sync slider
        self.camera.fov = fov

    def slider_value_changed_distance(self, sliderValue):
        """
        """
        self.spDistance.setValue(sliderValue) # sync spinbox
        self.camera.distance = sliderValue

    def spinbox_editing_finished_distance(self):
        """
        """
        distance = self.spDistance.value()
        self.sldDistance.setValue(distance) # sync slider
        self.camera.distance = distance

    def slider_value_changed_centerx(self, sliderValue):
        """
        """
        self.spCenterX.setValue(sliderValue) # sync spinbox
        self.centerX = sliderValue
        self.camera.center = (self.centerX, self.centerY, self.centerZ)

    def spinbox_editing_finished_centerx(self):
        """
        """
        self.centerX = self.spCenterX.value()
        self.sldCenterX.setValue(self.centerX) # sync slider
        self.camera.center = (self.centerX, self.centerY, self.centerZ)

    def slider_value_changed_centery(self, sliderValue):
        """
        """
        self.spCenterY.setValue(sliderValue) # sync spinbox
        self.centerY = sliderValue
        self.camera.center = (self.centerX, self.centerY, self.centerZ)

    def spinbox_editing_finished_centery(self):
        """
        """
        self.centerY = self.spCenterY.value()
        self.sldCenterY.setValue(self.centerY) # sync slider
        self.camera.center = (self.centerX, self.centerY, self.centerZ)

    def slider_value_changed_centerz(self, sliderValue):
        """
        """
        self.spCenterZ.setValue(sliderValue) # sync spinbox
        self.centerZ = sliderValue
        self.camera.center = (self.centerX, self.centerY, self.centerZ)

    def spinbox_editing_finished_centerz(self):
        """
        """
        self.centerZ = self.spCenterZ.value()
        self.sldCenterZ.setValue(self.centerZ) # sync slider
        self.camera.center = (self.centerX, self.centerY, self.centerZ)

    def load_from_viewer(self):
        state = self.camera.state

        azimuth = state['azimuth']
        self.sldAzimuth.setValue(azimuth)
        self.spAzimuth.setValue(azimuth)

        elevation = state['elevation']
        self.sldElevation.setValue(elevation)
        self.spElevation.setValue(elevation)

        fov = state['fov']
        self.sldFov.setValue(fov)
        self.spFov.setValue(fov)

        distance = state['distance']
        self.sldDistance.setValue(distance)
        self.spDistance.setValue(distance)

        self.centerX, self.centerY, self.centerZ = state['center']
        self.sldCenterX.setValue(self.centerX)
        self.spCenterX.setValue(self.centerX)
        self.sldCenterY.setValue(self.centerY)
        self.spCenterY.setValue(self.centerY)
        self.sldCenterZ.setValue(self.centerZ)
        self.spCenterZ.setValue(self.centerZ)
        # set slider range +/- 10000 as zoom in?


def main():
    from qtpy.QtWidgets import QApplication
    app = QApplication([])
    test = Dialog()
    test.show()
    app.exec_()


if __name__ == '__main__':
    main()
