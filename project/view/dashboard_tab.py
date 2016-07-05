# coding=utf-8
from PySide import QtGui, QtCore
from project.model.ResultTableModel import *

class DashboardTab(QtGui.QWidget):
    def __init__(self, neural_network, parent=None):
        super(DashboardTab, self).__init__(parent)
        self.neural_network = neural_network
        grid = QtGui.QGridLayout()
        # ------ AUTHORS ------- #
        authors_box = QtGui.QGroupBox("About authors")
        authors_layout = QtGui.QVBoxLayout()
        first_box = QtGui.QGroupBox("SW3/2013")
        first_layout = QtGui.QVBoxLayout()
        first_layout.addWidget(QtGui.QLabel("Stefan Ristanovic"))
        first_layout.addWidget(QtGui.QLabel("st.keky@gmail.com"))
        first_layout.addWidget(QtGui.QLabel("House Ristark"))
        first_box.setLayout(first_layout)
        second_box = QtGui.QGroupBox("SW8/2013")
        second_layout = QtGui.QVBoxLayout()
        second_layout.addWidget(QtGui.QLabel("Stefan Bratic"))
        second_layout.addWidget(QtGui.QLabel("cobrijani@gmail.com"))
        second_layout.addWidget(QtGui.QLabel("House Bratheon"))
        second_box.setLayout(second_layout)
        authors_layout.addWidget(first_box)
        authors_layout.addWidget(second_box)
        authors_box.setLayout(authors_layout)

        # DATASETS INFO #
        info_box = QtGui.QGroupBox("Data info")
        info_layout = QtGui.QVBoxLayout()

        info_layout.addWidget(QtGui.QLabel("Total battles:\t\t" + str(self.neural_network.data_cleaner.battles_csv.name.size)))
        info_layout.addWidget(QtGui.QLabel("Total characters:\t\t" + str(self.neural_network.data_cleaner.characters_csv.name.size)))
        info_layout.addWidget(QtGui.QLabel("Total houses:\t\t" + str(self.neural_network.data_cleaner.houses_json.name.size)))
        info_layout.addWidget(QtGui.QLabel("Total cultures:\t\t" + str(self.neural_network.data_cleaner.cultures_json.name.size)))
        info_box.setLayout(info_layout)

        # TOP 7 to DIE #
        die_box = QtGui.QGroupBox("Top 7 to die")
        self.table_data_die = []
        self.headers = ["Name", "Death rate"]

        self.table_model_die = ResultTableModel(die_box, self.table_data_die, self.headers)
        self.table_view = QtGui.QTableView()
        self.table_view.setModel(self.table_model_die)
        self.table_view.setSortingEnabled(True)
        self.table_view.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

        die_layout = QtGui.QVBoxLayout()
        die_layout.addWidget(self.table_view)
        die_box.setLayout(die_layout)
        grid.addWidget(die_box, 0, 0)

        # TOP 7 to LIVE #
        live_box = QtGui.QGroupBox("Top 7 to live")
        self.table_data_live = []
        if self.neural_network.train_completed:
            data = self.neural_network.raw_data.sort_values('death', ascending=False)
            top_7 = data.head(7)
            print(top_7)
        self.headers_live = ["Name", "Live rate"]

        self.table_model_live = ResultTableModel(live_box, self.table_data_live, self.headers_live)
        self.table_view_live = QtGui.QTableView()
        self.table_view_live.setModel(self.table_model_live)
        self.table_view_live.setSortingEnabled(True)
        self.table_view_live.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

        live_layout = QtGui.QVBoxLayout()
        live_layout.addWidget(self.table_view_live)
        live_box.setLayout(live_layout)
        grid.addWidget(die_box, 0, 0)
        grid.addWidget(live_box, 0, 1)
        grid.addWidget(authors_box, 1, 0)
        grid.addWidget(info_box, 1, 1)
        self.setLayout(grid)

    def update(self):
        print("update")
        if self.neural_network.train_completed:
            data = self.neural_network.raw_data.sort_values('death', ascending=False)
            top_7 = data.head(7)
            print(top_7)
