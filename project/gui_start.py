'''
Valar Morghulis Team
   SW  3-2013    Stefan Ristanovic
   SW  8-2013    Stefan Bratic
'''

from PySide import QtGui
from model.KerasWrapper import KerasWrapper
from model.parameters import Parameters
import sys

from view.main_window import MainWindow  # @NoMove

if __name__ == '__main__':
    neural_network = KerasWrapper()
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow(neural_network)

    sys.exit(app.exec_())
