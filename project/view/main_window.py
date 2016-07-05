from PySide import QtGui, QtCore
from dashboard_tab import DashboardTab
from characters_tab import CharactersTab
from houses_tab import HousesTab
from configuration_tab import ConfigurationTab


class MainWindow(QtGui.QMainWindow):
    def __init__(self, neural_network):
        super(MainWindow, self).__init__()
        self.neural_network = neural_network
        self.tabs = None
        self.setWindowTitle('Valar Morghulis')
        self.setWindowIcon(QtGui.QIcon('./view/images/favicon.jpg'))
        # x-position, y-position, width, height
        self.setGeometry(350, 150, 1170, 600)
        self.dashboard_tab = None
        self.main_model = None

        self.initialize()


    def initialize(self):
        self.tabs = QtGui.QTabWidget()
        self.tabs.currentChanged.connect(self.selector)
        self.dashboard_tab = DashboardTab(self.neural_network)
        self.tabs.addTab(self.dashboard_tab, "Dashboard")
        self.tabs.addTab(CharactersTab(self.neural_network), "Characters")
        self.tabs.addTab(HousesTab(), "Houses")
        self.tabs.addTab(ConfigurationTab(self.neural_network), "NN configuration")
        self.setCentralWidget(self.tabs)

    def selector(self, selected_index):
        print("selector")
        if selected_index == 0:
            self.dashboard_tab.update()
        else:
            pass