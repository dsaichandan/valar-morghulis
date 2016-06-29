

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


