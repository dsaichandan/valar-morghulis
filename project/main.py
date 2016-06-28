import data_loader as dt



file_reader = dt.DataLoad()

battles_filename = './../datasets/battles.csv'
character_deaths_filename = './../datasets/character-deaths.csv'
character_predictions_filename = './../datasets/character-predictions.csv'


header , data = file_reader.readCsv(character_predictions_filename)


print(header)
print(data)
