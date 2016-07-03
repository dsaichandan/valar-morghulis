from PySide import QtGui
from project.model.ResultTableModel import *


class ConfigurationTab(QtGui.QWidget):
    def __init__(self, neural_network, parent=None):
        super(ConfigurationTab, self).__init__(parent)

        self.training_status = ['Not working', 'In progress', 'Completed']
        self.status = self.training_status[0]
        self.loss_value = 'NaN'
        self.accuracy_value = 'NaN'
        self.headers_data = ['Character name', 'Dead (%)', 'Alive (%)']
        self.table_data = []

        self.neural_network = neural_network

        grid = QtGui.QGridLayout()

        constants_group_box = QtGui.QGroupBox("Constants configuration")
        constants_layout = self.__create_constants_area()
        constants_group_box.setLayout(constants_layout)

        status_group_box = QtGui.QGroupBox("Neural network status")
        status_layout = self.__create_training_results_area()
        status_group_box.setLayout(status_layout)

        train_button = QtGui.QPushButton("Start NN training", self)
        train_button.clicked.connect(self.train_neural_network)

        result_group_box = QtGui.QGroupBox('Prediction results')
        result_layout = self.__create_result_area()
        result_group_box.setLayout(result_layout)

        grid.addWidget(constants_group_box, 0, 0)
        grid.addWidget(status_group_box, 1, 0)
        grid.addWidget(train_button, 2, 0)
        grid.addWidget(result_group_box, 0, 1)

        self.setLayout(grid)

    def train_neural_network(self):
        self.status = self.training_status[1]
        self.__refresh_data()
        loss, accuracy = self.neural_network.start_whole_process()
        self.loss_value = str(loss) + ' %'
        self.accuracy_value = str(accuracy) + ' %'
        self.status = self.training_status[2]
        self.table_data = self.neural_network.prediction()
        self.__refresh_data(table=True)

    def __create_constants_area(self):
        layout = QtGui.QFormLayout()
        batch_size_edit = QtGui.QLineEdit(self)
        batch_size_label = QtGui.QLabel("Batch size: ", self)
        batch_size_label.setBuddy(batch_size_edit)
        batch_size_edit.setText(str(self.neural_network.params.batch_size))

        number_of_nodes_edit = QtGui.QLineEdit(self)
        number_of_nodes_label = QtGui.QLabel("Number of nodes per layer: ", self)
        number_of_nodes_label.setBuddy(number_of_nodes_edit)
        number_of_nodes_edit.setText(str(self.neural_network.params.nodes))

        epochs_edit = QtGui.QLineEdit(self)
        epochs_label = QtGui.QLabel("Number of epochs: ", self)
        epochs_label.setBuddy(epochs_edit)
        epochs_edit.setText(str(self.neural_network.params.epochs))

        early_stopping = QtGui.QCheckBox("Enable early stopping ", self)
        early_stopping.setChecked(self.neural_network.params.early)

        patience_edit = QtGui.QLineEdit(self)
        patience_label = QtGui.QLabel("Patience level: ", self)
        patience_label.setBuddy(patience_edit)
        patience_edit.setText(str(self.neural_network.params.patience))

        layout.addRow(batch_size_label, batch_size_edit)
        layout.addRow(number_of_nodes_label, number_of_nodes_edit)
        layout.addRow(epochs_label, epochs_edit)
        layout.addRow(early_stopping)
        layout.addRow(patience_label, patience_edit)

        return layout

    def __create_training_results_area(self):
        layout = QtGui.QFormLayout()

        status_label = QtGui.QLabel("Training status: ", self)
        self.status_value_label = QtGui.QLabel(self.status, self)
        status_label.setBuddy(self.status_value_label)

        loss_label = QtGui.QLabel("Loss : ", self)
        self.loss_value_label = QtGui.QLabel(self.loss_value, self)
        loss_label.setBuddy(self.loss_value_label)

        accuracy_label = QtGui.QLabel("Accuracy: ", self)
        self.accuracy_value_label = QtGui.QLabel(self.accuracy_value, self)
        accuracy_label.setBuddy(self.accuracy_value_label)

        layout.addRow(status_label, self.status_value_label)
        layout.addRow(loss_label, self.loss_value_label)
        layout.addRow(accuracy_label, self.accuracy_value_label)

        return layout

    def __create_result_area(self):
        self.table_model = ResultTableModel(self, self.table_data, self.headers_data)
        self.table_view = QtGui.QTableView()
        self.table_view.setModel(self.table_model)
        self.table_view.setSortingEnabled(True)
        self.table_view.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.table_view)
        return layout

    def __refresh_data(self, table=False):
        self.accuracy_value_label.setText(self.accuracy_value)
        self.loss_value_label.setText(self.loss_value)
        self.status_value_label.setText(self.status)
        if (table):
            self.table_model.changeData(self.table_data)
