import sys

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

from fgoc_ui import Ui_MainWindow

class MainWindow( qtw.QMainWindow ):

    def __init__( self, *args, **kwargs ):
        # run parent initialization
        super().__init__( *args, **kwargs )

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.show()

    def callBack( self ):
        print('Hi')

if __name__ == '__main__':

    app = qtw.QApplication( sys.argv )

    w = MainWindow(windowTitle = 'Hello World!')

    sys.exit( app.exec_() )