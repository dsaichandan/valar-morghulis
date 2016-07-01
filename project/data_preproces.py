

class PreProcessor(object):

    def __init__(self):
        pass


    '''
    Convert columns dtypes to category
    '''
    def convert_objects_to_categorical(self, data, columnList, convert_to_int = True):

        for col in columnList:
            data[col] = data[col].astype('category')

            if(convert_to_int):
             data[col] = data[col].cat.codes


        return data


    '''
        Normalize data
    '''
    def normalize_data(self, data, column_list):

        for column in column_list:
            df = data[column]
            data[column] = (df - df.mean()) / (df.max() - df.min())


        return data



