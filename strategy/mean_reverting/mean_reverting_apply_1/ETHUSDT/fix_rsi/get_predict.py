"""
load models
return prediction [0] or [1]
"""
from sklearn import datasets
from joblib import dump, load


class Get_predict:
    def __init__(self):
        self.model = None

    # load a model and store to self.model
    # input: file path
    # output: void
    def load_model(self, path):
        self.model = load(path)

    def predict(self, df):
        return self.model.predict(df)


