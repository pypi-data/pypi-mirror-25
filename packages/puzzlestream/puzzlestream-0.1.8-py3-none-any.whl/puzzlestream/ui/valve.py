from puzzlestream.ui.pipe import PSPipe
from puzzlestream.ui.puzzleitem import PSPuzzleItem


class PSValve(PSPuzzleItem):

    def __init__(self, valveID):
        super().__init__(valveID)
        self.__inputPipes = []
        self.autopass = True

    @property
    def saveProperties(self):
        props = {"autopass": self.autopass,
                 "inPipeIDs": [p.id for p in self.__inputPipes]}
        props.update(super().saveProperties)
        return props

    def restoreProperties(self, props):
        super().restoreProperties(props)
        self.autopass = props["autopass"]

    def centerPos(self):
        pass

    def setCenterPos(self, point):
        pass

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu()
        dataViewAction = QtWidgets.QAction("Show data")
        plotViewAction = QtWidgets.QAction("Show plots")

        if self.autopass is True:
            closingAction = QtWidgets.QAction("Close pipe")
        else:
            closingAction = QtWidgets.QAction("Open pipe")

        deleteAction = QtWidgets.QAction("Delete valve")

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

    def inputUpdate(self, pipe):
        if pipe.status == "finished":
            if self.streamSection is None:
                self.streamSection = pipe.streamSection
            else:
                self.streamSection.addSection(pipe.streamSection)

        if True in [(p.status == "paused" or p.status == "paused" or
                     p.status == "running") for p in self.__inputPipes]:
            self.status = "paused"
        else:
            self.status = "finished"

    def __openClose(self):
        if self.autopass:
            self.autopass = False
        else:
            self.autopass = True

    @property
    def inputPipes(self):
        return self.__inputPipes

    def addInputPipe(self, pipe):
        if isinstance(pipe, PSPipe):
            pipe.statusChanged.connect(self.inputUpdate)
            self.__inputPipes.append(pipe)
        else:
            raise TypeError

    def removeInputPipe(self, pipe):
        if pipe in self.__inputPipes:
            pipe.statusChanged.disconnect(self.inputUpdate)
            i = self.__inputPipes.index(pipe)
            del self.__inputPipes[i]
