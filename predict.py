#!env/bin/python3
import json
import sys
import os
import train
import numpy as np
import matplotlib.pyplot as plt

# only for get the input arguments
def parsing(av, ac):
	cmp = False
	if ac < 2:
		return (cmp)
	else:
		for i in range(1, ac):
			if av[i] == "-h" or av[i] == "--help":
				print("Classic run: no arguments\n\nOptions:\n-r:   reset the 'weights.json' file with theta0 = 0 and theta1 = 0\n-cmp: compare the csv's prices with our predict pricess with the csv milleage\n")
				exit()
			elif av[i] == "-r":
				if os.path.exists('weights.json'):
					f = open('weights.json', 'w')
					reset = {"t0" : 0, "t1" : 0, "ngd" : False}
					json.dump(reset, f)
					print("'weights.json' was succesfully reseting with theta0 = 0, theta1 = 0 and ngd = false\n")
					exit()
				else :
					print("'weights.json' file is actually missing so we can't reseting him\n")
					exit()
			elif av[i] == "-cmp":
				cmp = True
			else:
				print("Invalid argument please check usage with the flag [-h] or [--help]")
				exit()
		return (cmp)

# get data.csv
def get_csv(path):
	try:
		csv = np.loadtxt(path, delimiter = ',', skiprows = 1)
	except:
		print ("data.csv file missing")
		sys.exit()
	return [csv[:, 0], csv[:, 1]]

# fct for normalize a list
def normalize(data):
	return (data - min(data)) / (max(data) - min(data))

# fct for get the unnormalized price
def unnormalize(pred, data):
	return (pred * (max(data) - min(data)) + min(data))

# store and normalize data for predict the price
def normalize_data(km, csv):
	data = [[],[]]
	if km:
		data[0].append(km)
	for elem in csv[0]:
		data[0].append(elem)
	data[0] = normalize(data[0])
	data[1] = csv[1]
	return data

# simple fct for print error msg
def error(msg):
	print(msg)
	return False

# fct for check if the user enter a correct milleage
def check_input(km):
	km = float(km)
	try:
		if km == 0:
			return(error('\nNice new car, don\'t need to estimate the price.'))
		if km < 0:
			return(error('\nA car with a negativ mileage is pretty strange.'))
		if km > sys.maxsize:
			return(error('\nhummmm, seem\'s to be a little too much for a random car.'))
		return True
	except:
		return(error('\nError: please a correct number.'))

# fct for get the milleage input
def get_km():
	print('\nHow many milleage has the car ? Enter the amount then press ENTER.')
	km = input()
	while not check_input(km):
		print('So, what is the mileage of your car ?')
		km = input()
	return float(km)

# fct for get t0 and t1 in the 'weights.json' file, if not: use t0 = 0 and t1 = 0 by default
def get_weights():
	wrong_weights = {"t0" : 0, "t1" : 0, "ngd" : False}
	print(f"{'ngd' in wrong_weights}")
	if os.path.exists('weights.json'):
		f = open('weights.json')
		weights = json.load(f)
		if not 'ngd' in weights:
			print(f"'weights.json' file is actually wrong so we are using theta0 = {wrong_weights['t0']}, theta1 = {wrong_weights['t1']} and ngd = {wrong_weights['ngd']} by default")
			return wrong_weights
		print(f"Go for it with theta0 = {weights['t0']}, theta1 = {weights['t1']} and ngd = {weights['ngd']}")
		return weights
	print(f"'weights.json' file is actually missing so we are using theta0 = {wrong_weights['t0']}, theta1 = {wrong_weights['t1']} and ngd = {wrong_weights['ngd']} by default")
	return wrong_weights

# check your response for the trainning
def check_train(yesno):
	try:
		if yesno == "Y" or yesno == "n":
			return True
		return(error("\nPlease enter 'Y' for yes or 'n' for no"))
	except:
		return(error("\nPlease enter 'Y' for yes or 'n' for no"))

# only for ask if you want to train your model right now
def ask_for_train():
	print('\nDo you want to train your model right now ? [Y/n]')
	yesno = input()
	while not check_train(yesno):
		yesno = input()
	if yesno == "Y":
		train.main()

# only the calcul for estimate the car price
def predict_km(km, weights):
	price = weights['t0'] + km * weights['t1']
	return price

# compare our result and the data.csv result
def just_compare(args):
	plt.figure(1)
	plt.title("Linear Regression over dataset")
	plt.xlabel("Mileage (km)")
	plt.ylabel("Prices (USD)")
	weights = get_weights()
	csv = get_csv('data.csv')
	km = None
	pred_prices = []
	if weights['ngd'] == False:
		data = normalize_data(km, csv)
	else:
		data = [[],[]]
		data[0] = csv[0]
		data[1] = csv[1]
	for i in range(len(csv[0])):
		if weights['ngd'] == False:
			predict = unnormalize(predict_km(data[0][i], weights), data[1])
		else:
			predict = predict_km(data[0][i], weights)
		pred_prices.append(predict)
		print(f"{csv[0][i]} \n--------->   {csv[1][i]}   |   {predict}")
	kms = list(csv[0])
	prices = list(csv[1])
	plt.scatter(kms, prices, color = "pink", label="original dataset values")
	plt.scatter(kms, pred_prices, color = "blue", label="predicted dataset values")
	plt.legend()
	plt.pause(0.001)
	plt.waitforbuttonpress()
	plt.close()
	exit()

# a main with a different name
def predict():
	args = parsing(sys.argv, len(sys.argv))
	if args:
		just_compare(args)
	km = get_km()
	ask_for_train()
	weights = get_weights()
	if weights['ngd'] == False:
		csv = get_csv('data.csv')
		data = normalize_data(km, csv)
		predict = predict_km(data[0][0], weights)
		predict = unnormalize(predict, data[1])
	else:
		predict = predict_km(km, weights)
	print(f"\nThe estimate car price with {km} milleage is: {predict}")

if __name__ == "__main__":
	predict()