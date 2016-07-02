from PySide import QtGui

class ConfigurationTab(QtGui.QWidget):

    def __init__(self, parent=None):
        super(ConfigurationTab, self).__init__(parent)

        grid = QtGui.QGridLayout()

        constants_group_box = QtGui.QGroupBox("Constants configuration")
        constants_layout = self.__create_constants_area()
        constants_group_box.setLayout(constants_layout)

        status_group_box = QtGui.QGroupBox("Neural network status")
        status_layout = self.__create_training_results_area()
        status_group_box.setLayout(status_layout)


        train_button = QtGui.QPushButton("Start NN training", self)

        grid.addWidget(constants_group_box, 0, 0)
        grid.addWidget(status_group_box,1,0)
        grid.addWidget(train_button,2,0)

        self.setLayout(grid)


    def __create_constants_area(self):
        layout = QtGui.QFormLayout()
        batch_size_edit = QtGui.QLineEdit(self)
        batch_size_label = QtGui.QLabel("Batch size: ", self)
        batch_size_label.setBuddy(batch_size_edit)

        number_of_nodes_edit = QtGui.QLineEdit(self)
        number_of_nodes_label = QtGui.QLabel("Number of nodes per layer: ", self)
        number_of_nodes_label.setBuddy(number_of_nodes_edit)

        epochs_edit = QtGui.QLineEdit(self)
        epochs_label = QtGui.QLabel("Number of epochs: ", self)
        epochs_label.setBuddy(epochs_edit)

        early_stopping = QtGui.QCheckBox("Enable early stopping ", self)

        patience_edit = QtGui.QLineEdit(self)
        patience_label = QtGui.QLabel("Patience level: ",self)
        patience_label.setBuddy(patience_edit)


        layout.addRow(batch_size_label, batch_size_edit)
        layout.addRow(number_of_nodes_label, number_of_nodes_edit)
        layout.addRow(epochs_label, epochs_edit)
        layout.addRow(early_stopping)
        layout.addRow(patience_label,patience_edit)


        return layout

    def __create_training_results_area(self):
        layout = QtGui.QFormLayout()

        status_label = QtGui.QLabel("Training status: ",self)
        status_value_label = QtGui.QLabel("In progress",self)
        status_label.setBuddy(status_value_label)

        loss_label = QtGui.QLabel("Loss : ", self)
        loss_value_label = QtGui.QLabel("NaN", self)
        loss_label.setBuddy(loss_value_label)

        accuracy_label = QtGui.QLabel("Accuracy: ", self)
        accuracy_value_label = QtGui.QLabel("NaN", self)
        accuracy_label.setBuddy(accuracy_value_label)

        layout.addRow(status_label,status_value_label)
        layout.addRow(loss_label, loss_value_label)
        layout.addRow(accuracy_label, accuracy_value_label)

        return layout

    def __create_actions_area(self):
        pass
