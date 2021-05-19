import json
import sys
import os

# check for arguments: '-r' for reseting the thetas
def parsing(av, ac):
    if ac > 2 or ac < 2:
        return
    elif ac == 2:
        if av[1] == "-r":
            if os.path.exists('weights.json'):
                f = open('weights.json', 'w')
                reset = {"t0" : 0, "t1" : 0}
                json.dump(reset, f)
                print("'weights.json' was succesfully reseting with theta0 = 0 and theta1 = 0\n")
            else :
                print("'weights.json' file is actually missing so we can't reseting him\n")
        return

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

# fct for get the input milleage
def get_km():
    print('\nHow many milleage has the car ? Enter the amount then press ENTER.')
    km = input()
    while not check_input(km):
        print('So, what is the mileage of your car ?')
        km = input()
    return float(km)

# fct for get t0 and t1 in the 'weights.json' file, if not use t0 = 0 and t1 = 0 by default
def get_weights():
    weights = {"t0" : 0, "t1" : 0}
    if os.path.exists('weights.json'):
        f = open('weights.json')
        weights = json.load(f)
        print(f"Go for it with theta0 = {weights['t0']} and theta1 = {weights['t1']}")
    else :
        print(f"'weights.json' file is actually missing so we using theta0 = {weights['t0']} and theta1 = {weights['t1']} by default")
    return weights

# only the calcul for estimate the car price
def predict_km(km, weights):
    price = weights['t0'] + km * weights['t1']
    return price

if __name__ == "__main__":
    parsing(sys.argv, len(sys.argv))
    weights = get_weights()
    km = get_km()
    predict = predict_km(km, weights)
    print(f"\nThe estimate car price with {km} milleage is: {predict}")