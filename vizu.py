import numpy as np
import matplotlib.pyplot as plt

# delete a plot in the window
def remove_plot(plot):
	if plot:
		line = plot.pop(0)
		line.remove()

# just if you don't want to continue the visu
def on_close(event):
	plt.figure(1)
	plt.close()
	exit()

# bullshitclass.. yeah, for real
class My_event():
	def __init__(self):
		self.skip = False

	def on_click(self, event):
		self.skip = True

# show the data
def init_linear_graph(data):
	fig = plt.figure(1)
	plt.title("Linear Regression over dataset")
	plt.xlabel("Mileage (km)")
	plt.ylabel("Prices (USD)")
	kms = list(data.kms)
	prices = list(data.prices)
	plt.scatter(kms, prices, color = "pink", label="original dataset values")
	plt.pause(0.001)
	fig.canvas.mpl_connect('close_event', on_close)
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
	fig.canvas.mpl_connect('close_event', on_close)
	plt.waitforbuttonpress()
	return fig

# show how the gradient work and the final result
def print_fct(data, rocky, fig):
	skip = My_event()
	x = np.linspace(min(data.nrmlz_kms), max(data.nrmlz_prices), 100)
	y = 0
	line = None
	print("Loading...")
	for theta in rocky.thetas_hist:
		remove_plot(line)
		if skip.skip:
			break
		y = theta[1] * x + theta[0]
		line = plt.plot(x, y, "-c")
		plt.pause(0.01)
		fig.canvas.mpl_connect('close_event', on_close)
		fig.canvas.mpl_connect('button_press_event', skip.on_click)
	print("Done !")
	plt.clf()
	plt.title("Linear Regression over dataset")
	plt.xlabel("Normalized Mileage")
	plt.ylabel("Normalized Prices")
	kms = list(data.nrmlz_kms)
	prices = list(data.nrmlz_prices)
	y = rocky.thetas[1] * x + rocky.thetas[0]
	plt.plot(x, y, "-g")
	plt.scatter(kms, prices, color = "red", label="Normalized dataset values")
	plt.legend()
	plt.grid(True)
	plt.pause(0.001)
	fig.canvas.mpl_connect('close_event', on_close)
	plt.waitforbuttonpress()
	plt.close()

# again a main...
def main(data, rocky):
	fig = init_linear_graph(data)
	print_fct(data, rocky, fig)
