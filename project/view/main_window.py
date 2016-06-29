from PySide import QtGui, QtCore


class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('Valar Morghulis')
        self.setWindowIcon(QtGui.QIcon('./view/images/favicon.jpg'))
        # x-position, y-position, width, height
        self.setGeometry(350, 150, 720, 480)

        self.main_model = None

        self.initialize()

        self.show()

    def initialize(self):
        pass
