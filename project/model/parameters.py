class Parameters(object):
    def __init__(self, batch_size=128, epochs=100, nodes=100, early=False, patience=10, verbose=1, dropout=0.2,
                 default=True, activation='tanh', file_path='./../datasets/cleaned_data.csv'):
        self.batch_size = batch_size
        self.epochs = epochs
        self.nodes = nodes
        self.early = early
        self.patience = patience
        self.verbose = verbose
        self.dropout = dropout
        self.activation = activation
        self.file_path = file_path

        if (default):
            self.excluded_rows = [1, 5, 172, 192, 1092, 1481, 1517, 1558, 1656, 1749]
            self.converting_columns = ['name', 'title', 'culture', 'mother', 'father', 'heir', 'house', 'spouse']
            self.input_params = ['title', 'male', 'culture', 'house', 'isAliveMother', 'isAliveFather', 'isAliveHeir',
                                 'isMarried', 'isNoble', 'age',
                                 'numDeadRelations', 'boolDeadRelations']  # ,'isPopular','popularity']
            self.output_params = ['isAlive']
            self.default_params = Parameters(default=not default)
