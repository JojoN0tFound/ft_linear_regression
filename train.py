import json
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

vizu = False
ngd = False

def ft_draw_graph(data, thetas):
	kilometers = data.data.stdz_kms
	prices = data.data.stdz_prices
	x = np.linspace(min(kilometers), max(kilometers), 100)
	y = thetas[1] * x + thetas[0]
	plt.plot(x, y, "-r")
	plt.plot(kilometers, prices, "bo")
	plt.xlabel("kilometers normalized")
	plt.ylabel("prices normalized")
	plt.title("Linear regression graph")
	plt.show()

def parsing(av, ac):
	if ac > 2 or ac < 2:
		return
	elif ac == 2:
		if av[1] == "-h" or av[1] == "--help":
			print("Classic run: no arguments\n\nOptions:\n-v: active the visualisator (not working)\n-ngd: use variance and covariance instead of a descent gradient")
			exit()
		if av[1] == "-v":
			vizu = True
		if av[1] == "-ngd":
			ngd = True
		return

# 
def uptade_weights(t):
	weights = {"t0": t[0], "t1": t[1]}
	if os.path.exists('weights.json'):
		f = open('weights.json', 'w')
		json.dump(weights, f)
		print(f"We update the 'weights.json file with t0 = {weights['t0']} and t1 = {weights['t1']}")
	return

# Learning ratio, an ideal value here is 1, a too big value can causes the result to diverge
def enter_learning_rate():
	try:
		learning_rate = float(input("Learning rate : "))
	except:
		print ("type error")
		sys.exit()
	return (learning_rate)

# Precision is the "maximum OK value for cost function", useful to end the program a bit faster, but reduce results accuracy, 0.01035 is fast
def enter_precision():
	try:
		precision = float(input("Desired precision : "))
	except:
		print ("type error")
		sys.exit()
	return (precision)

# class for read and treat the dataset before train
class Dataset():
	def __init__(self, data = None, path = None):
		self.data = data
		if path != None:
			self.get_csv(path)
		self.kms = self.data["km"]
		self.prices = self.data["price"]
		self.get_mean_std()
		self.get_variance_covar()
		self.standartize_data()
		self.stdz_kms = self.data["stdz_kms"]
		self.stdz_prices = self.data["stdz_prices"]
		# self.data["std_kms"] = self.std_kms
		# self.data["std_prices"] = self.std_prices

	# get the csv data
	def get_csv(self, path):
		try :
			self.data = pd.read_csv(path)
			self.data["km"] = pd.to_numeric(self.data["km"], downcast='float')
			self.data["price"] = pd.to_numeric(self.data["price"], downcast='float')
		except Exception as e:
			print(e)
			exit()

	# get the variance and the covariance of the dataset
	def get_variance_covar(self):
		self.variance_kms = sum([(x - self.mean_kms)**2 for x in self.kms])
		self.variance_prices = sum([(x - self.mean_prices)**2 for x in self.prices])
		self.covar = 0.0
		for i in range(len(self.kms)):
			self.covar += (self.kms[i] - self.mean_kms) * (self.prices[i] - self.mean_prices)

	# get the mean and the standart deviation of the dataset
	def get_mean_std(self):
		self.mean_kms = self.data.mean()["km"]
		self.mean_prices = self.data.mean()["price"]
		self.std_kms = self.data.std()["km"]
		self.std_prices = self.data.std()["price"]

	# standardize data using z-score: (value - mean) / standart deviation
	def standartize_data(self):
		stdz_kms, stdz_prices = [], []
		stdz_kms = (self.data["km"] - min(self.data["km"])) / (max(self.data["km"]) - min(self.data["km"]))
		stdz_prices = (self.data["price"] - min(self.data["price"])) / (max(self.data["price"]) - min(self.data["price"]))
		self.data["stdz_kms"] = stdz_kms
		self.data["stdz_prices"] = stdz_prices

class Rocky():
	def __init__(self, data, learningRate = 1, precision = 0.01035):
		self.data = data
		self.thetas = [0.0, 0.0]
		self.tmp = [0.0, 0.0]
		self.final_thetas = [0.0, 0.0]
		self.cost = 0
		self.learningRate = learningRate
		self.precision = precision
		
	def predict_price(self, t, km):
		return(t[0] + (t[1] * km))

	# fct for get the thetas using the variance and the covariance
	def get_coef(self):
		self.final_thetas[1] = self.data.covar / self.data.variance_kms
		self.final_thetas[0] = self.data.mean_prices - self.final_thetas[1] * self.data.mean_kms

	def gradient(self):
		m = len(self.data.kms)
		x = self.data.stdz_kms
		y = self.data.stdz_prices
		i = 0
		for i in range(m):
			curr_pred = self.predict_price(self.thetas, x[i])
			self.tmp[0] = self.tmp[0] + curr_pred - y[i]
			self.tmp[1] = self.tmp[1] + (curr_pred - y[i]) * x[i]
		self.thetas[0] = self.learningRate * (1/m) * self.tmp[0]
		self.thetas[1] = self.learningRate * (1/m) * self.tmp[1]
		# self.thetas.append([0.0, 0.0])
		# while True:
		# 	# print(curr_pred)
		# 	tmp = 0
		# 	for j in range(m):
		# 		tmp = tmp + pow(curr_pred[j] - y[j], 2)
		# 	self.cost = (1 / (2 * m)) * tmp
		# 	print(self.cost)
		# 	if abs(self.cost) <= self.precision:
		# 		break
		# 	for j in range(m):
		# 		self.tmp[0] = self.tmp[0] + x[j] * (curr_pred[j] - y[j])
		# 		self.tmp[1] = self.tmp[1] + (curr_pred[j] - y[j]) * x[j]
		# 	new_thetas = [self.thetas[i][0] - (self.learningRate * (1 / m) * self.tmp[0]), self.thetas[i][0] - (self.learningRate * (1 / m) * self.tmp[1])]
		# 	self.thetas.append(new_thetas)
		# 	i = i + 1
		# print(self.thetas)
		self.final_thetas = self.thetas

	# def error(self):


def train():
	parsing(sys.argv, len(sys.argv))
	data = Dataset(path = 'data.csv')
	# precision = enter_precision()
	# learning_rate = enter_learning_rate()
	# rocky = Rocky(data, learning_rate, precision)
	rocky = Rocky(data)
	if ngd == True:
		rocky.get_coef()
	else:
		rocky.gradient()
	uptade_weights(rocky.final_thetas)
	if vizu == True:
		ft_draw_graph(data, rocky.final_thetas)

if __name__ == "__main__":
	train()
