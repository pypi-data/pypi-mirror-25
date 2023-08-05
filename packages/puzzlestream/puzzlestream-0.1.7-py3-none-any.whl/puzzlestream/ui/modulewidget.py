from PyQt5 import QtWidgets


class PSModuleWidget(QtWidgets.QGraphicsProxyWidget):

    def __init__(self, initx, inity, width, height, parent=None):

        super().__init__(parent=parent)

        self.__width = width
        self.__height = height

        self.__widget = QtWidgets.QWidget()
        self.__centralgrid = QtWidgets.QGridLayout(self.__widget)
        self.__playpauseButton = QtWidgets.QPushButton()
        self.__stopButton = QtWidgets.QPushButton()
        self.__playpauseButton.setText("")
        self.__stopButton.setText("")
        self.__stopButton.setEnabled(False)

        self.__centralgrid.addWidget(self.__playpauseButton, 0, 0)
        self.__centralgrid.addWidget(self.__stopButton, 0, 1)

        self.__widget.setGeometry(initx, inity, self.__width, self.__height)

        self.setWidget(self.__widget)

    def setPlayPauseButtonAction(self, action):
        self.__playpauseButton.clicked.connect(action)

    def setStopButtonAction(self, action):
        self.__stopButton.clicked.connect(action)

    def togglePlayPauseEnabled(self):
        self.__playPauseButton.setEnabled(
            not self.__playPauseButton.isEnabled())

    def toggleStopEnabled(self):
        self.__stopButton.setEnabled(not self.__stopButton.isEnabled())

    def updateTexts(self, module):
        if module.status == "running":
            self.__playpauseButton.setText("Pause")
            self.__stopButton.setEnabled(True)
        elif module.status == "paused":
            self.__playpauseButton.setText("Resume")
            self.__stopButton.setEnabled(True)
        else:
            self.__playpauseButton.setText("Run")
            self.__stopButton.setEnabled(False)
