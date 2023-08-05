import matplotlib.backends.backend_qt5agg as mplAgg
import numpy as np
import pyqtgraph as pg
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui, QtWidgets

from puzzlestream.backend.reference import PSCacheReference


class NumpyModel(QtCore.QAbstractTableModel):

    def __init__(self, narray, parent=None):
        super().__init__(parent)
        self.__array = narray

    def rowCount(self, parent=None):
        return self.__array.shape[0]

    def columnCount(self, parent=None):
        return self.__array.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                row = index.row()
                col = index.column()
                return QtCore.QVariant(str(self.getItemAt(row, col)))
        return QtCore.QVariant()

    def getItemAt(self, row, column):
        return self.__array[row, column]

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(section)
        return QtCore.QVariant()


class GeneralModel(QtCore.QAbstractTableModel):

    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.__data = data
        self.createKeyList()

    def createKeyList(self):
        keys = []

        for key in self.__data:
            if (isinstance(self.__data[key], np.ndarray) and
                    len(self.__data[key].shape) == 1):
                keys.append(key)

        self.__keys = sorted(keys)

    @property
    def keys(self):
        return self.__keys

    def rowCount(self, parent=None):
        maxLength = 0

        for key in self.__data:
            if isinstance(self.__data[key], np.ndarray):
                if len(self.__data[key]) > maxLength:
                        maxLength = len(self.__data[key])
        return maxLength + 1

    def columnCount(self, parent=None):
        return len(self.keys)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                row = index.row()
                col = index.column()
                if row > 0 and row < len(self.__data[self.__keys[col]]) + 1:
                    return QtCore.QVariant(str(self.getItemAt(row, col)))
        return QtCore.QVariant()

    def getItemAt(self, row, column):
        return self.__data[self.__keys[column]][row - 1]

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return QtCore.QVariant(self.__keys[section])
            else:
                if section > 0:
                    return QtCore.QVariant(section - 1)
        return QtCore.QVariant()


class PSDataView(QtWidgets.QMainWindow):

    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Data view")
        self.__data = data
        self.canvas, self.mpltoolbar = None, None
        self.__x, self.__y = None, None

        self.horizontalSplitter = QtWidgets.QSplitter()
        self.horizontalSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSplitter.setObjectName("horizontalSplitter")
        self.setCentralWidget(self.horizontalSplitter)

        self.tableModel = GeneralModel(self.__data)
        self.tableView = QtWidgets.QTableView(self.horizontalSplitter)
        self.tableView.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        self.tableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(
            self.tableContextMenu)
        self.horizontalSplitter.addWidget(self.tableView)
        self.tableView.setModel(self.tableModel)
        self.currentTable = self.tableModel

        self.verticalLayoutWidget = QtWidgets.QWidget(self.horizontalSplitter)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayoutWidget.setLayout(self.verticalLayout)
        self.horizontalSplitter.addWidget(self.verticalLayoutWidget)

        self.listModel = QtGui.QStandardItemModel(self.verticalLayoutWidget)
        self.listView = QtWidgets.QListView(self.verticalLayoutWidget)
        self.listView.setModel(self.listModel)

        self.plotGroupWidget = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.plotGroupWidgetLayout = QtWidgets.QVBoxLayout(
            self.plotGroupWidget)
        self.plotWidget = pg.PlotWidget(self.plotGroupWidget)
        self.plotCurve = pg.PlotCurveItem()
        self.plotWidget.addItem(self.plotCurve)

        self.dropdownX = QtWidgets.QComboBox(self.plotGroupWidget)
        self.dropdownY = QtWidgets.QComboBox(self.plotGroupWidget)
        self.dropdownX.currentIndexChanged.connect(self.setAsXDropdown)
        self.dropdownY.currentIndexChanged.connect(self.setAsYDropdown)
        self.swapBtn = QtWidgets.QPushButton(self.plotGroupWidget)
        self.swapBtn.setText("swap axes")
        self.swapBtn.setMaximumWidth(100)
        self.swapBtn.clicked.connect(self.swapAxes)
        self.hboxDropdown = QtWidgets.QHBoxLayout()
        self.hboxDropdown.addWidget(self.dropdownX)
        self.hboxDropdown.addWidget(self.swapBtn)
        self.hboxDropdown.addWidget(self.dropdownY)

        self.plotGroupWidgetLayout.addWidget(self.listView)
        self.plotGroupWidgetLayout.addLayout(self.hboxDropdown)
        self.plotGroupWidgetLayout.addWidget(self.plotWidget)

        self.mplGroupWidget = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.mplLayout = QtWidgets.QVBoxLayout(self.mplGroupWidget)
        self.mplGroupWidget.setLayout(self.mplLayout)

        self.verticalLayout.addWidget(self.listView)
        self.verticalLayout.addWidget(self.plotGroupWidget)
        self.verticalLayout.addWidget(self.mplGroupWidget)
        self.mplGroupWidget.hide()

        self.horizontalSplitter.setStretchFactor(0, 6)
        self.horizontalSplitter.setStretchFactor(1, 4)

        self.menubar = QtWidgets.QMenuBar(self)
        self.filemenu = QtWidgets.QMenu("File", self.menubar)
        self.datamenu = QtWidgets.QMenu("Data", self.menubar)
        self.menubar.addMenu(self.filemenu)
        self.menubar.addMenu(self.datamenu)
        self.setMenuBar(self.menubar)

        if len(self.__data) > 0:
            self.dataUpdate()

        self.showMaximized()

    def dataUpdate(self):
        listKeys = []

        for key in self.__data:
            if not isinstance(self.__data[key], PSCacheReference):
                listKeys.append(key)

        self.__listKeys = sorted(listKeys)

        self.tableView.horizontalHeader().setDefaultSectionSize(150)
        self.tableView.setRowHeight(0, 75)

        for i, key in enumerate(self.__listKeys):
            item = QtGui.QStandardItem(key)
            if key in self.tableModel.keys:
                item.setCheckable(True)
                item.setCheckState(2)
            self.listModel.setItem(i, item)
            # self.listModel.itemChanged.connect(lambda event: print(event))

        for column, key in enumerate(self.tableModel.keys):
            data = self.__data[key]

            w = pg.PlotWidget()
            w.getViewBox().setBackgroundColor("w")
            w.getPlotItem().hideAxis("bottom")
            w.getPlotItem().hideAxis("left")
            w.getPlotItem().hideButtons()
            w.getPlotItem().setMenuEnabled(False)
            w.getPlotItem().setMouseEnabled(False, False)
            w.getPlotItem().plot(np.arange(len(data)), data,
                                 pen=pg.mkPen("k"))
            index = self.tableView.model().index(0, column)
            self.tableView.setIndexWidget(index, w)

        self.dropdownX.clear()
        self.dropdownY.clear()
        for key in self.tableModel.keys:
            self.dropdownX.addItem(key)
            self.dropdownY.addItem(key)

        self.listView.setModel(self.listModel)
        self.listView.setEditTriggers(QtWidgets.QListView.NoEditTriggers)
        self.listView.selectionModel().selectionChanged.connect(
            self.listSelectionChanged
        )
        self.listView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listView.customContextMenuRequested.connect(self.listContextMenu)

    def listContextMenu(self, event):
        menu = QtWidgets.QMenu(self)
        xAction = menu.addAction("Set as x")
        xAction.triggered.connect(self.setAsXList)
        yAction = menu.addAction("Set as y")
        yAction.triggered.connect(self.setAsYList)
        action = menu.exec_(self.listView.mapToGlobal(event))

    def tableContextMenu(self, event):
        menu = QtWidgets.QMenu(self)
        exportAction = menu.addAction("Export")
        action = menu.exec_(self.tableView.mapToGlobal(event))

    def setAsXList(self):
        key = self.__listKeys[self.listView.currentIndex().row()]
        self.dropdownX.setCurrentIndex(self.tableModel.keys.index(key))

    def setAsYList(self):
        key = self.__listKeys[self.listView.currentIndex().row()]
        self.dropdownY.setCurrentIndex(self.tableModel.keys.index(key))

    def setAsXDropdown(self):
        index = self.dropdownX.currentIndex()
        self.__x = self.__data[self.tableModel.keys[index]]
        self.plotUpdate()

    def setAsYDropdown(self):
        index = self.dropdownY.currentIndex()
        self.__y = self.__data[self.tableModel.keys[index]]
        self.plotUpdate()

    def swapAxes(self):
        ix, iy = self.dropdownX.currentIndex(), self.dropdownY.currentIndex()
        self.dropdownX.setCurrentIndex(iy)
        self.dropdownY.setCurrentIndex(ix)

    def plotUpdate(self):
        if self.__x is not None and self.__y is not None:
            self.plotCurve.setData(self.__x, self.__y)
            keyx = self.tableModel.keys[self.dropdownX.currentIndex()]
            keyy = self.tableModel.keys[self.dropdownY.currentIndex()]
            self.plotWidget.getPlotItem().setLabel("bottom", keyx)
            self.plotWidget.getPlotItem().setLabel("left", keyy)

    def listSelectionChanged(self):
        if self.canvas is not None:
            self.canvas.hide()
            self.mpltoolbar.hide()
            self.mplLayout.removeWidget(self.canvas)
            self.mplLayout.removeWidget(self.mpltoolbar)
            del self.canvas
            del self.mpltoolbar
            self.canvas, self.mpltoolbar = None, None
            self.mplGroupWidget.hide()

        if self.currentTable != self.tableModel:
            self.tableView.setModel(self.tableModel)
            self.currentTable = self.tableModel

        self.tableView.clearSelection()

        i = self.listView.selectedIndexes()[0]
        key = self.listModel.data(i, 0)

        if isinstance(self.__data[key], Figure):
            self.listView.setCurrentIndex(i)
            self.hidePlotWidget()
            self.mplGroupWidget.show()

            fig = self.__data[key]
            self.canvas = mplAgg.FigureCanvasQTAgg(fig)
            self.canvas.setParent(self.mplGroupWidget)

            self.mpltoolbar = mplAgg.NavigationToolbar2QT(
                self.canvas,
                self.mplGroupWidget
            )

            self.mplLayout.addWidget(self.canvas)
            self.mplLayout.addWidget(self.mpltoolbar)
        elif key in self.tableModel.keys:
            self.plotUpdate()
            self.showPlotWidget()
            index = self.tableModel.keys.index(key)
            columns = [item.column()
                       for item in self.tableView.selectionModel().selectedColumns()]
            if index not in columns or index not in listColumns:
                self.tableView.selectColumn(index)
                self.listView.setFocus()
        elif isinstance(self.__data[key], np.ndarray):
            if len(self.__data[key].shape) == 2:
                model = NumpyModel(self.__data[key],
                                   self.horizontalSplitter)
                self.tableView.setModel(model)
                self.currentTable = model
        else:
            self.hidePlotWidget()

    def showPlotWidget(self):
        for e in (self.plotWidget, self.dropdownX,
                  self.dropdownY, self.swapBtn):
            e.show()

    def hidePlotWidget(self):
        for e in (self.plotWidget, self.dropdownX,
                  self.dropdownY, self.swapBtn):
            e.hide()
