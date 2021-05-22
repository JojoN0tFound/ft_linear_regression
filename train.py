import json
import sys
import os
import pandas as pd
import vizu as vz

def parsing(av, ac):
	if ac > 2 or ac < 2:
		return
	elif ac == 2:
		if av[1] == "-h" or av[1] == "--help":
			print("Classic run: no arguments\n\nOptions:\n-v: active the visualisator (not working)")
			exit()
		return

# 
def uptade_weights(t0, t1):
	weights = {"t0": t0, "t1": t1}
	if os.path.exists('weights.json'):
		f = open('weights.json', 'w')
		json.dump(weights, f)
		print(f"We update the 'weights.json file with t0 = {weights['t0']} and t1 = {weights['t1']}")
	return

# class for read and treat the dataset before train
class Dataset():
	def __init__(self, data = None, path = None):
		self.data = data
		if path != None:
			self.get_csv(path)
		self.kms = self.data["km"]
		self.prices = self.data["price"]
		self.get_mean_std()
		self.standartize_data()
		self.stdz_kms = self.data["stdz_kms"]
		self.stdz_prices = self.data["stdz_prices"]

	# get the csv data
	def get_csv(self, path):
		try :
			self.data = pd.read_csv(path)
			self.data["km"] = pd.to_numeric(self.data["km"], downcast='float')
			self.data["price"] = pd.to_numeric(self.data["price"], downcast='float')
		except Exception as e:
			print(e)
			exit()

	# get the mean and the standart deviation of the dataset
	def get_mean_std(self):
		self.mean_kms = self.data.mean()["km"]
		self.mean_prices = self.data.mean()["price"]
		self.std_kms = self.data.std()["km"]
		self.std_prices = self.data.std()["price"]

	# standardize data using z-score: (value - mean) / standart deviation
	def standartize_data(self):
		stdz_kms, stdz_prices = [], []
		for i in self.data.index:
			stdz_kms.append((self.data["km"][i] - self.mean_kms) / self.std_kms)
			stdz_prices.append((self.data["price"][i] - self.mean_prices) / self.std_prices)
		self.data["stdz_kms"] = stdz_kms
		self.data["stdz_prices"] = stdz_prices


class Rocky():
	def __init__(self, data):
		self.data = data
		self.t0 = 0.0
		self.t1 = 0.0
		self.tmp_t0 = 0.0
		self.tmp_t1 = 0.0
		self.old_t0 = 0.0
		self.old_t1 = 0.0
		self.learningRate = 0.0
		
	def predict_price(self, t0, t1, km):
		return(t0 + (t1 * km))

def train():
	parsing(sys.argv, len(sys.argv))
	data = Dataset(path = 'data.csv')
	rocky = Rocky(data)
	print(f"{data.data}")
	uptade_weights(rocky.t0, rocky.t1)

if __name__ == "__main__":
	train()
