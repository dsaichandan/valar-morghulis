from PySide import QtGui, QtCore
import project.data_cleaner as dc
import pandas as pd
import character_list_item as cli


class CharactersTab(QtGui.QWidget):
    def __init__(self, parent=None):
        super(CharactersTab, self).__init__(parent)
        self.main_layout = QtGui.QVBoxLayout()
        self.filter_field = QtGui.QLineEdit()
        self.filter_widget = QtGui.QWidget()
        filter_layout = QtGui.QHBoxLayout()
        self.filter_button = QtGui.QPushButton("Search")
        self.filter_button.clicked.connect(self.filter_characters)
        self.filter_button.setAutoDefault(True)
        filter_layout.addWidget(self.filter_field)
        filter_layout.addWidget(self.filter_button)
        self.filter_widget.setLayout(filter_layout)
        self.main_layout.addWidget(self.filter_widget)
        self.scroll = QtGui.QScrollArea()
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.main_layout.addWidget(self.scroll)

        self.grid = QtGui.QGridLayout()
        data_cleaner = dc.DataCleaner()
        data_cleaner.load_data()

        it = 0
        it2 = 0
        self.model = data_cleaner.characters_csv

        self.display_model = self.model
        self.display_model = self.model[self.model['name'].str.contains("Tar")]
        self.display_model = self.display_model.sort_values('popularity', ascending=False)
        for index, row in self.display_model.iterrows():
            filename = str(row['imageLink'])
            item = cli.CharacterListItem(str(row['name']), filename)

            self.grid.addWidget(item, it2, it)
            it += 1
            if it % 6 == 5:
                it2 += 1
                it = 0
        self.main_widget = QtGui.QWidget()
        self.main_widget.setLayout(self.grid)
        self.scroll.setWidget(self.main_widget)
        self.setLayout(self.main_layout)

    def filter_characters(self):
        filter_text = self.filter_field.text()
        print(filter_text)
        print(len(filter_text))
        for i in range(self.grid.count()):
            self.grid.itemAt(i).widget().close()

        self.main_layout.removeWidget(self.scroll)
        self.scroll = QtGui.QScrollArea()
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.main_layout.addWidget(self.scroll)
        self.grid = QtGui.QGridLayout()

        it = 0
        it2 = 0
        self.display_model = self.model
        if len(filter_text) > 0:
            self.display_model = self.display_model[self.display_model['name'].str.contains(filter_text)]
        self.display_model = self.display_model.sort_values('popularity', ascending=False)
        for index, row in self.display_model.iterrows():
            filename = str(row['imageLink'])
            item = cli.CharacterListItem(str(row['name']), filename)
            self.grid.addWidget(item, it2, it)
            it += 1
            if it % 6 == 5:
                it2 += 1
                it = 0
        self.main_widget = QtGui.QWidget()
        self.main_widget.setLayout(self.grid)
        self.scroll.setWidget(self.main_widget)

        self.main_widget.update()
        self.main_widget.repaint()

        self.scroll.update()
        self.scroll.repaint()

        self.update()
        self.repaint()
