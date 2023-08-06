import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import pandas as pd
class CreateSVM():

    def split(self,dfTrain, dftargetLabel):
        return train_test_split(dfTrain, dftargetLabel, test_size=0.3, random_state=2)

    def fit(self,X,Y):
        svc = SVC()
        return svc.fit(X,Y)

    def get_score(self,svcFitted, X,Y):
        return svcFitted.score(X,Y)


    def predict(self,svcFitted):
        X =100*np.random.sample((10,1))
        y = svcFitted.predict(X).reshape(10,1)
        return  np.concatenate((X,y), axis=1)





