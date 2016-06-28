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

    def change_culture(self, value):
        value = value.lower()
        v = [k for (k, v) in self.culture_cleaner.items() if value in v]
        return v[0] if len(v) > 0 else value.title()

    def change_house(self, value):
        value = value.lower()
        v = [k for (k, v) in self.house_cleaner.items() if value in v]
        return v[0] if len(v) > 0 else value.title()

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

    def clean(self):
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

    def save_cleaned(self):
        self.characters_csv.to_csv(self.cleaned_characters_data_filename)
        print('Created cleaned_data.csv')
        print("---------------------------------")
