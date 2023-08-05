import importlib as imp
import multiprocessing as mp
import os
import random
import string
import sys
import traceback
from multiprocessing.connection import Client, Listener
from threading import Thread
from time import sleep, time

import numpy as np
import psutil
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QBrush, QColor, QPen

from puzzlestream import pslib
from puzzlestream.backend.event import PSEvent
from puzzlestream.backend.pipe import PSPipe
from puzzlestream.backend.puzzleitem import PSPuzzleItem
from puzzlestream.ui.moduledock import PSModuleDock
from puzzlestream.ui.moduleheader import PSModuleHeader
from puzzlestream.ui.modulestatusbar import PSModuleStatusbar
from puzzlestream.ui.modulewidget import PSModuleWidget


class PSModule(PSPuzzleItem):

    def __init__(self, moduleID, x, y, path, name,
                 streamSectionSupplier, libs):
        """
        =======================================================================
            Define GUI appearence: geometry and position
        """

        self.__width = 150
        self.__height = self.__width
        self.__dockingDepth = 25
        self.__dockingWidth = 60
        self.__headerDepth = 20
        self.__statusbarDepth = 20
        self.__widgetDepth = (self.__height - self.__headerDepth -
                              self.__statusbarDepth)
        self.__initposx, self.__initposy = 0, 0
        self._radius = self.__width / 2 + self.__dockingDepth

        super().__init__(moduleID)

        """
        =======================================================================
            Initialisation of backendstructure
        """

        self.lastID = None
        self.__inputPipe = None
        self.__path, self.__name = path, name
        self.__newStreamSection = streamSectionSupplier
        self.__libs = libs
        self.__process = None
        self.__inittime, self.__runtime, self.__savetime = 0, 0, 0
        self.__testResults = {}
        self.statusChanged.connect(self.headerColourUpdate)

        self.__stdout = ""
        self.__status = "incomplete"
        self.__errorMessage = ""

        self.__pathChanged = PSEvent()
        self.__nameChanged = PSEvent()
        self.__stdoutChanged = PSEvent()
        self.__progressChanged = PSEvent()

        """
        =======================================================================
            Initialise GUI modulecomponents:
                - Colored Header
                - Centralwidget with modulename, run- and stop-button
                - Colored Footer with statusbar
                - Dockingslots for pipeline connection
        """

        # Header
        self.__header = PSModuleHeader(
            self.__initposx, self.__initposy,
            self.__width, self.__headerDepth,
            "darkgreen", parent=self
        )

        self.__widget = PSModuleWidget(
            self.__initposx, self.__initposy + self.__headerDepth,
            self.__width,
            self.__height - self.__headerDepth - self.__statusbarDepth,
            parent=self
        )

        self.__widget.setPlayPauseButtonAction(self.__playPauseClicked)
        self.__widget.setStopButtonAction(self.__stopClicked)
        self.statusChanged.connect(self.__widget.updateTexts)

        self.__statusbar = PSModuleStatusbar(
            self.__initposx,
            self.__initposy + self.__headerDepth + self.__widgetDepth,
            self.__width, self.__statusbarDepth,
            "darkgreen", parent=self
        )

        self.__statusbar.text = "Testtext"

        self.__dock1 = PSModuleDock(
            self.__initposx,
            self.__initposy,
            self.__dockingWidth,
            self.__dockingDepth,
            self.__width,
            self.__height,
            "in",
            parent=self
        )

        self.__dock2 = PSModuleDock(
            self.__initposx,
            self.__initposy,
            self.__dockingWidth,
            self.__dockingDepth,
            self.__width,
            self.__height,
            "in",
            parent=self
        )

        self.__dock1.toTop()
        self.__dock2.toBottom()

        self.__dock1.hide()
        self.__dock2.hide()

        self.setCenterPos(QtCore.QPointF(x, y))

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def boundingRect(self):
        return QtCore.QRectF(self.__initposx, self.__initposy,
                             self.__width, self.__height)

    @property
    def saveProperties(self):
        props = {"name": self.name,
                 "path": self.path,
                 "stdout": self.stdout,
                 "errorMessage": self.errorMessage,
                 "inittime": self.inittime,
                 "runtime": self.runtime,
                 "savetime": self.savetime,
                 "testResults": self.testResults,
                 "dock1_state": self.__dock1.state,
                 "dock2_state": self.__dock2.state,
                 "dock1_position": self.__dock1.position,
                 "dock2_position": self.__dock2.position
                 }
        props.update(super().saveProperties)

        if self.__inputPipe is not None:
            props["inPipeID"] = self.__inputPipe.id

        return props

    def restoreProperties(self, props):
        super().restoreProperties(props)
        self.__stdout = props["stdout"]
        self.__errorMessage = props["errorMessage"]
        self.__inittime = props["inittime"]
        self.__runtime = props["runtime"]
        self.__testResults = props["testResults"]
        self.__savetime = props["savetime"]
        self.__dock1.state = props["dock1_state"]
        self.__dock2.state = props["dock2_state"]
        self.__dock1.position = props["dock1_position"]
        self.__dock2.position = props["dock2_position"]

    def importModule(self):
        try:
            for lib in self.__libs + [os.path.dirname(pslib.__file__)]:
                if not lib in sys.path:
                    sys.path.append(lib)
            spec = imp.util.spec_from_file_location(self.__name, self.filePath)
            self.mod = imp.util.module_from_spec(spec)
            spec.loader.exec_module(self.mod)
        except Exception as e:
            self.__errorMessage = traceback.format_exc()
            print(self.__errorMessage)
            self.status = "error"

    @property
    def __shift(self):
        return QtCore.QPointF(self.__width / 2, self.__height / 2)

    def centerPos(self):
        return self.scenePos() + self.__shift

    def setCenterPos(self, point):
        self.setPos(point - self.__shift)

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu()
        dataViewAction = QtWidgets.QAction("Show data")
        plotViewAction = QtWidgets.QAction("Show plots")
        deleteAction = QtWidgets.QAction("Delete module")

        dataViewAction.triggered.connect(self._requestDataView)
        plotViewAction.triggered.connect(self._requestPlotView)
        deleteAction.triggered.connect(self._requestDeletion)

        if self.streamSection is None:
            dataViewAction.setEnabled(False)
            plotViewAction.setEnabled(False)

        menu.addAction(dataViewAction)
        menu.addAction(plotViewAction)
        menu.addAction(deleteAction)
        action = menu.exec(event.screenPos())

    def moduledocktest(self):
        if self.__dock1.position == "top":
            self.__dock1.toRight()
        elif self.__dock1.position == "left":
            self.__dock1.toTop()
        elif self.__dock1.position == "right":
            self.__dock1.toBottom()
        elif self.__dock1.position == "bottom":
            self.__dock1.toLeft()

    def __playPauseClicked(self):
        if self.status == "running":
            self.pause()
        elif self.status == "paused":
            self.resume()
        else:
            self.run()
        self.selected.emit(self)
        self.setSelected(True)

    def __stopClicked(self):
        self.stop()
        self.selected.emit(self)
        self.setSelected(True)

    def headerColourUpdate(self, module):
        if self.status == "error":
            self.__header.bgColor = "darkred"
        elif self.status == "test failed":
            self.__header.bgColor = "yellow"
        elif self.status == "running":
            self.__header.bgColor = "green"
        elif self.status == "paused":
            self.__header.bgColor = "orange"
        else:
            self.__header.bgColor = "darkgreen"

    """
        properties
    """

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, path):
        self.__path = path
        self.pathChanged.emit()
        self.importModule()

    @property
    def filePath(self):
        return self.__path + "/" + self.__name + ".py"

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        os.rename(self.filePath, self.path + "/" + name + ".py")
        self.__name = name
        self.nameChanged.emit()

    @property
    def stdout(self):
        return self.__stdout

    def resetStdout(self):
        self.__stdout = ""
        self.stdoutChanged.emit(self, None)

    def addStdout(self, value):
        self.__stdout += value
        self.stdoutChanged.emit(self, value)

    @property
    def errorMessage(self):
        return self.__errorMessage

    @property
    def progress(self):
        return self.__progress

    @progress.setter
    def progress(self, value):
        self.__progress = value
        self.progressChanged.emit(self)

    @property
    def inittime(self):
        return self.__inittime

    @property
    def inittimeHHMMSS(self):
        m, s = divmod(self.__inittime, 60)
        h, m = divmod(m, 60)
        return "%02d:%02d:%02d.%003d" % (h, m, s, self.__inittime * 1000)

    @property
    def runtime(self):
        return self.__runtime

    @property
    def runtimeHHMMSS(self):
        m, s = divmod(self.__runtime, 60)
        h, m = divmod(m, 60)
        return "%02d:%02d:%02d.%003d" % (h, m, s, self.__runtime * 1000)

    @property
    def savetime(self):
        return self.__savetime

    @property
    def savetimeHHMMSS(self):
        m, s = divmod(self.__savetime, 60)
        h, m = divmod(m, 60)
        return "%02d:%02d:%02d.%003d" % (h, m, s, self.__savetime * 1000)

    @property
    def testResults(self):
        return self.__testResults

    @property
    def statistics(self):
        text = "Run time: %s<br>" % (self.runtimeHHMMSS)
        text += "Save time: %d ms<br><br>" % (self.savetime * 1000)

        if len(self.testResults) > 0:
            text += "Test report:<br>"

            for test in sorted(self.testResults):
                text += test + ": "
                if self.testResults[test]:
                    text += "<font color=\"green\">SUCCESSFULL</font><br>"
                else:
                    text += "<font color=\"red\">FAILED</font><br>"
        return text

    @property
    def pathChanged(self):
        return self.__pathChanged

    @property
    def nameChanged(self):
        return self.__nameChanged

    @property
    def stdoutChanged(self):
        return self.__stdoutChanged

    @property
    def progressChanged(self):
        return self.__progressChanged

    @property
    def header(self):
        return self.__header

    @property
    def dock1(self):
        return self.__dock1

    @property
    def dock2(self):
        return self.__dock2

    """
        routines
    """

    @property
    def inputPipe(self):
        return self.__inputPipe

    def setInputPipe(self, pipe):
        if isinstance(pipe, PSPipe):
            self.__inputPipe = pipe
            self.__inputPipe.statusChanged.connect(self.inputUpdate)
        else:
            raise TypeError

    def disconnectInputPipe(self):
        if self.__inputPipe is not None:
            self.__inputPipe.statusChanged.disconnect(self.inputUpdate)
            self.__inputPipe = None

    def inputUpdate(self, pipe):
        self.lastID = pipe.id

        if pipe.status == "finished":
            self.streamSection = pipe.streamSection.copy(self.id)
            self.run()

    def run(self):
        self.importModule()

        if (self.status != "running" and self.status != "paused" and
                "main" in self.mod.__dict__):
            thr = Thread(target=self.__run)
            thr.start()

    def pause(self):
        if self.__process is not None and self.status == "running":
            p = psutil.Process(self.__process.pid)
            p.suspend()
            self.status = "paused"

    def resume(self):
        if self.__process is not None and self.status == "paused":
            p = psutil.Process(self.__process.pid)
            p.resume()
            self.status = "running"

    def stop(self):
        if self.__process is not None and \
                (self.status == "running" or self.status == "paused"):
            if self.status == "paused":
                self.resume()
            self.__process.terminate()
            self.__finish(False, [], "Aborted by user.", [0, 0], {})
            self.addStdout("Aborted by user.")
            self.status = "incomplete"

    def __newPassword(self):
        return "".join(random.choice(string.ascii_letters) for i in range(20))

    def __run(self):
        self.resetStdout()

        t0 = time()
        if self.streamSection is None:
            self.streamSection = self.__newStreamSection(self.id)
        self.__inittime = time() - t0

        address = ("localhost", 10000 + self.id)
        authkey = bytes(self.__newPassword(), "utf-8")
        self.__listener = Listener(address, authkey=authkey)
        self.__process = mp.Process(
            target=self.__calculate,
            args=(self.streamSection, address, authkey)
        )
        self.status = "running"
        self.__process.start()
        sleep(0.01)
        self.__conn = self.__listener.accept()

        result = None
        while True:
            result = self.__conn.recv()
            if isinstance(result, str):
                self.addStdout(result)
            elif isinstance(result, float):
                self.progress = result
            else:
                self.__finish(*result)
                break

    def __finish(self, success, log, out, times, testResults):
        self.__conn.close()
        self.__listener.close()
        self.__process.join()
        self.__process, self.__listener, self.__conn = None, None, None

        self.__runtime, self.__savetime = times
        self.__testResults = testResults
        self.streamSection.changelog.update(log)

        if success == "successful":
            self.status = "finished"
        elif success == "test failed":
            self.__errorMessage = out
            self.status = "test failed"
        else:
            self.__errorMessage = out
            print(out)
            self.status = "error"

    def __calculate(self, streamSec, address, authkey):
        conn = Client(address, authkey=authkey)

        def sendPrint(*args, sep=" ", end="\n"):
            s, sep = "", str(sep)
            for a in args:
                s += str(a) + sep
            conn.send(s + end)

        def progressUpdate(finished, total=None):
            if total is None and isinstance(finished, float):
                if finished < 0:
                    finished = 0
                elif finished > 1:
                    finished = 1
                conn.send(finished)
            else:
                finished = finished / total
                progressUpdate(finished)

        np.random.seed(int.from_bytes(os.urandom(4), "big"))

        self.mod.print = sendPrint
        self.mod.progressUpdate = progressUpdate

        runtime, savetime, testResults = 0, 0, {}

        try:
            inp = streamSec.sectionDict

            t0 = time()
            out = self.mod.main(inp)
            runtime = time() - t0
            log = out.changelog

            t0 = time()
            inp.update(out)
            streamSec.updateData(self.lastID, self.id, inp, log)
            savetime = time() - t0

            success, output = "successful", ""

            if "testFunctions" in dir(self.mod):
                if isinstance(self.mod.testFunctions, list):
                    for func in self.mod.testFunctions:
                        result = getattr(self.mod, func)(out)

                        if isinstance(result, bool):
                            testResults[func] = result

            del out

        except Exception as e:
            message = traceback.format_exc()
            success, log, output = "error", [], message

        times = [runtime, savetime]

        conn.send([success, streamSec.changelog, output, times, testResults])
        conn.close()
