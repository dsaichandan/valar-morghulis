import data_loader as dt
import data_cleaner as dc


file_reader = dt.DataLoad()

battles_filename = './../datasets/battles.csv'
character_deaths_filename = './../datasets/character-deaths.csv'
character_predictions_filename = './../datasets/character-predictions.csv'


header, data = file_reader.readCsv(character_predictions_filename)


data_cleaner = dc.DataCleaner()
data_cleaner.load_data()
data_cleaner.clean()
data_cleaner.save_cleaned()