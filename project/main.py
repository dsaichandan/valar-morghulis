from __future__ import absolute_import
from __future__ import print_function

import pandas as pd
import numpy as np
from keras.utils import  np_utils

import seaborn as sns

from keras.models import Sequential
from keras.layers import Dense,Dropout, BatchNormalization
from keras.callbacks import  BaseLogger,ProgbarLogger,History,ModelCheckpoint

import data_cleaner as dc
import data_preproces as dp


battles_filename = './../datasets/battles.csv'
character_deaths_filename = './../datasets/character-deaths.csv'
character_predictions_filename = './../datasets/character-predictions.csv'

cleaned_data_filename = './../datasets/cleaned_data.csv'


data_preproces = dp.PreProcessor()

data_cleaner = dc.DataCleaner()
data_cleaner.load_data()
data_cleaner.clean()
data_cleaner.save_cleaned()



converting_columns = ['name','title','culture', 'mother','father','heir','house', 'spouse']

print('Parsing csv file')
new_data = pd.read_csv(cleaned_data_filename   , delimiter=',')

raw_data = new_data.copy(deep=True)
new_data = data_preproces.convert_objects_to_categorical(new_data,converting_columns)
new_data = data_preproces.normalize_data(new_data, converting_columns)


new_data.to_csv('./../datasets/processed_data.csv')

new_data.fillna(-1, inplace = True)


input_params = ['title','male','culture','house','isAliveMother','isAliveFather','isAliveHeir','isMarried','isNoble',
                   'numDeadRelations','boolDeadRelations','isPopular','popularity']
output_params = ['isAlive']

exclude_rows = [1,5,172,192,1092,1481,1517,1558,1656,1683]

inputs = new_data[input_params]
outputs = new_data[output_params]

excluded_input_data = inputs.drop(inputs.index[exclude_rows])
excluded_output_data = outputs.drop(outputs.index[exclude_rows])
X = excluded_input_data.values
y = excluded_output_data.values


# Get dimensions of input and output
dimof_input = X.shape[1]
dimof_output = np.max(y) + 1
print('dimof_input: ', dimof_input)
print('dimof_output: ', dimof_output)

# Set y categorical
y = np_utils.to_categorical(y)



# Set constants
batch_size = 128
dimof_middle = 100
dropout = 0.2
countof_epoch = 100
verbose = 0
print('batch_size: ', batch_size)
print('dimof_middle: ', dimof_middle)
print('dropout: ', dropout)
print('countof_epoch: ', countof_epoch)
print('verbose: ', verbose)
print()

mid_layers_activation = 'tanh'

model = Sequential()
model.add(Dense(dimof_middle, input_dim=dimof_input, init='uniform', activation=mid_layers_activation))
model.add(Dropout(dropout))
model.add(Dense(dimof_middle, input_dim=dimof_input, init='uniform', activation=mid_layers_activation))
model.add(Dropout(dropout))
model.add(Dense(dimof_middle, input_dim=dimof_input, init='uniform', activation=mid_layers_activation))
model.add(Dropout(dropout))
model.add(Dense(dimof_middle, input_dim=dimof_input, init='uniform', activation=mid_layers_activation))
model.add(BatchNormalization(beta_init='uniform'))
model.add(Dense(dimof_output, input_dim=dimof_input, init='uniform', activation='softmax'))
model.compile(loss='mse', optimizer='sgd', metrics=['accuracy'])

model.summary()
# Train

print('Training neural network started...')

progbar_logger = ProgbarLogger()
history = History()
model_checkpoint = ModelCheckpoint('./../datasets/model_checkpoint.hdf5')
model.fit(
    X, y,
    validation_split=0.2,
    batch_size=batch_size, nb_epoch=countof_epoch, verbose=verbose, callbacks=[progbar_logger, history, model_checkpoint])
print('Training neural network complete')

# Evaluate
loss, accuracy = model.evaluate(X, y, verbose=verbose)
print('loss: ', loss)
print('accuracy: ', accuracy)
print()

print(15*"=" +'Predictions'+ 15*'=')
for i in exclude_rows:
    chosen_class =  model.predict_classes(inputs.iloc[i].values.reshape((1,len(input_params))), verbose=verbose)
    probability = model.predict_proba(inputs.iloc[i].values.reshape((1,len(input_params))), verbose=verbose)
    character = str(raw_data.iloc[i,6])
    print('Name: '+character)
    print('Dead: ' + str(probability[0][0]) +'%')
    print('Alive: '+ str(probability[0][1])+'%')
    print(30*'-')
















