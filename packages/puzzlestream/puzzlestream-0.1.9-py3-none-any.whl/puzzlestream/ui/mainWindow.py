import os
import shutil
import subprocess
import sys
import time

import psutil
from pyqode.python.backend import server
from pyqode.python.widgets import PyCodeEdit
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMenu

from puzzlestream import pslib
from puzzlestream.ui.about import PSAboutWindow
from puzzlestream.ui.dataview import PSDataView
from puzzlestream.ui.mainWindowUi_02 import Ui_MainWindow
from puzzlestream.ui.manager import PSManager
from puzzlestream.ui.module import PSModule
from puzzlestream.ui.pipe import PSPipe
from puzzlestream.ui.plotview import PSPlotView
from puzzlestream.ui.preferences import PSPreferencesWindow


class PSMainWindow(QtWidgets.QMainWindow):

    def __init__(self):

        super().__init__()

        self.__manager = PSManager()
        self.__manager.configChanged.connect(self.__configChanged)

        self.__designerUI = Ui_MainWindow()
        self.__designerUI.setupUi(self)

        self.__editor = PyCodeEdit(
            server_script=server.__file__,
            args=["-s" + os.path.dirname(pslib.__file__)]
        )
        self.__editor.save_on_focus_out = True
        self.__editor.hide()
        self.__designerUI.editorFilePathLabel.hide()
        self.__designerUI.vertEditorLayout.addWidget(self.__editor)

        actionList = self.__createToolBarActions()
        for action in actionList:
            self.__designerUI.toolBar.addAction(action)

        self.__designerUI.toolBar.setMovable(False)
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                             QtWidgets.QSizePolicy.Preferred)
        self.__designerUI.toolBar.insertSeparator(actionList[2])
        self.__designerUI.toolBar.insertSeparator(actionList[7])
        self.__designerUI.toolBar.insertWidget(actionList[-3], spacer)

        self.__designerUI.horizontalSplitter.setStretchFactor(0, 5)
        self.__designerUI.horizontalSplitter.setStretchFactor(1, 8)

        self.__designerUI.verticalSplitter.setStretchFactor(0, 1000)
        self.__designerUI.verticalSplitter.setStretchFactor(1, 1)

        self.__createFileMenuActions()
        self.__createEditMenuActions()
        self.__createViewMenuActions()
        self.__createStreamMenuActions()
        self.__createHelpMenuActions()
        self.__createGraphicsScene()
        self.__designerUI.puzzleGraphicsView.setScene(self.__manager.scene)

        if len(self.__manager.config["last projects"]) > 0:
            self.__openProject(self.__manager.config["last projects"][-1])

        self.__createLibMenuActions()

        """
        =======================================================================
            Timer for CPU and RAM update
        """

        self.__loadViewer = QtWidgets.QLabel(self.__designerUI.statusbar)
        self.__designerUI.statusbar.addPermanentWidget(self.__loadViewer)
        self.__loadTimer = QtCore.QTimer(self)
        self.__loadTimer.setInterval(3000)
        self.__loadTimer.timeout.connect(self.__updateLoad)
        self.__updateLoad()
        self.__loadTimer.start()

        """
        =======================================================================
            Show window
        """

        self.showMaximized()
        self.__lastWindowState = "maximized"

        """
        =======================================================================
            Start testing
        """

        self.__test = "test" in sys.argv

        if self.__test:
            self.__runTest()

    def closeEvent(self, event):
        if self.__manager.projectPath is not None:
            self.__manager.save(thread=False)
            self.__editor.file.save()
            self.__manager.stream.close()
        event.accept()

    def __resetUI(self, path):
        self.__editor.hide()
        self.__designerUI.editorFilePathLabel.hide()
        self.__designerUI.outputTextEdit.setText("")

    def __createGraphicsScene(self):
        scene = self.__manager.scene
        scene.stdoutChanged.connect(self.updateText)
        scene.statusChanged.connect(self.updateStatus)
        scene.itemAdded.connect(self.__enableAddActions)
        scene.dataViewRequested.connect(self.__showData)
        scene.plotViewRequested.connect(self.__showPlots)
        scene.selectionChanged.connect(self.__selectionChanged)
        return scene

    def __selectionChanged(self, puzzleItem):
        if isinstance(puzzleItem, PSModule):
            self.__editor.file.open(puzzleItem.filePath)
            self.__designerUI.editorFilePathLabel.setText(puzzleItem.filePath)
            self.__designerUI.outputTextEdit.setText(puzzleItem.stdout)
            self.__designerUI.statisticsTextEdit.setHtml(puzzleItem.statistics)
            self.__designerUI.outputTabWidget.setTabText(
                0, "Output - " + puzzleItem.name)
            self.__editor.show()
            self.__designerUI.editorFilePathLabel.show()

    def __createFileMenuActions(self):
        newProjectAction = self.__designerUI.menuFile.addAction("&New project")
        openProjectAction = self.__designerUI.menuFile.addAction(
            "&Open project")
        saveprojectAsAction = self.__designerUI.menuFile.addAction(
            "&Save project as...")

        newProjectAction.triggered.connect(self.__newProject)
        openProjectAction.triggered.connect(self.__openProject)
        saveprojectAsAction.triggered.connect(self.__saveProjectAs)

        self.__recentProjectsMenu = QtWidgets.QMenu("Recent projects")
        self.__designerUI.menuFile.insertMenu(saveprojectAsAction,
                                              self.__recentProjectsMenu)

    def __createEditMenuActions(self):
        undoAction = self.__designerUI.menuEdit.addAction("&Undo")
        redoAction = self.__designerUI.menuEdit.addAction("&Redo")
        undoRedoSeparator = self.__designerUI.menuEdit.addSeparator()
        cutAction = self.__designerUI.menuEdit.addAction("&Cut")
        copyAction = self.__designerUI.menuEdit.addAction("&Copy")
        pasteAction = self.__designerUI.menuEdit.addAction("&Paste")
        cutCopyPasteSeparator = self.__designerUI.menuEdit.addSeparator()
        preferencesAction = self.__designerUI.menuEdit.addAction(
            "Pre&ferences")

        undoAction.triggered.connect(self.__editor.undo)
        redoAction.triggered.connect(self.__editor.redo)
        cutAction.triggered.connect(self.__editor.cut)
        copyAction.triggered.connect(self.__editor.copy)
        pasteAction.triggered.connect(self.__editor.paste)
        preferencesAction.triggered.connect(self.__showPreferences)

    def __createViewMenuActions(self):
        fullscreenAction = self.__designerUI.menuView.addAction(
            "&Toggle fullscreen")
        fullscreenAction.triggered.connect(self.__toggleFullscreen)

    def __createLibMenuActions(self):
        self.__designerUI.menuLib.clear()
        self.__addLibAction = self.__designerUI.menuLib.addAction(
            "Add lib path")
        self.__libSeparator = self.__designerUI.menuLib.addSeparator()
        self.__addLibAction.triggered.connect(self.__addLib)

        for path in self.__manager.libs:
            menu = self.__designerUI.menuLib.addMenu(path)
            openAction = menu.addAction("Open folder")
            openAction.triggered.connect(lambda: self.__open_file(path))
            deleteAction = menu.addAction("Delete")
            deleteAction.triggered.connect(lambda: self.__deleteLib(path))

    def __createStreamMenuActions(self):
        dataAction = self.__designerUI.menuStream.addAction("Show &data")
        plotAction = self.__designerUI.menuStream.addAction("Show &plots")
        self.__designerUI.menuStream.addSeparator()
        cleanAction = self.__designerUI.menuStream.addAction(
            "&Clean stream")

        dataAction.triggered.connect(self.__showStreamDataView)
        plotAction.triggered.connect(self.__showStreamPlotView)
        cleanAction.triggered.connect(self.__clearStream)

    def __createHelpMenuActions(self):
        aboutAction = self.__designerUI.menuHelp.addAction(
            "&About Puzzle Stream")
        aboutAction.triggered.connect(self.__showAboutWindow)

    def __toggleFullscreen(self):
        if self.isFullScreen():
            if self.__lastWindowState == "maximized":
                self.showMaximized()
            else:
                self.showNormal()
        else:
            if self.isMaximized():
                self.__lastWindowState = "maximized"
            else:
                self.__lastWindowState = "normal"
            self.showFullScreen()

    def __showPreferences(self):
        preferences = PSPreferencesWindow(self.__manager.config, self)
        preferences.show()

    def __showStreamDataView(self):
        viewer = PSDataView(self.__manager.stream, self)

    def __showStreamPlotView(self):
        viewer = PSPlotView(self.__manager.stream, self.__manager.config, self)

    def __clearStream(self):
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirm clean up",
            "Are you sure you want to erase ALL data from the stream?",
            QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes
        )

        if reply == QtWidgets.QMessageBox.Yes:
            self.__manager.stream.clear()

    def __showAboutWindow(self):
        about = PSAboutWindow(self)

    def __updateRecentProjects(self):
        self.__recentProjectsMenu.clear()

        for item in self.__manager.config["last projects"][::-1]:
            action = self.__recentProjectsMenu.addAction(item)
            action.triggered.connect(
                lambda x, item=item: self.__openProject(item))

    def __createToolBarActions(self):
        currentDir = os.path.dirname(__file__)

        self.__openProjectAction = QAction(
            QIcon(os.path.join(currentDir, "../icons//folder.svg")),
            'Open project', self
        )

        self.__saveFileAction = QAction(
            QIcon(os.path.join(currentDir, "../icons//save.svg")),
            'Save file', self
        )

        self.__undoAction = QAction(
            QIcon(os.path.join(currentDir, "../icons//back.svg")),
            'Back', self
        )

        self.__redoAction = QAction(
            QIcon(os.path.join(currentDir, "../icons//forward.svg")),
            'Forward', self
        )

        self.__copyAction = QAction(
            QIcon(os.path.join(currentDir, "../Icons//copy.png")),
            'Copy', self
        )

        self.__cutAction = QAction(
            QIcon(os.path.join(currentDir, "../Icons//cut.png")),
            'Cut', self
        )

        self.__pasteAction = QAction(
            QIcon(os.path.join(currentDir, "../Icons//paste.png")),
            'Paste', self
        )

        self.__runAction = QAction(
            QIcon(os.path.join(currentDir, "../icons/play.svg")),
            'Run puzzle', self
        )

        self.__stopAction = QAction(
            QIcon(os.path.join(currentDir, "../icons//stop.svg")),
            'Stop puzzle', self
        )

        self.__newModuleMenu = QMenu("New module", self)
        self.__newIntModuleAction = self.__newModuleMenu.addAction(
            "New internal module")
        self.__newExtModuleAction = self.__newModuleMenu.addAction(
            "New external module")
        self.__newPipeAction = QAction("New pipe", self)
        self.__newValveAction = QAction("New valve", self)

        self.__openProjectAction.triggered.connect(self.__openProject)
        self.__saveFileAction.triggered.connect(self.__saveFileToolbar)
        self.__undoAction.triggered.connect(self.__editor.undo)
        self.__redoAction.triggered.connect(self.__editor.redo)
        self.__copyAction.triggered.connect(self.__editor.copy)
        self.__cutAction.triggered.connect(self.__editor.cut)
        self.__pasteAction.triggered.connect(self.__editor.paste)
        self.__runAction.triggered.connect(self.__run)
        self.__stopAction.triggered.connect(self.__stop)
        self.__newModuleMenu.menuAction().triggered.connect(
            self.__newIntModule)
        self.__newIntModuleAction.triggered.connect(self.__newIntModule)
        self.__newExtModuleAction.triggered.connect(self.__newExtModule)
        self.__newPipeAction.triggered.connect(self.__newPipe)
        self.__newValveAction.triggered.connect(self.__newValve)

        return [self.__openProjectAction, self.__saveFileAction,
                self.__undoAction, self.__redoAction,
                self.__copyAction, self.__cutAction, self.__pasteAction,
                self.__runAction, self.__stopAction,
                self.__newModuleMenu.menuAction(), self.__newPipeAction,
                self.__newValveAction]

    def updateText(self, module, text):
        if module.isSelected():
            if text is None:
                self.__designerUI.outputTextEdit.setText("")
            else:
                cursor = self.__designerUI.outputTextEdit.textCursor()
                cursor.movePosition(cursor.End)
                cursor.insertText(text)

    def updateStatus(self, module):
        if module.isSelected():
            self.__designerUI.statisticsTextEdit.setHtml(module.statistics)

    def __updateLoad(self):
        vm = psutil.virtual_memory()

        self.__loadViewer.setText(
            (str(psutil.cpu_percent()) +
             "% CPU  " +
             "%.1f" % (vm.used / vm.total * 100) +
             "% RAM  " +
             time.strftime("%H:%M"))
        )

    def __configChanged(self, key):
        if key == "last projects":
            self.__updateRecentProjects()

    """
        reaction routines
    """

    def __newProject(self, path=None):
        if not isinstance(path, str):
            path = QtWidgets.QFileDialog.getExistingDirectory(
                self,
                "New project folder")

        if path != "":
            if len(os.listdir(path)) == 0:
                self.__manager.newProject(path)
                self.setWindowTitle(
                    "Puzzle Stream - " + self.__manager.projectPath)
                self.__editor.hide()
                self.__designerUI.editorFilePathLabel.hide()
                self.__designerUI.outputTextEdit.setText("")
            else:
                msg = QtWidgets.QMessageBox(self)
                msg.setText("Directory not empty.")
                msg.show()

    def __openProject(self, path=None):
        if not isinstance(path, str):
            path = QtWidgets.QFileDialog.getExistingDirectory(
                self,
                "Open project folder")

        if os.path.isdir(path) and os.path.isfile(path + "/puzzle.json"):
            self.__manager.load(path)
            self.setWindowTitle("Puzzle Stream - " + path)
            self.__resetUI(path)

    def __saveProjectAs(self, path=None):
        if not isinstance(path, str):
            path = QtWidgets.QFileDialog.getExistingDirectory(
                self,
                "Save project folder")

        if os.path.isdir(path):
            if len(os.listdir(path)) == 0:
                self.__manager.saveAs(path)
                self.setWindowTitle("Puzzle Stream - " + path)
                self.__resetUI(path)
            else:
                msg = QtWidgets.QMessageBox(self)
                msg.setText("Directory not empty.")
                msg.show()

    def __saveFileToolbar(self, value):
        self.__editor.file.save()

    def __newIntModule(self):
        self.__disableAddActions()
        self.__manager.addStatus = "intModule"

    def __newExtModule(self):
        self.__disableAddActions()
        self.__manager.addStatus = "extModule"

    def __newPipe(self):
        self.__disableAddActions()
        self.__manager.addStatus = "pipe"

    def __newValve(self):
        self.__disableAddActions()
        self.__manager.addStatus = "valve"

    def __enableAddActions(self, item):
        for a in (self.__newModuleMenu, self.__newPipeAction,
                  self.__newValveAction):
            a.setEnabled(True)

    def __disableAddActions(self):
        for a in (self.__newModuleMenu, self.__newPipeAction,
                  self.__newValveAction):
            a.setDisabled(True)

    def __showData(self, puzzleItem):
        dataview = PSDataView(puzzleItem.streamSection.data, self)

    def __showPlots(self, puzzleItem):
        plotview = PSPlotView(puzzleItem.streamSection.data,
                              self.__manager.config, self)

    def __run(self):
        for module in self.__manager.scene.modules.values():
            if module.inputPipe is None:
                module.run()

    def __stop(self):
        for module in self.__manager.scene.modules.values():
            module.stop()

    """
    ===========================================================================
        Lib stuff
    """

    def __addLib(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                          "Add lib folder")
        if os.path.isdir(path):
            self.__manager.addLib(path)

            args = ["-s" + os.path.dirname(pslib.__file__)]
            for lib in self.__manager.libs:
                args.append("-s" + lib)

            self.__editor.backend.start(
                server.__file__, args=args)
            self.__createLibMenuActions()

    def __open_file(self, filename):
        if sys.platform == "win32":
            os.startfile(filename)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, filename])

    def __deleteLib(self, path):
        self.__manager.deleteLib(path)
        self.__createLibMenuActions()

    """
    ===========================================================================
        Testing
    """

    def __runTest(self):
        self.__testNewProject()
        module = self.__testNewIntModule()
        pipe = self.__testNewPipe()

        self.close()
        sys.exit()

    def __testNewProject(self):
        path = os.path.abspath("./testproject")

        if not os.path.isdir(path):
            os.mkdir(path)
            print("directory created")

        self.__newProject(path)
        print("new project created")

    def __testNewIntModule(self):
        self.__newIntModule()
        press = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonPress,
                                  QtCore.QPointF(1500, 400),
                                  QtCore.Qt.LeftButton,
                                  QtCore.Qt.LeftButton,
                                  QtCore.Qt.NoModifier)
        self.__designerUI.puzzleGraphicsView.mousePressEvent(press)

        for item in self.__manager.scene.modules.values():
            module = item
        print("module", str(module), "created")
        return module

    def __testNewPipe(self):
        self.__newPipe()
        press = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonPress,
                                  QtCore.QPointF(1300, 400),
                                  QtCore.Qt.LeftButton,
                                  QtCore.Qt.LeftButton,
                                  QtCore.Qt.NoModifier)

        self.__designerUI.puzzleGraphicsView.mousePressEvent(press)

        for item in self.__manager.scene.pipes.values():
            pipe = item
        print("pipe", str(pipe), "created")
        return pipe
