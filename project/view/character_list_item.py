from PySide import QtGui, QtCore

size = 200


class CharacterListItem(QtGui.QWidget):
    def __init__(self, name, image_name, parent=None):
        super(CharacterListItem, self).__init__(parent)
        self.name = name
        layout = QtGui.QGridLayout()
        layout.setAlignment(QtCore.Qt.AlignVCenter)
        label = QtGui.QLabel()

        url = 'view/images/characters/' + image_name
        pixels = QtGui.QPixmap()
        pixels.load(url)
        pixels = pixels.scaled(size, size)
        label.setPixmap(pixels)
        label.setFixedSize(size, size)

        button = QtGui.QPushButton(name)
        button.setMaximumWidth(size)
        layout.addWidget(label, 0, 0)
        layout.addWidget(button, 1, 0)
        self.setLayout(layout)
