import pandas as pd


class DataCleaner(object):
    battles_filename = './../datasets/battles.csv'
    character_deaths_filename = './../datasets/character-deaths.csv'
    character_predictions_filename = './../datasets/character-predictions.csv'
    cultures_json_filename = './../datasets/cultures.json'
    houses_json_filename = './../datasets/houses.json'
    characters_json_filename = './../datasets/characters.json'
    cleaned_characters_data_filename = './../datasets/cleaned_data.csv'
    battles_csv = None
    deaths_csv = None
    characters_csv = None
    houses_json = None
    cultures_json = None
    characters_json = None

    culture_cleaner = {
        'Summer Islands': ['summer islands', 'summer islander', 'summer isles'],
        'Ghiscari': ['ghiscari', 'ghiscaricari', 'ghis'],
        'Asshai': ["asshai'i", 'asshai'],
        'Lysene': ['lysene', 'lyseni'],
        'Andal': ['andal', 'andals'],
        'Braavosi': ['braavosi', 'braavos'],
        'Dornish': ['dornishmen', 'dorne', 'dornish'],
        'Myrish': ['myr', 'myrish', 'myrmen'],
        'Westermen': ['westermen', 'westerman', 'westerlands'],
        'Westerosi': ['westeros', 'westerosi'],
        'Stormlander': ['stormlands', 'stormlander'],
        'Norvoshi': ['norvos', 'norvoshi'],
        'Northmen': ['the north', 'northmen'],
        'Free Folk': ['wildling', 'first men', 'free folk'],
        'Qartheen': ['qartheen', 'qarth'],
        'Reach': ['the reach', 'reach', 'reachmen'],
        'Others': ['', 'nan'],
        'Vale Mountain Clans': ['vale mountain clans', 'vale', 'valemen'],
        'Lhazareen': ['lhazareen', 'lhazarene']
    }

    house_cleaner = {
        'Wildlings': ['wildling'],
        'Brotherhood Without Banners': ['brotherhood without banners'],
        'Unknown': ['nan', '']
    }

    important_houses = {
        1: ['house stark', 'house targaryen', 'house martell', 'house tyrell', 'house lannister', 'house baratheon',
            'house tully', 'house mormont', 'house baelish', 'house arryn', 'house greyjoy', 'house bolton',
            'house florent', 'house redwyne', 'house umber', 'house frey']
    }

    def change_culture(self, value):
        value = value.lower()
        v = [k for (k, v) in self.culture_cleaner.items() if value in v]
        return v[0] if len(v) > 0 else value.title()

    def change_house(self, value):
        value = value.lower()
        v = [k for (k, v) in self.house_cleaner.items() if value in v]
        return v[0] if len(v) > 0 else value.title()

    def is_important_house(self, value):
        value = value.lower()
        v = [k for (k, v) in self.important_houses.items() if value in v]
        return v[0] if len(v) > 0 else 0

    def find_in_json(self, name, col):
        idx = self.characters_json[self.characters_json['name'] == name].index.tolist()
        if len(idx) == 0:
            return ''
        return self.characters_json.get_value(idx[0], col)

    def load_data(self):
        print('Data loading...')
        print("---------------------------------")
        self.battles_csv = pd.read_csv(self.battles_filename)
        print("battles.csv:\t\t\t\t" + str(self.battles_csv.name.size))
        self.deaths_csv = pd.read_csv(self.character_deaths_filename)
        print("characters-deaths.csv:\t\t" + str(self.deaths_csv.Name.size))
        self.characters_csv = pd.read_csv(self.character_predictions_filename)
        print("character_predictions.csv:\t" + str(self.characters_csv.name.size))
        self.houses_json = pd.read_json(self.houses_json_filename)
        print("houses.json:\t\t\t\t" + str(self.houses_json.name.size))
        self.cultures_json = pd.read_json(self.cultures_json_filename)
        print("cultures.json:\t\t\t\t" + str(self.cultures_json.name.size))
        self.characters_json = pd.read_json(self.characters_json_filename)
        print("characters.json:\t\t\t" + str(self.characters_json.name.size))
        print("---------------------------------")
        print("Data loading finished.")
        print("---------------------------------")

    def data_info(self):
        print("---------------------------------")
        print("Data info.")
        print("---------------------------------")
        unknown_house = 0
        unknown_culture = 0
        unknown_mother = 0
        unknown_father = 0
        unknown_spouse = 0
        unknown_heir = 0
        unknown_birth = 0
        unknown_death = 0
        for index, row in self.characters_csv.iterrows():
            if row['house'] == 'Unknown':
                unknown_house += 1
            if row['culture'] == 'Others':
                unknown_culture += 1
            if pd.isnull(row['mother']):
                unknown_mother += 1
            if pd.isnull(row['father']):
                unknown_father += 1
            if pd.isnull(row['spouse']):
                unknown_spouse += 1
            if pd.isnull(row['heir']):
                unknown_heir += 1
            if pd.isnull(row['DateoFdeath']):
                unknown_birth += 1
            if pd.isnull(row['dateOfBirth']):
                unknown_death += 1

        print("Unknown houses:\t\t" + str(unknown_house))
        print("Unknown cultures:\t" + str(unknown_culture))
        print("Unknown mother:\t\t" + str(unknown_mother))
        print("Unknown father:\t\t" + str(unknown_father))
        print("Unknown spouse:\t\t" + str(unknown_spouse))
        print("Unknown heir:\t\t" + str(unknown_heir))
        print("Unknown birth date:\t" + str(unknown_birth))
        print("Unknown death date:\t" + str(unknown_death))
        print("---------------------------------")

    def clean(self, images_pairing_flag=False):
        # clean all the cultures
        print("Cleaning the cultures...")
        print("---------------------------------")
        old_cultures = {}
        for c in self.characters_csv.culture:
            old_cultures[c] = True
        print("Old cultures:\t\t\t\t" + str(len(old_cultures)))
        self.characters_csv.loc[:, "culture"] = [self.change_culture(cult) for cult in
                                                 self.characters_csv.culture.fillna("")]
        cleaned_cultures = {}
        for c in self.characters_csv.culture:
            cleaned_cultures[c] = True
        print("New cultures:\t\t\t\t" + str(len(cleaned_cultures)))
        print("JSON cultures:\t\t\t\t" + str(self.cultures_json.name.size))
        print("---------------------------------")
        print("Cultures cleaned.")
        print("---------------------------------")

        # clean all the houses
        print("Cleaning the houses...")
        print("---------------------------------")
        old_houses = {}
        for h in self.characters_csv.house:
            old_houses[h] = True
        print("Old houses:\t\t\t\t\t" + str(len(old_houses)))
        self.characters_csv.loc[:, "house"] = [self.change_house(house) for house in
                                               self.characters_csv.house.fillna("")]
        cleaned_houses = {}
        for c in self.characters_csv.house:
            cleaned_houses[c] = True
        print("New houses:\t\t\t\t\t" + str(len(cleaned_houses)))
        print("JSON houses:\t\t\t\t" + str(self.houses_json.name.size))
        print("---------------------------------")
        print("Houses cleaned.")
        print("---------------------------------")
        print("Selecting important houses.")
        self.houses_json['isImportant'] = ''
        self.houses_json.loc[:, "isImportant"] = [self.is_important_house(house) for house in
                                                  self.houses_json.name]
        print("---------------------------------")
        print("Important houses selected.")
        print("---------------------------------")
        if images_pairing_flag:
            print("Images pairing...")
            self.characters_csv["imageLink"] = ""
            paired = 0
            for index, row_csv in self.characters_csv.iterrows():
                for index2, row_json in self.characters_json.iterrows():
                    if str(row_csv['name']) == str(row_json['name']):
                        if pd.notnull(row_json['imageLink']):
                            link = str(row_json['imageLink'])
                            self.characters_csv.set_value(index, 'imageLink', link.split('/')[4])
                        else:
                            self.characters_csv.set_value(index, 'imageLink', 'no_image.jpg')
                        paired += 1
                        if paired % 100 == 0:
                            print(paired)
                        break
            print("---------------------------------")
            print("Images pairing completed.")
            print("---------------------------------")

    def save_cleaned(self):
        self.characters_csv.to_csv(self.cleaned_characters_data_filename)
        self.houses_json.to_json(self.houses_json_filename, orient='records')
        print('Created cleaned_data.csv')
        print("---------------------------------")

    def merging_json_to_csv(self):
        print("---------------------------------")
        print("Merging...")
        print("---------------------------------")
        for index, row in self.characters_csv.iterrows():
            house = self.find_in_json(row['name'], 'house')
            if row['house'] == 'Unknown' and pd.isnull(house) == False:
                self.characters_csv.set_value(index, 'house', str(house))
            culture = self.find_in_json(row['name'], 'culture')
            if row['culture'] == 'Others' and pd.isnull(culture) == False:
                self.characters_csv.set_value(index, 'culture', str(culture))
            mother = self.find_in_json(row['name'], 'mother')
            if pd.isnull(row['mother']) and pd.isnull(mother) == False:
                self.characters_csv.set_value(index, 'mother', str(mother))
            father = self.find_in_json(row['name'], 'father')
            if pd.isnull(row['father']) and pd.isnull(father) == False:
                self.characters_csv.set_value(index, 'father', str(father))
            spouse = self.find_in_json(row['name'], 'spouse')
            if pd.isnull(row['spouse']) and pd.isnull(spouse) == False:
                self.characters_csv.set_value(index, 'spouse', str(spouse))
            heir = self.find_in_json(row['name'], 'heir')
            if pd.isnull(row['heir']) and pd.isnull(heir) == False:
                self.characters_csv.set_value(index, 'heir', str(heir))
            birth = self.find_in_json(row['name'], 'dateOfBirth')
            if pd.isnull(row['dateOfBirth']) and pd.isnull(birth) == False and birth != '':
                self.characters_csv.set_value(index, 'dateOfBirth', float(birth))
            death = self.find_in_json(row['name'], 'dateOfDeath')
            if pd.isnull(row['DateoFdeath']) and pd.isnull(death) == False and death != '':
                self.characters_csv.set_value(index, 'DateoFdeath', float(death))
        print("---------------------------------")
        print("Merging finished.")
        print("---------------------------------")

    def __add_battle_data(self):
        pass


if __name__ == '__main__':
    data_cleaner = DataCleaner()
    data_cleaner.load_data()
    data_cleaner.data_info()
    data_cleaner.merging_json_to_csv()
    data_cleaner.data_info()

    #data_cleaner.clean()
    data_cleaner.save_cleaned()
