import sys
from PyQt5 import QtWidgets
from puzzlestream.ui.mainWindow import PSMainWindow


def main():
    """ Create Application and MainWindow """
    global app, psMainWindow
    app = QtWidgets.QApplication(sys.argv)
    psMainWindow = PSMainWindow()
    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())
