from PySide import QtGui, QtCore
from dashboard_tab import DashboardTab

class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.tabs = None
        self.setWindowTitle('Valar Morghulis')
        self.setWindowIcon(QtGui.QIcon('./view/images/favicon.jpg'))
        # x-position, y-position, width, height
        self.setGeometry(350, 150, 720, 480)

        self.main_model = None

        self.initialize()

        self.show()

    def initialize(self):
        self.tabs = QtGui.QTabWidget()
        self.tabs.addTab(DashboardTab(), "Dashboard")
        self.tabs.addTab(QtGui.QLabel("STH"), "Houses")
        self.tabs.addTab(QtGui.QLabel("STH"), "Characters")
        self.setCentralWidget(self.tabs)
