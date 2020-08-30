#This starts the version of the project that is needed
import os
from PyQt5 import QtCore, QtGui, QtWidgets

from Resources.MainWindowNoSpotifyTest import Ui_MainWindowNoSpotify
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindowNoSpotify = QtWidgets.QMainWindow()
    ui = Ui_MainWindowNoSpotify()
    ui.setupUi(MainWindowNoSpotify)
    MainWindowNoSpotify.show()
    sys.exit(app.exec_())
