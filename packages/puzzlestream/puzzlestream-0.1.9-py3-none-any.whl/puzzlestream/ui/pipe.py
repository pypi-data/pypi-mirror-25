from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QBrush, QColor, QPalette, QPen

import puzzlestream.backend
from puzzlestream.ui.puzzleitem import PSPuzzleItem


class PSPipe(PSPuzzleItem):

    def __init__(self, pipeID, x, y):
        """
        =======================================================================
            Define GUI appearence: geometry and position
        """

        self.__width = 40
        self.__length = 100
        self.__buttonsize = 20
        self.__bodycolor = "darkgreen"
        self.__framecolor = "black"
        self.__name = "Pipe_" + str(pipeID)

        self.__initposx, self.__initposy = 0, 0
        self._radius = self.__length / 2

        super().__init__(pipeID)

        self.setTransformOriginPoint(
            self.__initposx + self.__width / 2,
            self.__initposy + self.__length / 2)

        self.__body = QtWidgets.QGraphicsRectItem(
            self.boundingRect(), parent=self)
        self.__bodyBrush = QBrush(QColor(self.__bodycolor))
        self.__framePen = QPen(QColor(self.__framecolor))

        self.__body.setBrush(self.__bodyBrush)
        self.__body.setPen(self.__framePen)

        widgetGeoRect = QtCore.QRect(
            self.__initposx + self.__width / 2 - self.__buttonsize / 2,
            self.__initposy + self.__length / 2 - self.__buttonsize / 2,
            self.__buttonsize, self.__buttonsize
        )
        widgetGeoRectF = QtCore.QRectF(widgetGeoRect)

        self.__proxyWidgetBox = QtWidgets.QGraphicsProxyWidget(parent=self)
        self.__proxyWidgetBox.setGeometry(widgetGeoRectF)
        self.__changeOrientationButton = QtWidgets.QPushButton()
        self.__changeOrientationButton.setAutoFillBackground(False)
        self.__changeOrientationButton.setAttribute(
            QtCore.Qt.WA_NoSystemBackground)
        self.__changeOrientationButton.setGeometry(widgetGeoRect)
        self.__changeOrientationButton.clicked.connect(self.changeOrientation)
        self.__proxyWidgetBox.setWidget(self.__changeOrientationButton)

        """
        =======================================================================
            Initialisation of backendstructure
        """

        self.__inputItem = None
        self.autopass = True
        self.setPos(QtCore.QPointF(x, y))

    def __str__(self):
        return self.__name

    def __repr__(self):
        return self.__name

    @property
    def orientation(self):
        if int(round(self.rotation())) == 90:
            return "horizontal"
        return "vertical"

    def changeOrientation(self):
        if self.orientation == "horizontal":
            self.setRotation(0)
        elif self.orientation == "vertical":
            self.setRotation(90)

    def setOrientation(self, orientation):
        if orientation == "horizontal":
            self.setRotation(90)
        elif orientation == "vertical":
            self.setRotation(0)

    def boundingRect(self):
        return QtCore.QRectF(self.__initposx, self.__initposy,
                             self.__width, self.__length)

    @property
    def __shift(self):
        if self.orientation == "horizontal":
            return QtCore.QPointF(-self.__length / 2, self.__width / 2)
        return QtCore.QPointF(self.__width / 2, self.__length / 2)

    def centerPos(self):
        return self.scenePos() + self.__shift

    def setCenterPos(self, point):
        self.setPos(point - self.__shift)

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu()
        dataViewAction = QtWidgets.QAction("Show data")
        plotViewAction = QtWidgets.QAction("Show plots")

        if self.autopass is True:
            closingAction = QtWidgets.QAction("Close pipe")
        else:
            closingAction = QtWidgets.QAction("Open pipe")

        deleteAction = QtWidgets.QAction("Delete pipe")

        dataViewAction.triggered.connect(self._requestDataView)
        plotViewAction.triggered.connect(self._requestPlotView)
        closingAction.triggered.connect(self.__openClose)
        deleteAction.triggered.connect(self._requestDeletion)

        if self.streamSection is None:
            dataViewAction.setEnabled(False)
            plotViewAction.setEnabled(False)

        menu.addAction(dataViewAction)
        menu.addAction(plotViewAction)
        menu.addAction(closingAction)
        menu.addAction(deleteAction)
        action = menu.exec(event.screenPos())

    @property
    def saveProperties(self):
        props = {"autopass": self.autopass,
                 "orientation": self.orientation}

        if self.__inputItem is not None:
            props["inItemID"] = self.__inputItem.id

        props.update(super().saveProperties)
        return props

    def restoreProperties(self, props):
        super().restoreProperties(props)
        self.autopass = props["autopass"]
        self.setOrientation(props["orientation"])

    def __openClose(self):
        if self.autopass:
            self.autopass = False
        else:
            self.autopass = True

    @property
    def inputItem(self):
        return self.__inputItem

    def inputUpdate(self, puzzleItem):
        if (puzzleItem.status == "paused" or puzzleItem.status == "paused" or
                puzzleItem.status == "running"):
            self.status = "paused"
        else:
            self.streamSection = puzzleItem.streamSection
            self.status = "finished"

    def setInputItem(self, puzzleItem):
        if isinstance(puzzleItem, PSPuzzleItem):
            self.disconnectInputItem()
            self.__inputItem = puzzleItem
            puzzleItem.statusChanged.connect(self.inputUpdate)
        else:
            raise TypeError

    def disconnectInputItem(self):
        if self.__inputItem is not None:
            self.__inputItem.statusChanged.disconnect(self.inputUpdate)
            self.__inputItem = None
