from __future__ import print_function
import pandas as pd
from os import path
class ReadCSV(object):
    def __init__(self):
        here = path.dirname(path.dirname(path.abspath(__file__)))
        pathFile = path.join(here,"data")
        pathFile = path.join(pathFile, "train.csv")
        print(pathFile)
        self.df = pd.read_csv(pathFile)

    def making_print(self):
        print (self.df)