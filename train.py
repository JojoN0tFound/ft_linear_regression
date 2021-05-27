#!env/bin/python3
import json
import sys
import os
import numpy as np
import vizu as vz

# only for get the input arguments
def parsing(av, ac):
	vizu = False
	ngd = False
	if ac < 2:
		return([vizu, ngd])
	else:
		for i in range(1, ac):
			if av[i] == "-h" or av[i] == "--help":
				print("Classic run: no arguments\n\nOptions (only one):\n-v:   active the visualisator\n-ngd: use variance and covariance instead of a gradient descent\n")
				exit()
			elif av[i] == "-v":
				vizu = True
			elif av[i] == "-ngd":
				ngd = True
			else:
				print("Invalid argument please check usage with the flag [-h] or [--help]")
				exit()
	if vizu and ngd:
		print("[-ngd] and [-v] can't be both activate")
		exit()
	return([vizu, ngd])

# write the right thetas in the file
def uptade_weights(t, rocky, ngd):
	weights = {"t0": t[0], "t1": t[1], "ngd": ngd}
	f = open('weights.json', 'w')
	json.dump(weights, f)
	if not ngd:
		print(f"We got a cost of: {rocky.cost} in {rocky.iteration} loop")
	print(f"ngd is {ngd}")
	print(f"We update the 'weights.json file with t0 = {weights['t0']} and t1 = {weights['t1']}")
	return

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

# class for train our dataset
class Rocky():
	def __init__(self, data, learningRate = 0.1, learningRateGoal = 0.0000001, precision = 15):
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
		self.min_cost_diff = 10 ** -precision
		self.iteration = 0

	# only for predict the price
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

	# get the cost with the lastest thethas
	def get_new_cost(self, pred):
		self.cost = (1 / (2 * self.m)) * sum((pred - self.y) ** 2)
		self.cost_hist.append(self.cost.copy())

	# loop of training
	def gradient(self):
		while self.learningRate > self.learningRateGoal:
			self.iteration += 1
			curr_pred = self.predict_price(self.thetas, self.x)
			self.get_new_cost(curr_pred)
			self.update_thetas(curr_pred)
			if abs(self.cost - self.cost_hist[-2]) < self.min_cost_diff:
				break
			if self.cost > self.cost_hist[-2]:
				self.cost = self.cost_hist[-2]
				self.thetas = self.thetas_hist[-2]
				self.learningRate /= 10

		self.final_thetas = self.thetas

# just a main dude
def main():
	args = parsing(sys.argv, len(sys.argv))
	data = Dataset(path = 'data.csv')
	rocky = Rocky(data)
	if args[1] == True:
		rocky.get_coef()
	else:
		rocky.gradient()
	uptade_weights(rocky.final_thetas, rocky, args[1])
	if args[0] == True:
		vz.main(data, rocky)

if __name__ == "__main__":
	main()
