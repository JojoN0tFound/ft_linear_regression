#!env/bin/python3
import json
import sys
import os
import time
import numpy as np
import vizu as vz

def parsing(av, ac):
	vizu = False
	ngd = False
	if ac == 2:
		if av[1] == "-h" or av[1] == "--help":
			print("Classic run: no arguments\n\nOptions:\n-v: active the visualisator (not working)\n-ngd: use variance and covariance instead of a descent gradient")
			exit()
		if av[1] == "-v":
			vizu = True
		if av[1] == "-ngd":
			ngd = True
	return([vizu, ngd])

# 
def uptade_weights(t, cost):
	weights = {"t0": t[0], "t1": t[1]}
	if os.path.exists('weights.json'):
		f = open('weights.json', 'w')
		json.dump(weights, f)
		print(f"We got a cost of: {cost}")
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
		self.kms = self.data[:,0]
		self.prices = self.data[:,1]
		self.get_mean_std()
		self.get_variance_covar()
		self.normalize_data()

	# get the csv data
	def get_csv(self, path):
		try:
			self.data = np.loadtxt(path, delimiter = ',', skiprows = 1)
		except:
			print ("data.csv file missing")
			sys.exit()

	# get the variance and the covariance of the dataset
	def get_variance_covar(self):
		self.variance_kms = sum([(x - self.mean_kms)**2 for x in self.kms])
		self.variance_prices = sum([(x - self.mean_prices)**2 for x in self.prices])
		self.covar = 0.0
		for i in range(len(self.kms)):
			self.covar += (self.kms[i] - self.mean_kms) * (self.prices[i] - self.mean_prices)

	# get the mean of the dataset
	def get_mean_std(self):
		self.mean_kms = self.kms.mean()
		self.mean_prices = self.prices.mean()

	# normalize data
	def normalize_data(self):
		nrmlz_kms, nrmlz_prices = [], []
		nrmlz_kms = (self.data[:,0] - min(self.data[:,0])) / (max(self.data[:,0]) - min(self.data[:,0]))
		nrmlz_prices = (self.data[:,1] - min(self.data[:,1])) / (max(self.data[:,1]) - min(self.data[:,1]))
		self.nrmlz_kms = nrmlz_kms
		self.nrmlz_prices = nrmlz_prices

class Rocky():
	def __init__(self, data, learningRate = 0.1, learningRateGoal = 0.0000001):
		self.data = data
		self.m = len(self.data.kms)
		self.x = self.data.nrmlz_kms
		self.y = self.data.nrmlz_prices
		self.thetas = [0.0, 0.0]
		self.thetas_hist = [[0.0, 0.0]]
		self.dt = [0.0, 0.0]
		self.dt_hist = [[0.0, 0.0]]
		self.final_thetas = [0.0, 0.0]
		self.cost = 1
		self.cost_hist = [1]
		self.learningRate = learningRate
		self.learningRateGoal = learningRateGoal
		self.min_cost_diff = 0.0000001
		self.iteration = 0
		
	def predict_price(self, t, km):
		return(t[0] + (t[1] * km))

	# fct for get the thetas using the variance and the covariance
	def get_coef(self):
		self.final_thetas[1] = self.data.covar / self.data.variance_kms
		self.final_thetas[0] = self.data.mean_prices - self.final_thetas[1] * self.data.mean_kms

	# fct for get thetas and the derivate
	def update_thetas(self, pred):
		self.dt[0] = (1 / self.m) * sum(pred - self.y)
		self.dt[1] = (1 / self.m) * sum((pred - self.y) * self.x)

		self.thetas[0] -= self.learningRate * self.dt[0]
		self.thetas[1] -= self.learningRate * self.dt[1]

		self.thetas_hist.append(self.thetas.copy())
		self.dt_hist.append(self.dt.copy())

	def get_new_cost(self, pred):
		self.cost = (1 / (2 * self.m)) * sum((pred - self.y) ** 2)
		self.cost_hist.append(self.cost.copy())

	def gradient(self):
		while self.learningRate > self.learningRateGoal:
			self.iteration += 1
			curr_pred = self.predict_price(self.thetas, self.x)
			self.get_new_cost(curr_pred)
			self.update_thetas(curr_pred)
			if abs(self.cost > self.cost_hist[-2]) > self.min_cost_diff:
				break
			if self.cost > self.cost_hist[-2]:
				print(f"down ->{self.iteration}")
				self.cost = self.cost_hist[-2]
				self.thetas = self.thetas_hist[-2]
				self.learningRate /= 10

		self.final_thetas = self.thetas

def main():
	args = parsing(sys.argv, len(sys.argv))
	data = Dataset(path = 'data.csv')
	# precision = enter_precision()
	# learning_rate = enter_learning_rate()
	# rocky = Rocky(data, learning_rate, precision)
	rocky = Rocky(data)
	if args[1] == True:
		rocky.get_coef()
	else:
		rocky.gradient()
	uptade_weights(rocky.final_thetas, rocky.cost)
	if args[0] == True:
		vz.main(data, rocky)

if __name__ == "__main__":
	main()
