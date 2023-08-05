#!/usr/bin/python3

import sys
from PyQt5 import QtWidgets
from puzzlestream.ui.mainWindow import PSMainWindow


def main():
    """ Create Application and MainWindow """
    app = QtWidgets.QApplication(sys.argv)
    psMainWindow = PSMainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
