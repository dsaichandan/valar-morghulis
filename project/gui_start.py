'''
Valar Morghulis Team
   SW  3-2013    Stefan Ristanovic
   SW  8-2013    Stefan Bratic
'''

from PySide import QtGui
import sys

from view.main_window import MainWindow  # @NoMove

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()

    sys.exit(app.exec_())

