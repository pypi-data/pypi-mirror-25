import matplotlib.backends.backend_qt5agg as mplAgg
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtWidgets


class PSPlotView(QtWidgets.QMainWindow):

    def __init__(self, stream, config, parent=None, numberOfViewers=1):
        super().__init__(parent)
        self.__viewers = []
        self.__viewerWindows = []
        self.__stream = stream
        self.__config = config
        self.__autotile = self.__config["autotilePlots"]
        self.__createGUI(numberOfViewers)
        self.setWindowTitle("Plot view")
        self.show()

    def __createGUI(self, numberOfViewers=1):
        self.mdi = QtWidgets.QMdiArea()
        self.setCentralWidget(self.mdi)

        self.toolbar = QtWidgets.QToolBar()
        addAction = self.toolbar.addAction("Add viewer")
        tileAction = self.toolbar.addAction("Tile windows")

        tileChkBox = QtWidgets.QCheckBox("auto tile")
        tileChkBox.setChecked(self.__config["autotilePlots"])
        tileChkBox.stateChanged.connect(self.__autotileChanged)
        self.toolbar.addWidget(tileChkBox)

        addAction.triggered.connect(self.__addViewer)
        tileAction.triggered.connect(self.mdi.tileSubWindows)
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        for i in range(numberOfViewers):
            self.__addViewer()

    def __addViewer(self):
        viewer = PSSinglePlotView(self.__stream, self)
        window = QtWidgets.QMdiSubWindow()
        window.setWidget(viewer)
        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.__viewers.append(viewer)
        self.__viewerWindows.append(window)
        self.mdi.addSubWindow(window)
        window.show()

        if self.__autotile:
            self.mdi.tileSubWindows()

    def __autotileChanged(self, state):
        self.__autotile = state == 2

    def updatePlots(self):
        for viewer in self.__viewers:
            viewer.updatePlots()

    def closeEvent(self, event):
        self.__config["autotilePlots"] = self.__autotile
        event.accept()


class PSSinglePlotView(QtWidgets.QWidget):

    def __init__(self, stream, parent=None):
        super().__init__(parent)
        self.__stream = stream
        self.__parent = parent
        self.box = QtWidgets.QGridLayout()
        self.setLayout(self.box)
        self.__plots = []

        self.combo = QtWidgets.QComboBox()
        self.combo.currentIndexChanged.connect(self.__selectionChanged)
        self.box.addWidget(self.combo, 0, 0)

        self.canvas, self.mpltoolbar = None, None
        self.updatePlots()

    def updatePlots(self):
        plotList = []

        for key in self.__stream:
            if isinstance(self.__stream[key], Figure):
                plotList.append((key, self.__stream[key]))

        self.__plots = sorted(plotList, key=lambda x: x[0])
        self.combo.clear()
        for plot in self.__plots:
            self.combo.addItem(plot[0])
        self.__setFigure()

    def __setFigure(self, index=0):
        if self.canvas is not None:
            self.canvas.hide()
            self.mpltoolbar.hide()
            self.box.removeWidget(self.canvas)
            self.box.removeWidget(self.mpltoolbar)
            del self.canvas
            del self.mpltoolbar

        if len(self.__plots) > 0:
            fig = self.__plots[index][1]
            self.canvas = mplAgg.FigureCanvasQTAgg(fig)
            self.canvas.setParent(self.__parent)
            self.box.addWidget(self.canvas, 1, 0)

            self.mpltoolbar = mplAgg.NavigationToolbar2QT(self.canvas,
                                                          self.__parent)
            self.box.addWidget(self.mpltoolbar, 2, 0)

    def __selectionChanged(self):
        self.__setFigure(self.combo.currentIndex())
