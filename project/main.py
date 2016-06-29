from __future__ import absolute_import
from __future__ import print_function

import pandas as pd
import numpy as np
from keras.utils import  np_utils

import seaborn as sns

from keras.models import Sequential
from keras.layers import Dense,Dropout

import data_loader as dt
import data_cleaner as dc
import data_preproces as dp

file_reader = dt.DataLoad()

battles_filename = './../datasets/battles.csv'
character_deaths_filename = './../datasets/character-deaths.csv'
character_predictions_filename = './../datasets/character-predictions.csv'

cleaned_data_filename = './../datasets/cleaned_data.csv'


data_preproces = dp.PreProcessor()

data_cleaner = dc.DataCleaner()
data_cleaner.load_data()
data_cleaner.clean()
data_cleaner.save_cleaned()



print('Parsing csv file')
new_data = pd.read_csv(cleaned_data_filename   , delimiter=',')

raw_data = new_data.copy(deep=True)
new_data = data_preproces.convert_objects_to_categorical(new_data,['name','title','culture',
                                                                   'mother','father','heir','house',
                                                                   'spouse'])
new_data.fillna(-1, inplace = True)



inputs = new_data[['name','title','male','culture','dateOfBirth','mother','father','heir','house',
                   'spouse','isAliveMother','isAliveFather','isAliveHeir','isMarried','isNoble','age',
                   'numDeadRelations','boolDeadRelations','isPopular','popularity']]
outputs = new_data['isAlive']

X = inputs.values
y = outputs.values


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
countof_epoch = 1000
verbose = 0
print('batch_size: ', batch_size)
print('dimof_middle: ', dimof_middle)
print('dropout: ', dropout)
print('countof_epoch: ', countof_epoch)
print('verbose: ', verbose)
print()

model = Sequential()
model.add(Dense(dimof_middle, input_dim=dimof_input, init='uniform', activation='tanh'))
model.add(Dropout(dropout))
model.add(Dense(dimof_middle, input_dim=dimof_input, init='uniform', activation='tanh'))
model.add(Dropout(dropout))
model.add(Dense(dimof_output, input_dim=dimof_input, init='uniform', activation='softmax'))
model.compile(loss='mse', optimizer='sgd', metrics=['accuracy'])

model.summary()
# Train

print('Training neural network started...')
model.fit(
    X, y,
    validation_split=0.2,
    batch_size=batch_size, nb_epoch=countof_epoch, verbose=verbose)
print('Training neural network complete')

# Evaluate
loss, accuracy = model.evaluate(X, y, verbose=verbose)
print('loss: ', loss)
print('accuracy: ', accuracy)
print()


for i in range(0,5):
    print('prediction of '+str(raw_data.iloc[i,6])+' : ', model.predict_classes(inputs.iloc[i].values.reshape((1,20)), verbose=verbose))

















