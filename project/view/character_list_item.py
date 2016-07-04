from PySide import QtGui, QtCore
from character_dialog import CharacterDialog

size = 200


class CharacterListItem(QtGui.QWidget):
    def __init__(self, data, neural_network, parent=None):
        super(CharacterListItem, self).__init__(parent)
        self.neural_network = neural_network
        self.data = data
        layout = QtGui.QGridLayout()
        layout.setAlignment(QtCore.Qt.AlignVCenter)
        label = QtGui.QLabel()

        url = 'view/images/characters/' + str(self.data.imageLink)
        pixels = QtGui.QPixmap()
        pixels.load(url)
        pixels = pixels.scaled(size, size)
        label.setPixmap(pixels)
        label.setFixedSize(size, size)
        css_label = """
            QLabel {
                border: 2px solid grey;
                border-radius: 4px;
                padding: 2px;
            }
        """
        label.setStyleSheet(css_label)

        button = QtGui.QPushButton(str(self.data['name']))
        button.clicked.connect(self.show_dialog)
        button.setMaximumWidth(size)
        layout.addWidget(label, 0, 0)
        layout.addWidget(button, 1, 0)
        self.setLayout(layout)
        self.dialog = None

    def show_dialog(self):
        self.dialog = CharacterDialog(self.data, self.neural_network)
