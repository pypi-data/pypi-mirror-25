from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPen

from puzzlestream.backend.event import PSEvent


class PSPuzzleItem(QtWidgets.QGraphicsItem):

    def __init__(self, ID, *args):
        super().__init__(*args)
        self.__id = ID
        self.streamSection = None
        self.__status = "incomplete"
        self.__statusChanged = PSEvent()
        self.__positionChanged = PSEvent()
        self.__mousePressed = PSEvent()
        self.__mouseReleased = PSEvent()
        self.__selected = PSEvent()
        self.__dataViewRequested = PSEvent()
        self.__plotViewRequested = PSEvent()
        self.__deletionRequested = PSEvent()
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)

    @property
    def saveProperties(self):
        return {"id": self.id, "status": self.status,
                "x": self.centerPos().x(), "y": self.centerPos().y()}

    def restoreProperties(self, props):
        status = props["status"]
        if (status == "finished" or
                status == "error" or
                status == "test failed"):
            self.status = status
        self.setCenterPos(QtCore.QPointF(props["x"], props["y"]))

    def paint(self, painter, *args):
        if self.isSelected():
            pen = QPen()
            pen.setWidth(4)
            painter.setPen(pen)
            painter.drawRect(self.boundingRect())

    @property
    def radius(self):
        return self._radius

    def centerPos(self):
        pass

    def setCenterPos(self):
        pass

    def _standardContextMenu(self):
        menu = QtWidgets.QMenu()
        dataViewAction = QtWidgets.QAction("Show data")
        plotViewAction = QtWidgets.QAction("Show plots")
        deleteAction = QtWidgets.QAction("Delete")
        dataViewAction.triggered.connect(self._requestDataView)
        plotViewAction.triggered.connect(self._requestPlotView)
        menu.addAction(dataViewAction)
        menu.addAction(plotViewAction)
        menu.addAction(deleteAction)
        return menu

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.mousePressed.emit(self)

    def mouseDoubleClickEvent(self, event):
        self.dataViewRequested.emit(self)

    def mouseMoveEvent(self, event):
        self.positionChanged.emit(self)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.mouseReleased.emit(self)
        super().mouseReleaseEvent(event)

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemSelectedChange:
            if bool(value):
                self.selected.emit(self)
        return QtWidgets.QGraphicsItem.itemChange(self, change, value)

    @property
    def status(self):
        return self.__status

    @property
    def statusChanged(self):
        return self.__statusChanged

    @property
    def mousePressed(self):
        return self.__mousePressed

    @property
    def positionChanged(self):
        return self.__positionChanged

    @property
    def mouseReleased(self):
        return self.__mouseReleased

    @property
    def selected(self):
        return self.__selected

    @property
    def dataViewRequested(self):
        return self.__dataViewRequested

    @property
    def plotViewRequested(self):
        return self.__plotViewRequested

    @property
    def deletionRequested(self):
        return self.__deletionRequested

    @status.setter
    def status(self, status):
        if isinstance(status, str):
            self.__status = status
            self.statusChanged.emit(self)
        else:
            raise TypeError

    def inputUpdate(self, module):
        pass

    @property
    def id(self):
        return self.__id

    def _requestDataView(self):
        self.dataViewRequested.emit(self)

    def _requestPlotView(self):
        self.plotViewRequested.emit(self)

    def _requestDeletion(self):
        self.deletionRequested.emit(self)
