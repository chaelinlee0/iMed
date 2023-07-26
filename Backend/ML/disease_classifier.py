import pandas as pd 
import numpy as np

from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier

class DiseaseClassifier:
    def __init__(self):
        self.model = None
        self.le = preprocessing.LabelEncoder()
    
    def train_model(self):
        df_train = pd.read_csv("ML/Training.csv")
        df_train.drop(df_train.columns[len(df_train.columns)-1], axis=1, inplace=True)

        y_train = df_train["prognosis"]
        X_train = df_train.drop("prognosis", axis=1)
        self.le.fit(y_train)
        y_train = self.le.transform(y_train)

        rf = RandomForestClassifier(max_depth = 2, random_state=0)
        self.model = rf.fit(X_train, y_train)
    
    def evaluate_model(self):
        df_test = pd.read_csv("ML/Testing.csv")
        y_test = df_test["prognosis"]
        X_test = df_test.drop("prognosis", axis=1)
        y_test = self.le.transform(y_test)
        return self.model.score(X_test, y_test)

    def predict(self, symptoms):
        prediction_input = np.array(symptoms).reshape(1,-1)
        print(prediction_input)
        disease_num = self.model.predict(prediction_input)
        return self.le.inverse_transform(disease_num)