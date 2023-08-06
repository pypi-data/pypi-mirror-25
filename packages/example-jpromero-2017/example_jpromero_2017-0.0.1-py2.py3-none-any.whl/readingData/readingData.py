import pandas as pd
from os import path
class ReadCSV(object):
    def __init__(self):
        here = path.abspath(path.dirname(__file__))
        pathFile = here[:-11] + "train.csv"
        print pathFile
        self.df = pd.read_csv(pathFile)

    def making_print(self):
        print self.df