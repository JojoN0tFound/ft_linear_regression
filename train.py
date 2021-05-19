import json
import sys
import os
import pandas as pd
import vizu as vz

def parsing(av, ac):
    if ac > 2 or ac < 2:
        return
    elif ac == 2:
        return

def uptade_weights(weights):
    if os.path.exists('weights.json'):
        f = open('weights.json', 'w')
        json.dump(weights, f)
    return

class Dataset():
    def __init__(self, data = None, path = None):
        self.data = data
        if path != None:
            self.get_csv(path)
        self.kms = self.data["km"]
        self.prince = self.data["price"]
        self.standartize_data()
        self.stdz_kms = self.data["km"]
        self.stdz_prince = self.data["price"]

    def get_csv(self, path):
        try :
            self.data = pd.read_csv(path)
            self.data["km"] = pd.to_numeric(self.data["km"], downcast='float')
            self.data["price"] = pd.to_numeric(self.data["price"], downcast='float')
        except Exception as e:
            print(e)
            exit()

    def standartize_data(self):
        return

class Rocky():
    def __init__(self, data):
        self.data = data
        self.t0 = 0.0
        self.t1 = 0.0
        self.old_t0 = 0.0
        self.old_t1 = 0.0

if __name__ == "__main__":
    parsing(sys.argv, len(sys.argv))
    data = Dataset(path = 'data.csv')
    rocky = Rocky(data)
    weights = 0
    uptade_weights(weights)
