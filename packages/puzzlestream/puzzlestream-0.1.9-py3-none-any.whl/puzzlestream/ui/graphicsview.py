from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect, QSize, QRectF


class PSGraphicsView(QtWidgets.QGraphicsView):

    def __init__(self, *args):
        super().__init__(*args)
        self.setTransformationAnchor(
            QtWidgets.QGraphicsView.AnchorUnderMouse
        )

        self.__minZoom, self.__maxZoom = 0.5, 1.5

        self.slider = QtWidgets.QSlider(self)
        self.slider.setRange(int(10 * self.__minZoom),
                             int(10 * self.__maxZoom))
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setValue(10)
        self.slider.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                  QtWidgets.QSizePolicy.Fixed)
        self.slider.valueChanged.connect(self.__sliderValueChanged)
        self.addScrollBarWidget(self.slider, QtCore.Qt.AlignRight)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setDragMode(self.RubberBandDrag)

    def wheelEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier:
            if (event.angleDelta().y() < 0 and
                    self.transform().m11() > self.__minZoom):
                self.scale(0.9, 0.9)

            elif (event.angleDelta().y() > 0 and
                    self.transform().m11() < self.__maxZoom):
                self.scale(1.1, 1.1)

            self.slider.setValue(int(self.transform().m11() * 10))
        else:
            super().wheelEvent(event)

    def __sliderValueChanged(self, event):
        scale = self.slider.value() / 10
        self.setTransform(QtGui.QTransform.fromScale(scale, scale))
