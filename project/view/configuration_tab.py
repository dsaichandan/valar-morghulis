from PySide import QtGui
from project.model.ResultTableModel import *
import pandas as pd


class ConfigurationTab(QtGui.QWidget):
    def __init__(self, neural_network, parent=None):
        super(ConfigurationTab, self).__init__(parent)

        self.training_status = ['Not working', 'In progress', 'Completed']
        self.status = self.training_status[0]
        self.loss_value = 'NaN'
        self.accuracy_value = 'NaN'
        self.headers_data = ['Character name', 'Dead (%)', 'Alive (%)']
        self.table_data = []
        self.character_count = 0

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

        character = QtGui.QGroupBox('Character selection')
        character_layout = self.__create_character_selection_area()
        character.setLayout(character_layout)

        grid.addWidget(constants_group_box, 0, 0)
        grid.addWidget(status_group_box, 1, 0)
        grid.addWidget(train_button, 2, 0)
        grid.addWidget(character, 0, 1)
        grid.addWidget(result_group_box, 1, 1)

        self.setLayout(grid)

    def train_neural_network(self):
        self.status = self.training_status[1]
        self.__refresh_data()
        loss, accuracy = self.neural_network.start_whole_process()
        self.loss_value = str(loss * 100) + ' %'
        self.accuracy_value = str(accuracy * 100) + ' %'
        self.status = self.training_status[2]
        self.table_data = self.neural_network.prediction()
        self.__refresh_data(table=True)

    def __create_constants_area(self):
        layout = QtGui.QFormLayout()
        self.batch_size_edit = QtGui.QLineEdit(self)
        batch_size_label = QtGui.QLabel("Batch size: ", self)
        batch_size_label.setBuddy(self.batch_size_edit)
        self.batch_size_edit.setText(str(self.neural_network.params.batch_size))

        self.number_of_nodes_edit = QtGui.QLineEdit(self)
        number_of_nodes_label = QtGui.QLabel("Number of nodes per layer: ", self)
        number_of_nodes_label.setBuddy(self.number_of_nodes_edit)
        self.number_of_nodes_edit.setText(str(self.neural_network.params.nodes))

        self.epochs_edit = QtGui.QLineEdit(self)
        epochs_label = QtGui.QLabel("Number of epochs: ", self)
        epochs_label.setBuddy(self.epochs_edit)
        self.epochs_edit.setText(str(self.neural_network.params.epochs))

        self.early_stopping = QtGui.QCheckBox("Enable early stopping ", self)
        self.early_stopping.setChecked(self.neural_network.params.early)

        self.patience_edit = QtGui.QLineEdit(self)
        patience_label = QtGui.QLabel("Patience level: ", self)
        patience_label.setBuddy(self.patience_edit)
        self.patience_edit.setText(str(self.neural_network.params.patience))

        save_button = QtGui.QPushButton('Save configuration', self)
        reset_defaults_button = QtGui.QPushButton('Reset defaults', self)
        save_button.clicked.connect(self.save_configuration)
        reset_defaults_button.clicked.connect(self.reset_defaults)

        layout.addRow(batch_size_label, self.batch_size_edit)
        layout.addRow(number_of_nodes_label, self.number_of_nodes_edit)
        layout.addRow(epochs_label, self.epochs_edit)
        layout.addRow(self.early_stopping)
        layout.addRow(patience_label, self.patience_edit)
        layout.addRow(save_button)
        layout.addRow(reset_defaults_button)

        return layout

    def save_configuration(self):
        batch_size = self.batch_size_edit.text()
        nodes = self.number_of_nodes_edit.text()
        epochs = self.epochs_edit.text()
        early = self.early_stopping.isChecked()
        patience = self.patience_edit.text()

        try:
            self.neural_network.params.batch_size = int(batch_size)
            self.neural_network.params.nodes = int(nodes)
            self.neural_network.params.epochs = int(epochs)
            self.neural_network.params.early = early
            self.neural_network.params.patience = int(patience)
        except:
            self.reset_defaults()

    def reset_defaults(self):
        self.neural_network.params.reset_default()
        self.__refresh_constants_values()

    def __refresh_constants_values(self):
        self.batch_size_edit.setText(str(self.neural_network.params.batch_size))
        self.number_of_nodes_edit.setText(str(self.neural_network.params.nodes))
        self.epochs_edit.setText(str(self.neural_network.params.epochs))
        self.early_stopping.setChecked(self.neural_network.params.early)
        self.patience_edit.setText(str(self.neural_network.params.patience))

    def __create_character_selection_area(self):
        self.character_edit = QtGui.QLineEdit(self)
        self.character_completer = QtGui.QCompleter(self.neural_network.raw_data['name'].values, self)

        self.character_completer.setCaseSensitivity(Qt.CaseInsensitive)
        character_label = QtGui.QLabel('Character to predict')
        character_label.setBuddy(self.character_edit)
        self.character_edit.setCompleter(self.character_completer)
        character_add_push_button = QtGui.QPushButton('Add', self)
        character_add_push_button.clicked.connect(self.__add_character__to_predictions)

        box_layout = QtGui.QHBoxLayout(self)
        box_layout.addWidget(character_label)
        box_layout.addWidget(self.character_edit)
        box_layout.addWidget(character_add_push_button)

        return box_layout

    def __add_character__to_predictions(self):
        data = self.character_edit.text()
        row = self.neural_network.raw_data.loc[self.neural_network.raw_data['name'] == self.character_edit.text()]
        index = row.index.tolist()

        if (index in self.neural_network.params.excluded_rows):
            return

        if (self.character_count >= 5 or len(index) == 0):
            return
        self.neural_network.params.excluded_rows.append(index[0])

        death = 'NaN'
        life = 'NaN'
        if (not row['death'].isnull().values.any()):
            death = str(row['death'].values[0] * 100)
            life = str(100 - (row['death'].values[0] * 100))

        self.table_data.append((index[0], data, death, life))
        self.__refresh_data(table=True)

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

        character_clear_push_button = QtGui.QPushButton('Clear', self)
        character_clear_push_button.clicked.connect(self.__clear_characters_in_table)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.table_view)
        layout.addWidget(character_clear_push_button)
        return layout

    def __clear_characters_in_table(self):
        self.table_data = []
        self.neural_network.params.excluded_rows = []
        self.__refresh_data(table=True)

    def __refresh_data(self, table=False):
        self.accuracy_value_label.setText(self.accuracy_value)
        self.loss_value_label.setText(self.loss_value)
        self.status_value_label.setText(self.status)
        if (table):
            self.table_model.changeData(self.table_data)
