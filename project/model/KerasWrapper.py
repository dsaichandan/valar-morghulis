import numpy as np
import pandas as pd
from keras.callbacks import EarlyStopping
from keras.layers import Dense, Dropout, BatchNormalization
from keras.models import Sequential
from keras.utils import np_utils

from project.data_cleaner import DataCleaner
from project.data_preproces import PreProcessor
from project.model.parameters import Parameters


class KerasWrapper(object):
    def __init__(self, parameters=Parameters()):
        self.params = parameters
        self.data_cleaner = DataCleaner()
        self.pre_processor = PreProcessor()
        self.load_data()
        self.model_constructed = False
        self.train_completed = False

    def clean_data(self):
        self.data_cleaner.load_data()
        self.data_cleaner.clean()
        self.data_cleaner.save_cleaned()

    def load_data(self):
        self.data = pd.read_csv(self.params.file_path)
        self.raw_data = self.data.copy(deep=True)
        self.data_cleaner.load_data()

    def __prepare_data(self):

        self.data = self.pre_processor.convert_objects_to_categorical(self.data, self.params.converting_columns)
        self.data = self.pre_processor.normalize_data(self.data, self.params.converting_columns)
        self.data.fillna(-1, inplace=True)

        self.inputs = self.data[self.params.input_params]
        self.outputs = self.data[self.params.output_params]

        excluded_input_data = self.inputs.drop(self.inputs.index[self.params.excluded_rows])
        excluded_output_data = self.outputs.drop(self.outputs.index[self.params.excluded_rows])
        X = excluded_input_data.values
        y = excluded_output_data.values
        y = np_utils.to_categorical(y)

        return X, y

    def create_model(self, summary=True):

        X, y = self.__prepare_data()

        if (self.model_constructed):
            self.model.set_weights(self.network_weights)
            return X, y

        dimof_input = X.shape[1]
        dimof_output = np.max(y) + 1

        if (summary):
            print('dimof_input: ', dimof_input)
            print('dimof_output: ', dimof_output)
            print('batch_size: ', self.params.batch_size)
            print('dimof_middle: ', self.params.nodes)
            print('dropout: ', self.params.dropout)
            print('countof_epoch: ', self.params.epochs)
            print('verbose: ', self.params.verbose)
            print()

        self.model = Sequential()
        self.model.add(
            Dense(self.params.nodes, input_dim=dimof_input, init='uniform', activation=self.params.activation))
        self.model.add(BatchNormalization(beta_init='uniform'))
        self.model.add(
            Dense(self.params.nodes * 2, input_dim=dimof_input, init='uniform', activation=self.params.activation))
        self.model.add(Dropout(self.params.dropout))
        self.model.add(Dense(dimof_output, input_dim=dimof_input, init='uniform', activation='softmax'))
        self.model.compile(loss='mse', optimizer='sgd', metrics=['accuracy'])

        weight_ref = self.model.get_weights()
        self.network_weights = np.empty_like(weight_ref)
        self.network_weights[:] = weight_ref

        if (summary):
            self.model.summary()

        self.model_constructed = True

        return X, y

    def start_train(self, input_data, output_data):
        callbacks = []
        if (self.params.early):
            callbacks.append(
                EarlyStopping(patience=self.params.patience, verbose=self.params.verbose, monitor='val_loss'))
        fit = self.model.fit(input_data, output_data, validation_split=0.2,
                             batch_size=self.params.batch_size, nb_epoch=self.params.epochs,
                             verbose=self.params.verbose, shuffle=True, callbacks=callbacks)
        self.train_completed = True
        return fit

    def evaluate(self, input, output):
        loss, accuracy = self.model.evaluate(input, output, verbose=self.params.verbose)
        return loss, accuracy

    def run_for_all_characters(self):
        self.raw_data['death'] = np.nan
        self.raw_data['live'] = np.nan
        self.raw_data.sort_values('popularity', ascending=False)
        index = self.raw_data.head(100).index.tolist()
        self.params.excluded_rows = []

        # index = self.raw_data.index.tolist()

        for i in index:
            self.params.excluded_rows.append(i)
            self.start_whole_process()
            self.prediction()
            self.params.excluded_rows = []
        self.params.excluded_rows = []

    def prediction(self):

        predictions = []
        for i in self.params.excluded_rows:
            chosen_class = self.model.predict_classes(
                self.inputs.iloc[i].values.reshape((1, len(self.params.input_params))),
                verbose=0)
            probability = self.model.predict_proba(
                self.inputs.iloc[i].values.reshape((1, len(self.params.input_params))),
                verbose=0)
            character = str(self.raw_data['name'][i])

            # rounding on 2 decimals
            death = int((probability[0][0] * 100) + 0.5) / 100.0
            life = int((probability[0][1] * 100) + 0.5) / 100.0

            self.raw_data.set_value(i, 'death', 0)
            self.raw_data.set_value(i, 'live', 0)

            data = (i, character, str(death), str(life))
            predictions.append(data)
            self._prediction_summary(chosen_class, probability, character)

        return predictions

    def start_whole_process(self):
        X, y = self.create_model()
        self.start_train(X, y)
        return self.evaluate(X, y)

    def _prediction_summary(self, chosen_class, probability, character):
        print('Name: ' + character)
        print('Dead: ' + str(probability[0][0]) + ' %')
        print('Alive: ' + str(probability[0][1]) + ' %')
        print('Chosen class: ' + str(chosen_class))
        print(30 * '-')


if __name__ == '__main__':
    kw = KerasWrapper()
    kw.run_for_all_characters()
    kw.raw_data.to_csv('./../datasets/cleaned_data.csv')
