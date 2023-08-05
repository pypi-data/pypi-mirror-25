import matplotlib.backends.backend_qt5agg as mplAgg
import numpy as np
import pyqtgraph as pg
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui, QtWidgets

from puzzlestream.backend.reference import PSCacheReference


class NumpyModel(QtCore.QAbstractTableModel):

    def __init__(self, narray, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
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
                return QtCore.QVariant(str(self.__array[row, col]))
        return QtCore.QVariant()


class ProgressViewer(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__progress = QtWidgets.QProgressBar(self)
        self.__text = QtWidgets.QLabel("Loading", self)

        self.__vbox = QtWidgets.QVBoxLayout()
        self.__vbox.addWidget(self.__progress)
        self.__vbox.addWidget(self.__text)
        self.setLayout(self.__vbox)

    def updateProgress(self, percent):
        self.__progress.setValue(percent)

    def updateText(self, text):
        self.__text.setText(text)


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

        self.tableWidget = QtWidgets.QTableWidget(self.horizontalSplitter)
        self.tableWidget.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        self.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(
            self.tableContextMenu)
        self.horizontalSplitter.addWidget(self.tableWidget)
        self.currentTable = self.tableWidget

        self.verticalLayoutWidget = QtWidgets.QWidget(self.horizontalSplitter)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayoutWidget.setLayout(self.verticalLayout)
        self.horizontalSplitter.addWidget(self.verticalLayoutWidget)

        self.listModel = QtCore.QStringListModel(self.verticalLayoutWidget)
        self.listView = QtWidgets.QListView(self.verticalLayoutWidget)

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
        tableKeys = []
        listKeys = []
        maxLength = 0

        for key in self.__data:
            if isinstance(self.__data[key], np.ndarray):
                if len(self.__data[key].shape) == 1:
                    tableKeys.append(key)
                    if len(self.__data[key]) > maxLength:
                        maxLength = len(self.__data[key])

            if not isinstance(self.__data[key], PSCacheReference):
                listKeys.append(key)

        self.__listKeys = sorted(listKeys)
        self.__tableKeys = sorted(tableKeys)

        self.tableWidget.setRowCount(maxLength + 1)
        self.tableWidget.setColumnCount(len(self.__tableKeys))
        self.tableWidget.setHorizontalHeaderLabels(self.__tableKeys)

        self.tableWidget.setVerticalHeaderItem(
            0, QtWidgets.QTableWidgetItem(""))
        for i in range(maxLength):
            self.tableWidget.setVerticalHeaderItem(
                i + 1, QtWidgets.QTableWidgetItem(str(i)))

        self.tableWidget.horizontalHeader().setDefaultSectionSize(150)
        self.tableWidget.setRowHeight(0, 75)
        self.listModel.setStringList(self.__listKeys)

        report = ProgressViewer(self)

        for column, key in enumerate(self.__tableKeys):
            report.updateText("Loading " + key)
            report.updateProgress(0)
            data = self.__data[key]

            for row, item in enumerate(data):
                tableItem = QtWidgets.QTableWidgetItem(str(item))
                self.tableWidget.setItem(row + 1, column, tableItem)
                report.updateProgress(row / len(data) * 100)

            w = pg.PlotWidget(parent=self.tableWidget)
            w.getViewBox().setBackgroundColor("w")
            w.getPlotItem().hideAxis("bottom")
            w.getPlotItem().hideAxis("left")
            w.getPlotItem().hideButtons()
            w.getPlotItem().setMenuEnabled(False)
            w.getPlotItem().setMouseEnabled(False, False)
            w.getPlotItem().plot(np.arange(len(data)), data,
                                 pen=pg.mkPen("k"))
            self.tableWidget.setCellWidget(0, column, w)

        report.hide()

        self.dropdownX.clear()
        self.dropdownY.clear()
        for key in self.__tableKeys:
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
        action = menu.exec_(self.currentTable.mapToGlobal(event))

    def setAsXList(self):
        key = self.__listKeys[self.listView.currentIndex().row()]
        self.dropdownX.setCurrentIndex(self.__tableKeys.index(key))

    def setAsYList(self):
        key = self.__listKeys[self.listView.currentIndex().row()]
        self.dropdownY.setCurrentIndex(self.__tableKeys.index(key))

    def setAsXDropdown(self):
        index = self.dropdownX.currentIndex()
        self.__x = self.__data[self.__tableKeys[index]]
        self.plotUpdate()

    def setAsYDropdown(self):
        index = self.dropdownY.currentIndex()
        self.__y = self.__data[self.__tableKeys[index]]
        self.plotUpdate()

    def swapAxes(self):
        ix, iy = self.dropdownX.currentIndex(), self.dropdownY.currentIndex()
        self.dropdownX.setCurrentIndex(iy)
        self.dropdownY.setCurrentIndex(ix)

    def plotUpdate(self):
        if self.__x is not None and self.__y is not None:
            self.plotCurve.setData(self.__x, self.__y)
            keyx = self.__tableKeys[self.dropdownX.currentIndex()]
            keyy = self.__tableKeys[self.dropdownY.currentIndex()]
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

        if self.currentTable != self.tableWidget:
            self.currentTable.hide()
            del self.currentTable
            self.tableWidget.show()
            self.currentTable = self.tableWidget

        self.tableWidget.clearSelection()

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
        elif key in self.__tableKeys:
            self.plotUpdate()
            self.showPlotWidget()
            index = self.__tableKeys.index(key)
            columns = [item.column()
                       for item in self.tableWidget.selectionModel().selectedColumns()]
            if index not in columns or index not in listColumns:
                self.tableWidget.selectColumn(index)
                self.listView.setFocus()
        elif isinstance(self.__data[key], np.ndarray):
            if len(self.__data[key].shape) == 2:
                model = NumpyModel(self.__data[key],
                                   self.horizontalSplitter)
                tableView = QtWidgets.QTableView(self.horizontalSplitter)
                tableView.setModel(model)
                tableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                tableView.customContextMenuRequested.connect(
                    self.tableContextMenu)
                self.tableWidget.hide()
                self.currentTable = tableView
                self.horizontalSplitter.insertWidget(0, tableView)
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
