import numpy as np
from PyQt5.QtCore import (QLineF, QPointF, QRect, QRectF, QSize, QSizeF, Qt,
                          pyqtSignal)
from PyQt5.QtGui import (QBrush, QColor, QFont, QIcon, QIntValidator, QPainter,
                         QPainterPath, QPen, QPixmap, QPolygonF)
from PyQt5.QtWidgets import (QAction, QApplication, QButtonGroup, QComboBox,
                             QFontComboBox, QGraphicsItem, QGraphicsLineItem,
                             QGraphicsPolygonItem, QGraphicsScene,
                             QGraphicsTextItem, QGraphicsView, QGridLayout,
                             QHBoxLayout, QLabel, QMainWindow, QMenu,
                             QMessageBox, QSizePolicy, QToolBox, QToolButton,
                             QWidget)

from puzzlestream.ui.module import PSModule
from puzzlestream.ui.pipe import PSPipe
from puzzlestream.ui.valve import PSValve


class PSGraphicsScene(QGraphicsScene):

    """
    ===========================================================================
        Init / events
    """

    stdoutChanged = pyqtSignal(object, object)
    statusChanged = pyqtSignal(object)
    mousePressed = pyqtSignal(object)
    positionChanged = pyqtSignal(object)
    mouseReleased = pyqtSignal(object)
    selectionChanged = pyqtSignal(object)
    progressChanged = pyqtSignal(object)
    itemAdded = pyqtSignal(object)
    dataViewRequested = pyqtSignal(object)
    plotViewRequested = pyqtSignal(object)

    def __init__(self, *args):
        super().__init__(*args)
        self.__modules, self.__pipes, self.__valves = {}, {}, {}
        self.__bkScenePos = {}
        self.lastID = -1

    """
    ===========================================================================
        Position Reset
    """

    def bkAllItemPos(self):
        for item in self.puzzleItemList:
            self.__bkScenePos[item.id] = item.scenePos()

    def bkSomePos(self, itemlist):
        for item in itemlist:
            self.__bkScenePos[item.id] = item.scenePos()

    def bkSelectedItemPos(self):
        for item in self.selectedItemList:
            self.__bkScenePos[item.id] = item.scenePos()

    def resetItemPos(self):
        for item in self.puzzleItemList:
            item.setPos(self.__bkScenePos[item.id])

    """
    ===========================================================================
        Stuff necessary for connecting items
    """

    def __distance(self, item1, item2):
        x1, y1 = item1.centerPos().x(), item1.centerPos().y()
        x2, y2 = item2.centerPos().x(), item2.centerPos().y()
        return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def getNeighbors(self, currentItem):
        itemList = self.puzzleItemList
        itemList.remove(currentItem)

        distances = []

        for item in itemList:
            distances.append(self.__distance(currentItem, item))

        neighbors = {item: distance for item, distance in
                     sorted(zip(itemList, distances),
                            key=lambda pair: pair[1])}

        return neighbors

    @property
    def numberOfItems(self):
        return (len(self.__modules) + len(self.__pipes) + len(self.__valves))

    @property
    def puzzleItemList(self):
        return (list(self.modules.values()) +
                list(self.pipes.values()) +
                list(self.valves.values()))

    @property
    def selectedItemList(self):
        selItemList = []
        for item in self.puzzleItemList:
            if item.isSelected() is True:
                selItemList.append(item)
        return selItemList

    @property
    def unselectedItemList(self):
        unselItemList = []
        for item in self.puzzleItemList:
            if item.isSelected() is False:
                unselItemList.append(item)
        return unselItemList

    """
    ===========================================================================
        Item dictionary properties
    """

    @property
    def modules(self):
        return self.__modules

    @property
    def pipes(self):
        return self.__pipes

    @property
    def valves(self):
        return self.__valves

    """
    ===========================================================================
        Item creation
    """

    def getNextID(self):
        self.lastID += 1
        return self.lastID

    def __setStandardConnections(self, puzzleItem):
        puzzleItem.statusChanged.connect(self.statusChanged.emit)
        puzzleItem.positionChanged.connect(self.positionChanged.emit)
        puzzleItem.mouseReleased.connect(self.mouseReleased.emit)
        puzzleItem.mousePressed.connect(self.mousePressed.emit)
        puzzleItem.dataViewRequested.connect(self.dataViewRequested.emit)
        puzzleItem.plotViewRequested.connect(self.plotViewRequested.emit)
        puzzleItem.deletionRequested.connect(self.deleteItem)
        puzzleItem.selected.connect(self.selectionChanged.emit)
        return puzzleItem

    def addModule(self, module):
        if isinstance(module, PSModule):
            module = self.__setStandardConnections(module)
            module.stdoutChanged.connect(self.stdoutChanged.emit)
            module.progressChanged.connect(self.progressChanged.emit)
            self.__modules[module.id] = module
            self.addItem(module)
            self.itemAdded.emit(module)
            self.bkSomePos([module])
        else:
            raise TypeError("Has to be a module.")

    def addPipe(self, pipe):
        if isinstance(pipe, PSPipe):
            self.__pipes[pipe.id] = pipe
            pipe = self.__setStandardConnections(pipe)
            self.addItem(pipe)
            self.itemAdded.emit(pipe)
            self.bkSomePos([pipe])
        else:
            raise TypeError("Has to be a pipe.")

    def addValve(self, valve):
        if isinstance(valve, PSValve):
            self.__valves[valve.id] = valve
            valve = self.__setStandardConnections(valve)
            self.addItem(valve)
            self.itemAdded.emit(valve)
            self.bkSomePos([valve])
        else:
            raise TypeError("Has to be a valve.")

    """
    ===========================================================================
        Item deletion
    """

    def deleteItem(self, puzzleItem):
        self.removeItem(puzzleItem)

        if isinstance(puzzleItem, PSModule):
            del self.__modules[puzzleItem.id]
        elif isinstance(puzzleItem, PSPipe):
            del self.__pipes[puzzleItem.id]
        elif isinstance(puzzleItem, PSValve):
            del self.__valves[puzzleItem.id]

    def clear(self):
        super().clear()
        self.__modules.clear()
        self.__pipes.clear()
        self.__valves.clear()
