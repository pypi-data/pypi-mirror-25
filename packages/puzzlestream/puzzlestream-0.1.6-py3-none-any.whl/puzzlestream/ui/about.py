from PyQt5 import QtWidgets


class PSAboutWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.label = QtWidgets.QLabel()
        self.label.setText("Hier kommt der Text hin.")
        self.setCentralWidget(self.label)
        self.show()
