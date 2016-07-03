from PySide import QtGui, QtCore
from house_dialog import HouseDialog
size = 200


class HouseListItem(QtGui.QWidget):
    def __init__(self, data, characters, parent=None):
        super(HouseListItem, self).__init__(parent)
        self.data = data
        self.characters = characters
        layout = QtGui.QGridLayout()
        layout.setAlignment(QtCore.Qt.AlignVCenter)
        label = QtGui.QLabel()

        url = 'view/images/houses/' + self.data['imageLink'].split('/')[4]
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

        button = QtGui.QPushButton(self.data['name'])
        button.clicked.connect(self.show_dialog)
        button.setMaximumWidth(size)
        layout.addWidget(label, 0, 0)
        layout.addWidget(button, 1, 0)
        self.setLayout(layout)
        self.dialog = None

    def show_dialog(self):
        self.dialog = HouseDialog(self.data, self.characters)
