import numpy as np
import matplotlib.pyplot as plt

def remove_plot(plot):
	if plot:
		line = plot.pop(0)
		line.remove()

def on_close(event):
	plt.figure(1)
	plt.close()
	exit()

def init_linear_graph(data):
	fig = plt.figure(1)
	plt.title("Linear Regression over dataset")
	plt.xlabel("Mileage (km)")
	plt.ylabel("Prices (USD)")
	kms = list(data.kms)
	prices = list(data.prices)
	points = plt.scatter(kms, prices, color = "pink", label="original dataset values")
	plt.pause(0.001)
	plt.waitforbuttonpress()
	plt.clf()
	plt.title("Linear Regression over dataset")
	plt.xlabel("Normalized Mileage")
	plt.ylabel("Normalized Prices")
	kms = list(data.nrmlz_kms)
	prices = list(data.nrmlz_prices)
	plt.scatter(kms, prices, color = "red", label="Normalized dataset values")
	plt.legend()
	plt.grid(True)
	plt.pause(0.001)
	plt.waitforbuttonpress()
	return fig

def print_fct(data, rocky, fig):
	plt.figure(1)
	x = np.linspace(min(data.nrmlz_kms), max(data.nrmlz_prices), 100)
	line = None
	for theta in rocky.thetas_hist:
		remove_plot(line)
		y = theta[1] * x + theta[0]
		line = plt.plot(x, y)
		plt.pause(0.01)
		fig.canvas.mpl_connect('close_event', on_close)
	plt.waitforbuttonpress()
	plt.close()

def main(data, rocky):
	fig = init_linear_graph(data)
	print_fct(data, rocky, fig)