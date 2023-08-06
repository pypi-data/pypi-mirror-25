from readingData.readingData import ReadCSV
from core.core import CreateSVM
import numpy as np
import pandas as pd
def main():
    print "-------------------------------------"
    readCSV = ReadCSV()
    df = readCSV.df
    print "Dataset read"
    print "-------------------------------------"
    #readCSV.making_print()
    createSVM = CreateSVM()
    print "Dataset splitted"
    Xtrain, Xtest,Ytrain, Ytest = createSVM.split(df['Fare'],df['Survived'])
    print "-------------------------------------"
    svcFitted = createSVM.fit(Xtrain[:,np.newaxis],Ytrain)
    print "SVM trained"
    svcScore = createSVM.get_score(svcFitted, Xtest[:,np.newaxis], Ytest)
    print 'Score '+ str(svcScore)
    dfPred = pd.DataFrame(createSVM.predict(svcFitted), columns=['Fare', 'Survived'])
    print "-------------------------------------"
    print "Predictions"
    print dfPred
main()
