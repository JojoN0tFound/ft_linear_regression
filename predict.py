#!env/bin/python3
import json
import sys
import os
import train
import numpy as np

# check for arguments: '-r' for reseting the thetas
def parsing(av, ac):
	cmp = False
	ngd = False
	if ac > 2 or ac < 2:
		return
	elif ac == 2:
		if av[1] == "-h" or av[1] == "--help":
			print("Classic run: no arguments\n\nOptions:\n-r: reset the 'weights.json' file with theta0 = 0 and theta1 = 0")
			exit()
		if av[1] == "-r":
			if os.path.exists('weights.json'):
				f = open('weights.json', 'w')
				reset = {"t0" : 0, "t1" : 0}
				json.dump(reset, f)
				print("'weights.json' was succesfully reseting with theta0 = 0 and theta1 = 0\n")
				exit()
			else :
				print("'weights.json' file is actually missing so we can't reseting him\n")
				exit()
		if av[1] == "-ngd":
			ngd = True
		if av[1] == "-cmp":
			cmp = True
		return ([cmp, ngd])

# get data.csv
def get_csv(path):
	try:
		csv = np.loadtxt(path, delimiter = ',', skiprows = 1)
	except:
		print ("data.csv file missing")
		sys.exit()
	return [csv[:, 0], csv[:, 1]]

def normalize(data):
	return (data - min(data)) / (max(data) - min(data))

def unnormalize(pred, data):
	return (pred * (max(data) - min(data)) + min(data))

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
	weights = {"t0" : 0, "t1" : 0}
	if os.path.exists('weights.json'):
		f = open('weights.json')
		weights = json.load(f)
		print(f"Go for it with theta0 = {weights['t0']} and theta1 = {weights['t1']}")
	else :
		print(f"'weights.json' file is actually missing so we areusing theta0 = {weights['t0']} and theta1 = {weights['t1']} by default")
	return weights

def check_train(yesno):
	try:
		if yesno == "Y" or yesno == "n":
			return True
		return(error("\nPlease enter 'Y' for yes or 'n' for no"))
	except:
		return(error("\nPlease enter 'Y' for yes or 'n' for no"))

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

def just_compare(args):
	weights = get_weights()
	csv = get_csv('data.csv')
	km = None
	data = normalize_data(km, csv)
	for i in range(len(csv[0])):
		predict = unnormalize(predict_km(data[0][i], weights), data[1])
		print(f"{csv[0][i]} \n--------->   {csv[1][i]}   |   {predict}")
	exit()

def predict():
	args = parsing(sys.argv, len(sys.argv))
	if args[0]:
		just_compare(args)
	km = get_km()
	ask_for_train()
	weights = get_weights()
	if args[1] == False:
		csv = get_csv('data.csv')
		data = normalize_data(km, csv)
		predict = predict_km(data[0][0], weights)
		predict = unnormalize(predict, data[1])
	else:
		predict = predict_km(km, weights)
	print(f"\nThe estimate car price with {km} milleage is: {predict}")

if __name__ == "__main__":
	predict()