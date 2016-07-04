# coding=utf-8
import pandas as pd
from PySide import QtGui

size = 180


class CharacterDialog(QtGui.QDialog):
    def __init__(self, data, neural_network, parent=None):
        super(CharacterDialog, self).__init__(parent)
        self.neural_network = neural_network
        self.data = data
        # print(data)
        self.grid = QtGui.QGridLayout()
        self.setWindowTitle(str(self.data['name']))
        self.setWindowIcon(QtGui.QIcon('./view/images/favicon.jpg'))
        self.setModal(True)
        font = QtGui.QFont()
        font.setBold(True)
        name_lbl = QtGui.QLabel("Name: ")
        culture_lbl = QtGui.QLabel("Culture: ")
        house_lbl = QtGui.QLabel("House: ")
        birth_date_lbl = QtGui.QLabel("Birth date: ")
        death_date_lbl = QtGui.QLabel("Death date: ")
        mother_lbl = QtGui.QLabel("Mother:")
        father_lbl = QtGui.QLabel("Father:")

        heir_lbl = QtGui.QLabel("Heir: ")
        spouse_lbl = QtGui.QLabel("Spouse: ")
        noble_lbl = QtGui.QLabel("Noble: ")
        title_lbl = QtGui.QLabel("Title: ")
        age_lbl = QtGui.QLabel("Age: ")
        alive_lbl = QtGui.QLabel("Alive: ")
        popularity_label = QtGui.QLabel("Popularity: ")
        prediction_label = QtGui.QLabel("Death prediction: ")

        name_lbl.setFont(font)
        culture_lbl.setFont(font)
        house_lbl.setFont(font)
        birth_date_lbl.setFont(font)
        death_date_lbl.setFont(font)
        mother_lbl.setFont(font)
        father_lbl.setFont(font)
        heir_lbl.setFont(font)
        spouse_lbl.setFont(font)
        noble_lbl.setFont(font)
        title_lbl.setFont(font)
        age_lbl.setFont(font)
        alive_lbl.setFont(font)
        popularity_label.setFont(font)
        prediction_label.setFont(font)

        self.popularity_bar = QtGui.QProgressBar(self)
        self.prediction_bar = QtGui.QProgressBar(self)

        self.prediction_push_button = QtGui.QPushButton('Glaeson iā Morghon', self)
        self.prediction_push_button.clicked.connect(self.__death_predict)

        css = """
            QProgressBar {
                border: 1px solid grey;
                border-radius: 3px;
                text-align: center;
                font-weight: bold;
                padding: 1px;
                height: 17px;
            }

            QProgressBar::chunk {
                background-color: #c62828;
                width: 15px;
            }
        """
        self.prediction_bar.setStyleSheet(css)

        self.grid.addWidget(name_lbl, 0, 0)
        self.grid.addWidget(culture_lbl, 1, 0)
        self.grid.addWidget(house_lbl, 2, 0)
        self.grid.addWidget(mother_lbl, 3, 0)
        self.grid.addWidget(father_lbl, 4, 0)
        self.grid.addWidget(heir_lbl, 5, 0)
        self.grid.addWidget(spouse_lbl, 6, 0)
        self.grid.addWidget(birth_date_lbl, 7, 0)
        self.grid.addWidget(death_date_lbl, 8, 0)
        self.grid.addWidget(age_lbl, 9, 0)

        self.grid.addWidget(title_lbl, 7, 2)
        self.grid.addWidget(noble_lbl, 8, 2)
        self.grid.addWidget(alive_lbl, 9, 2)
        self.grid.addWidget(popularity_label, 10, 0)
        self.grid.addWidget(prediction_label, 11, 0)
        self.grid.addWidget(self.popularity_bar, 10, 1, 1, 3)
        self.grid.addWidget(self.prediction_bar, 11, 1, 1, 3)
        self.grid.addWidget(self.prediction_push_button, 12, 1, 1, 3)
        self.populate_data()
        self.setLayout(self.grid)
        self.show()

    def __death_predict(self):
        self.neural_network.params.excluded_rows = []
        index = self.data.values[0]
        self.neural_network.params.excluded_rows.append(index)
        loss, accuracy = self.neural_network.start_whole_process()
        print(accuracy)
        print(loss)
        results = self.neural_network.prediction()
        death_percentage = results[0][2]
        self.data['death'] = death_percentage
        self.prediction_bar.setValue(int(float(death_percentage) * 100))

    def populate_data(self):
        name_data = QtGui.QLabel(str(self.data['name']))

        if pd.notnull(self.data['culture']):
            culture = str(self.data['culture'])
        else:
            culture = " - "
        culture_data = QtGui.QLabel(culture)

        if pd.notnull(self.data['house']):
            house = str(self.data['house'])
        else:
            house = " - "
        house_data = QtGui.QLabel(house)

        if pd.notnull(self.data['mother']):
            mother = str(self.data['mother'])
        else:
            mother = " - "
        mother_data = QtGui.QLabel(mother)

        if pd.notnull(self.data['father']):
            father = str(self.data['father'])
        else:
            father = " - "
        father_data = QtGui.QLabel(father)

        if pd.notnull(self.data['dateOfBirth']):
            birth = str(int(self.data['dateOfBirth']))
        else:
            birth = " - "
        birth_data = QtGui.QLabel(birth)

        if pd.notnull(self.data['DateoFdeath']):
            death = str(int(self.data['DateoFdeath']))
        else:
            death = " - "
        death_data = QtGui.QLabel(death)

        if pd.notnull(self.data['heir']):
            heir = str(self.data['heir'])
        else:
            heir = " - "
        heir_data = QtGui.QLabel(heir)

        if pd.notnull(self.data['spouse']):
            spouse = str(self.data['spouse'])
        else:
            spouse = " - "
        spouse_data = QtGui.QLabel(spouse)

        if pd.notnull(self.data['age']):
            age = str(int(self.data['age']))
        else:
            age = " - "
        age_data = QtGui.QLabel(age)

        self.grid.addWidget(name_data, 0, 1)
        self.grid.addWidget(culture_data, 1, 1)
        self.grid.addWidget(house_data, 2, 1)
        self.grid.addWidget(mother_data, 3, 1)
        self.grid.addWidget(father_data, 4, 1)
        self.grid.addWidget(heir_data, 5, 1)
        self.grid.addWidget(spouse_data, 6, 1)
        self.grid.addWidget(birth_data, 7, 1)
        self.grid.addWidget(death_data, 8, 1)
        self.grid.addWidget(age_data, 9, 1)

        if pd.notnull(self.data['title']):
            title = str(self.data['title'])
        else:
            title = " - "
        title_data = QtGui.QLabel(title)

        if pd.notnull(self.data['isNoble']):
            if self.data['isNoble'] == 1:
                noble = "Yes"
            else:
                noble = "No"
        else:
            noble = " - "
        noble_data = QtGui.QLabel(noble)

        if pd.notnull(self.data['isAlive']):
            if self.data['isAlive'] == 1:
                alive = "Yes"
            else:
                alive = "No"
        else:
            alive = " - "
        alive_data = QtGui.QLabel(alive)

        image_data = QtGui.QLabel()
        url = 'view/images/characters/' + str(self.data['imageLink'])
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
        if pd.notnull(self.data['popularity']):
            popularity = int(self.data['popularity'] * 100)
        else:
            popularity = 0
        self.popularity_bar.setValue(popularity)
        self.prediction_bar.setValue(0)
        self.grid.addWidget(image_data, 0, 2, 7, 2)
        self.grid.addWidget(title_data, 7, 3)
        self.grid.addWidget(noble_data, 8, 3)
        self.grid.addWidget(alive_data, 9, 3)
