import json
import os
import shutil
from math import sqrt
from threading import Thread

import numpy as np
from PyQt5 import QtCore, QtWidgets

from puzzlestream.backend.graphicsscene import PSGraphicsScene
from puzzlestream.backend.module import PSModule
from puzzlestream.backend.pipe import PSPipe
from puzzlestream.backend.stream import PSStream
from puzzlestream.backend.streamsection import PSStreamSection
from puzzlestream.backend.valve import PSValve
from puzzlestream.backend.config import PSConfig


class PSManager(QtCore.QObject):

    configChanged = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.__stream, self.__projectPath, self.__libs = None, None, []
        self.__scene = PSGraphicsScene()
        self.__scene.installEventFilter(self)
        self.__scene.mousePressed.connect(self.__itemDrag)
        self.__scene.positionChanged.connect(self.__positionChanged)
        self.__scene.mouseReleased.connect(self.__mouseReleased)

        self.addStatus = None
        self.config = PSConfig()
        self.config.edited.connect(self.configChanged.emit)
        self.__dockingrange = 200
        self.__connectionOnDrop = False

    def close(self):
        self.__stream.clear()
        self.__stream.close()

    @property
    def stream(self):
        return self.__stream

    @property
    def scene(self):
        return self.__scene

    @property
    def projectPath(self):
        return self.__projectPath

    def eventFilter(self, target, event):
        if isinstance(event, QtWidgets.QGraphicsSceneMouseEvent):
            x, y = event.scenePos().x(), event.scenePos().y()

            if (self.addStatus is not None and
                    event.button() == QtCore.Qt.LeftButton):
                if self.addStatus == "intModule":
                    self.newModule(x, y)
                elif self.addStatus == "extModule":
                    path = QtWidgets.QFileDialog.getOpenFileName()
                    if os.path.isfile(path[0]):
                        self.newModule(x, y, path[0])
                elif self.addStatus == "pipe":
                    self.newPipe(x, y)
                elif self.addStatus == "valve":
                    self.newValve(x, y)
                self.addStatus = None
        return QtCore.QObject.eventFilter(self, target, event)

    def __itemDrag(self, puzzleItem):
        """
            Puzzleitems OnClick Method:
            1. Save selected items and force the scene to save
               the position of all selected puzzleitems to allow position
               reset, if there is no valid constellation OnDrop
        """
        self.__sel = self.scene.selectedItemList
        self.__unsel = self.scene.unselectedItemList
        self.scene.bkSelectedItemPos()

    def __positionChanged(self, puzzleItem):
        """
            This method is connected to any movement of Module, Pipe or Valve
            in the PSGraphicsScene.

            1. Calculate the dists of any selected item to any unselected
               item and save those pairs as possible connection canidates
            2. Find the pair of selected and unselected items with
               minimum distance
            3. Check if this distance is smaller than the docking range
               that shall be experienced
                    a) distance > dockingrange:
                        - set flag: connectionOnDrop = False
                    b) distance < dockingrange:
                        - check if the connection would lead to a valid
                          Puzzle
                            i) connection NOT valid:
                                - delete the pair of items from connection
                                  cannidates
                                - go back to step 2
                            ii) connection valid:
                                - Save the right dockingstation for connection
                                - set flag: connectionOnDrop = True
                                - GUI feedback: dockingstation now visible

        """
        # ---  1. ---#
        if len(self.__unsel) != 0:
            dists = np.empty(
                [len(self.__sel), len(self.__unsel)]
            )

            for i in range(len(self.__sel)):
                neighbors = self.scene.getNeighbors(self.__sel[i])
                for key in neighbors:
                    index = -1
                    for j in range(len(self.__unsel)):
                        if self.__unsel[j].id == key.id:
                            index = j
                            break
                    dists[i, index] = neighbors[key]

        # ---  2. ---#
            somethingInRange = True
            while somethingInRange:
                minPairIndizes = np.unravel_index(
                    np.argmin(dists), dists.shape)
                minDist = dists[minPairIndizes[0], minPairIndizes[1]]
                if minDist > self.__dockingrange:
                    self.__connectionOnDrop = False
                    return None
                else:
                    minPair = [self.__sel[minPairIndizes[0]],
                               self.__unsel[minPairIndizes[1]]]
                    self.__connectionOnDrop = True
                    somethingInRange = False

        """
        for i in items:
            posn = i.centerPos()
            xn, yn = posn.x(), posn.y()
            minDistance = puzzleItem.radius + i.radius
            distance = sqrt((xn - x)**2 + (yn - y)**2)

            if ((isinstance(puzzleItem, PSPipe) and isinstance(i, PSModule))
                    or (isinstance(i, PSPipe) and
                    isinstance(puzzleItem, PSModule))):

                if isinstance(puzzleItem, PSPipe):
                    module, pipe = i, puzzleItem
                    xdif, ydif = x - xn, y - yn
                else:
                    module, pipe = puzzleItem, i
                    xdif, ydif = xn - x, yn - y

                if not module.dock1.connected:
                    dock = module.dock1
                elif not module.dock2.connected:
                    dock = module.dock2
                else:
                    dock = None

        """

    def __mouseReleased(self, puzzleItem):
        if not self.__connectionOnDrop:
            self.scene.resetItemPos()
        self.save()

    def newModule(self, x, y, path=None):
        moduleID = self.scene.getNextID()

        if path is None:
            modPath, name = self.__projectPath, "Module_" + str(moduleID)
        else:
            modPath, name = os.path.split(os.path.splitext(path)[0])

        module = PSModule(
            moduleID, x, y, modPath, name,
            self.newStreamSection, self.libs
        )

        if path is None or os.stat(module.filePath).st_size == 0:
            with open(module.filePath, "w") as f:
                f.write("\ndef main(data):\n\treturn data\n")

        self.scene.addModule(module)

    def newPipe(self, x, y):
        pipe = PSPipe(self.scene.getNextID(), x, y)
        self.scene.addPipe(pipe)

    def newValve(self, x, y):
        valve = PSValve(self.scene.getNextID(), x, y)
        self.scene.addValve(valve)

    def newStreamSection(self, pipeID):
        return PSStreamSection(pipeID, self.__stream)

    def newProject(self, path):
        if self.__stream is not None:
            self.__stream.close()
        self.__stream = PSStream(path + "/pscache")
        self.__projectPath = path
        self.__scene.clear()
        self.config.addRecentProject(path)
        self.scene.lastID = -1
        self.save()

    def save(self, thread=True):
        if thread:
            thr = Thread(target=self.__savePuzzle, args=(self.__projectPath,))
            thr.start()
        else:
            self.__savePuzzle(self.__projectPath)

    def saveAs(self, path):
        shutil.rmtree(path)
        shutil.copytree(self.__projectPath, path)
        thr = Thread(target=self.__savePuzzle, args=(path,))
        thr.start()

        for module in self.scene.modules.values():
            if module.path == self.__projectPath:
                module.path = path

        self.__projectPath = path
        self.__stream.close()
        self.__stream = PSStream(self.__projectPath + "/pscache")
        self.config.addRecentProject(path)

    def load(self, path):
        if self.__stream is not None:
            self.__stream.close()
        self.__stream = PSStream(path + "/pscache")
        self.__projectPath = path
        self.__loadPuzzle(self.__projectPath, False)
        self.config.addRecentProject(path)

    def __savePuzzle(self, path):
        moduleProps = []
        for moduleID in self.__scene.modules:
            moduleProps.append(self.__scene.modules[moduleID].saveProperties)

        pipeProps = []
        for pipeID in self.__scene.pipes:
            pipeProps.append(self.__scene.pipes[pipeID].saveProperties)

        valveProps = []
        for valveID in self.__scene.valves:
            valveProps.append(self.__scene.valves[valveID].saveProperties)

        with open(path + "/puzzle.json", "w") as f:
            json.dump({"modules": moduleProps, "pipes": pipeProps,
                       "valves": valveProps, "lastID": self.__scene.lastID,
                       "libs": self.libs}, f)

    def __loadPuzzle(self, path, clearStream=True):
        if clearStream:
            self.__stream.clear()
        with open(path + "/puzzle.json", "r") as f:
            puzzle = json.load(f)

        self.__scene.lastID = puzzle["lastID"]
        self.__libs = puzzle["libs"]

        self.__scene.clear()
        pipes = []
        for props in puzzle["pipes"]:
            pipe = PSPipe(props["id"], props["x"], props["y"])
            pipe.restoreProperties(props)
            pipes.append(pipe)
            pipe.streamSection = PSStreamSection(pipe.id, self.__stream)
            self.__scene.addPipe(pipe)

        for props in puzzle["valves"]:
            valve = PSValve(props["id"], props["x"], props["y"])
            valve.restoreProperties(props)
            valve.streamSection = PSStreamSection(valve.id, self.__stream)
            inPipeIDs = props["inPipeIDs"]

            for i in inPipeIDs:
                valve.addInputPipe(self.__scene.pipes[i])

            self.__scene.addValve(valve)

        for props in puzzle["modules"]:
            module = PSModule(props["id"], props["x"], props["y"],
                              props["path"], props["name"],
                              self.newStreamSection, self.__libs)
            module.restoreProperties(props)

            if "lastID" in props:
                module.lastID = props["lastID"]

            if "inPipeID" in props:
                module.setInputPipe(self.__scene.pipes[props["inPipeID"]])

            module.streamSection = PSStreamSection(module.id, self.__stream)
            self.__scene.addModule(module)

        for i in range(len(pipes)):
            props = puzzle["pipes"][i]
            if "inPipeID" in props:
                if props["inPipeID"] in self.__scene.pipes:
                    self.__scene.pipes[props["inPipeID"]].setInputItem(
                        pipes[i]
                    )
                else:
                    self.__scene.valves[props["inPipeID"]].setInputItem(
                        pipes[i]
                    )

    @property
    def libs(self):
        return self.__libs

    def addLib(self, path):
        if path not in self.libs:
            self.__libs.append(path)
            self.save()

    def deleteLib(self, path):
        i = self.__libs.index(path)
        del self.__libs[i]
        self.save()
