import pandas as pd
from PySide import QtGui

size = 180


class HouseDialog(QtGui.QDialog):
    def __init__(self, data, characters, parent=None):
        super(HouseDialog, self).__init__(parent)
        self.data = data
        self.characters = characters
        self.display_model = characters
        print(data)
        self.grid = QtGui.QGridLayout()
        self.setWindowTitle(str(self.data['name']))
        self.setWindowIcon(QtGui.QIcon('./view/images/favicon.jpg'))
        self.setModal(True)
        font = QtGui.QFont()
        font.setBold(True)

        name_lbl = QtGui.QLabel("Name: ")
        lord_lbl = QtGui.QLabel("Current Lord: ")
        words_lbl = QtGui.QLabel("Words: ")
        arms_lbl = QtGui.QLabel("Coat of Arms: ")
        title_lbl = QtGui.QLabel("Title: ")
        region_lbl = QtGui.QLabel("Region: ")
        overlord_lbl = QtGui.QLabel("Overlord:")
        cadet_lbl = QtGui.QLabel("Cadet branch:")

        name_lbl.setFont(font)
        lord_lbl.setFont(font)
        words_lbl.setFont(font)
        arms_lbl.setFont(font)
        title_lbl.setFont(font)
        region_lbl.setFont(font)
        overlord_lbl.setFont(font)
        cadet_lbl.setFont(font)

        self.grid.addWidget(name_lbl, 1, 0)
        self.grid.addWidget(lord_lbl, 2, 0)
        self.grid.addWidget(title_lbl, 3, 0)
        self.grid.addWidget(words_lbl, 4, 0)
        self.grid.addWidget(arms_lbl, 5, 0)
        self.grid.addWidget(region_lbl, 6, 0)
        self.grid.addWidget(overlord_lbl, 7, 0)
        self.grid.addWidget(cadet_lbl, 8, 0)

        self.populate_data()
        self.setLayout(self.grid)
        self.show()

    def populate_data(self):
        name_data = QtGui.QLabel(str(self.data['name']))

        if pd.notnull(self.data['currentLord']):
            lord = str(self.data['currentLord'])
        else:
            lord = " - "
        lord_data = QtGui.QLabel(lord)

        if pd.notnull(self.data['words']):
            words = str(self.data['words'])
        else:
            words = " - "
        words_data = QtGui.QLabel(words)

        if pd.notnull(self.data['coatOfArms']):
            arms = str(self.data['coatOfArms'])
        else:
            arms = " - "
        arms_data = QtGui.QLabel(arms)

        if pd.notnull(self.data['title']):
            title = str(self.data['title'])
        else:
            title = " - "
        title_data = QtGui.QLabel(title)

        if pd.notnull(self.data['region']):
            region = str(self.data['region'])
        else:
            region = " - "
        region_data = QtGui.QLabel(region)

        if pd.notnull(self.data['overlord']):
            overlord = str(self.data['overlord'])
        else:
            overlord = " - "
        overlord_data = QtGui.QLabel(overlord)

        if pd.notnull(self.data['cadetBranch']):
            cadet = str(self.data['cadetBranch'])
        else:
            cadet = " - "
        cadet_data = QtGui.QLabel(cadet)

        self.grid.addWidget(name_data, 1, 1)
        self.grid.addWidget(lord_data, 2, 1)
        self.grid.addWidget(title_data, 3, 1)
        self.grid.addWidget(words_data, 4, 1)
        self.grid.addWidget(arms_data, 5, 1)
        self.grid.addWidget(region_data, 6, 1)
        self.grid.addWidget(overlord_data, 7, 1)
        self.grid.addWidget(cadet_data, 8, 1)

        image_data = QtGui.QLabel()
        url = 'view/images/houses/' + str(self.data['imageLink'].split('/')[4])
        pixels = QtGui.QPixmap()
        pixels.load(url)
        pixels = pixels.scaled(size, size)
        image_data.setPixmap(pixels)
        image_data.setFixedSize(size, size)
        css_label = """
            QLabel {
                border: 2px solid grey;
                border-radius: 4px;
                padding: 2px;
            }
        """
        image_data.setStyleSheet(css_label)
        self.grid.addWidget(image_data, 0, 0)

        group_box = QtGui.QGroupBox("Members")

        member_list = QtGui.QListView()
        member_list.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        # Create an empty model for the list's data
        model = QtGui.QStandardItemModel(member_list)
        house_name = self.data['name']
        self.display_model = self.display_model[self.display_model['house'].str.contains(house_name)]
        self.display_model = self.display_model.sort_values('popularity', ascending=False)

        for index, row in self.display_model.iterrows():
            item = QtGui.QStandardItem(row['name'])
            # Add the item to the model
            model.appendRow(item)

        # Apply the model to the list view
        member_list.setModel(model)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(member_list)
        group_box.setLayout(layout)
        self.grid.addWidget(group_box, 0, 1)



