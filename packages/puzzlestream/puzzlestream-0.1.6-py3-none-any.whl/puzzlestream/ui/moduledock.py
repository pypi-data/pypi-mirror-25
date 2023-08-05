from PyQt5 import QtWidgets
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QBrush, QColor, QMouseEvent, QPen, QPolygonF


class Triangle(QtWidgets.QGraphicsPolygonItem):

    def __init__(self, posx, posy, width, height, parent=None):

        super().__init__(parent=parent)

        self.__width = width
        self.__height = height
        self.__triangle = QPolygonF()

        self.__triangle.append(QPointF(posx - self.__width / 2, posy))
        self.__triangle.append(QPointF(posx, posy - self.__height))
        self.__triangle.append(QPointF(posx + self.__width / 2, posy))
        self.__triangle.append(QPointF(posx - self.__width / 2, posy))

        self.setPolygon(self.__triangle)


class PSModuleDock(QtWidgets.QGraphicsItemGroup):

    def __init__(self, initx, inity, width, height,
                 moduleWidth, moduleHeight, state,
                 parent=None):

        super().__init__(parent=parent)
        self.__initx = initx + moduleWidth / 2 - width / 2
        self.__inity = inity - height
        self.__state = state
        self.__width = width
        self.__height = height
        self.__moduleHeight = moduleHeight
        self.__moduleWidth = moduleWidth
        self.setFlag(QtWidgets.QGraphicsItemGroup.ItemIsSelectable)
        self.__position = "top"
        self.connected = False

        self.__rectangle = QtWidgets.QGraphicsRectItem(
            self.__initx, self.__inity, self.__width, self.__height
        )

        self.__triangle = Triangle(
            self.__initx + self.__width / 2, self.__inity + self.__height,
            self.__width, self.__height
        )

        self.addToGroup(self.__rectangle)
        self.addToGroup(self.__triangle)

        self.__colorDock()
        self.setTransformOriginPoint(
            self.__initx + self.__width / 2, self.__inity + self.__height / 2)

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        if self.__state == "in":
            self.changeToOutput()
        elif self.__state == "out":
            self.changeToInput()

    def __colorDock(self):

        if self.__state == "in":
            self.__rectBrush = QBrush(QColor("orange"))
        if self.__state == "out":
            self.__rectBrush = QBrush(QColor("violet"))

        self.__triBrush = QBrush(QColor("black"))
        self.__framePen = QPen(QColor("black"))

        self.__rectangle.setBrush(self.__rectBrush)
        self.__rectangle.setPen(self.__framePen)

        self.__triangle.setBrush(self.__triBrush)
        self.__triangle.setPen(self.__framePen)

    def __inputRotation(self):
        if self.__state == "in":
            if self.__position == "bottom":
                self.setRotation(180.)
            elif self.__position == "left":
                self.setRotation(270.)
            elif self.__position == "top":
                self.setRotation(0.)
            elif self.__position == "right":
                self.setRotation(90.)

    def __outputRotation(self):
        if self.__state == "out":
            if self.__position == "top":
                self.setRotation(180.)
            elif self.__position == "right":
                self.setRotation(270.)
            elif self.__position == "bottom":
                self.setRotation(0.)
            elif self.__position == "left":
                self.setRotation(90.)

    def changeToInput(self):
        self.__state = "in"
        self.__inputRotation()
        self.__colorDock()

    def changeToOutput(self):
        self.__state = "out"
        self.__outputRotation()
        self.__colorDock()

    def toTop(self):
        width = self.__moduleWidth + self.__height
        height = self.__moduleHeight + self.__height
        if self.__position == "bottom":
            self.moveBy(0, -height)
        elif self.__position == "right":
            self.moveBy(-width / 2, -height / 2)
        elif self.__position == "left":
            self.moveBy(width / 2, -height / 2)

        self.__position = "top"

        if self.__state == "in":
            self.__inputRotation()
        elif self.__state == "out":
            self.__outputRotation()

    def toBottom(self):
        width = self.__moduleWidth + self.__height
        height = self.__moduleHeight + self.__height
        if self.__position == "top":
            self.moveBy(0, height)
        elif self.__position == "right":
            self.moveBy(-width / 2, height / 2)
        elif self.__position == "left":
            self.moveBy(width / 2, height / 2)

        self.__position = "bottom"

        if self.__state == "in":
            self.__inputRotation()
        elif self.__state == "out":
            self.__outputRotation()

    def toLeft(self):
        width = self.__moduleWidth + self.__height
        height = self.__moduleHeight + self.__height

        if self.__position == "right":
            self.moveBy(-width, 0)
        elif self.__position == "bottom":
            self.moveBy(-width / 2, -height / 2)
        elif self.__position == "top":
            self.moveBy(-width / 2, height / 2)

        self.__position = "left"

        if self.__state == "in":
            self.__inputRotation()
        elif self.__state == "out":
            self.__outputRotation()

    def toRight(self):
        width = self.__moduleWidth + self.__height
        height = self.__moduleHeight + self.__height

        if self.__position == "left":
            self.moveBy(width, 0)
        elif self.__position == "bottom":
            self.moveBy(width / 2, -height / 2)
        elif self.__position == "top":
            self.moveBy(width / 2, height / 2)

        self.__position = "right"

        if self.__state == "in":
            self.__inputRotation()
        elif self.__state == "out":
            self.__outputRotation()

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, stateToSet):
        if stateToSet == "in":
            self.changeToInput()
        elif stateToSet == "out":
            self.changeToOutput()

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, posToSet):
        if posToSet == "top":
            self.toTop()
        elif posToSet == "bottom":
            self.toBottom()
        elif posToSet == "left":
            self.toLeft()
        elif posToSet == "right":
            self.toRight()
