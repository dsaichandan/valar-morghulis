'''
Valar Morghulis Team
   SW  3-2013    Stefan Ristanovic
   SW  8-2013    Stefan Bratic
'''
from PySide import QtCore
from PySide import QtGui
from model.KerasWrapper import KerasWrapper
from model.parameters import Parameters
import sys

from view.main_window import MainWindow  # @NoMove

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)



    # pixmap = QtGui.QPixmap('./../poster_data/Valar-Morghulis.png')
    pixmap = QtGui.QPixmap('./../poster_data/havran_super.png')
    pixmap = pixmap.scaled(QtCore.QSize(600, 400), aspectMode=QtCore.Qt.KeepAspectRatio,
                           mode=QtCore.Qt.SmoothTransformation)
    splash = QtGui.QSplashScreen(pixmap, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(pixmap.mask())
    app.processEvents()
    splash.show()
    neural_network = KerasWrapper()
    #neural_network.run_for_all_characters()
    #neural_network.raw_data.to_csv('./../datasets/cleaned_data.csv')
    app.setStyle('Plastique')
    ex = MainWindow(neural_network)
    ex.show()
    splash.finish(ex)

    sys.exit(app.exec_())
