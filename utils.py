
import os
import shutil

import numpy as np
from scipy.stats import gamma

import matplotlib.pyplot as plt

#---------------------------------
# PARTICLE RELATED FUNCTIONS
#---------------------------------

def vel_components_from_angle(vel_angle, vel_norm):
	return (np.cos(vel_angle)*vel_norm, np.sin(vel_angle)*vel_norm)


#---------------------------------
# PROBABILITY FUNCTIONS
#---------------------------------

# def truncated_gaussian(min_val, max_val, mean_val, std_val):

# 	# Input for truncated gaussian
# 	a, b = (min_val - mean_val) / std_val, (max_val - mean_val) / std_val

# 	# range of values for which CDF is computed
# 	x_range = np.linspace(min_val,max_val,1000)

# 	# Cumulative distribution function
# 	cdf = truncnorm.cdf(x_range, a, b, loc = mean_val, scale = std_val)

# 	cdf_mat = np.vstack([x_range,cdf]).T

# 	return cdf_mat

def gamma_cdf(mean_val, std_val, saving_folder):

	# Input for gamma law
	a = 2

	# range of values for which CDF is computed
	x_range = np.linspace(0,50,1000)

	# Cumulative distribution function
	pdf = gamma.pdf(x_range, a, mean_val, std_val)
	cdf = gamma.cdf(x_range, a, mean_val, std_val)

	cdf_mat = np.vstack([x_range,cdf]).T

	# Plot pdf to sanity check
	fig, ax = plt.subplots()
	ax.plot(x_range, pdf, color="k", lw=2)
	ax.set_xlabel("days")
	ax.set_ylabel("pdf")
	ax.grid(ls="--", alpha=0.5)
	fig.savefig(saving_folder + "/pdf.png", dpi=250)

	return cdf_mat


def invert_cdf(y, cdf_mat):
	""" y is a number between 0 and 1
	 cdf is a vector representing a CDF (growing function)
	 (it goes from (val_min,vam_max) to [0,1]) """

	# Unpacking cdf
	x = cdf_mat[:,0]
	cdf = cdf_mat[:,1]

	# By default inverse of y is max(x)
	inv_y = np.max(x)

	for i in range(len(cdf)):
		if cdf[i]>=y:
			inv_y = x[i]
			break

	return inv_y

#---------------------------------
# MISC FUNCTIONS
#---------------------------------

def clean_init_directory(input_data):

	# Remove folder if they already exist
	if os.path.exists(input_data.saving_folder):
		shutil.rmtree(input_data.saving_folder)

	# Create folder for solution
	os.makedirs(input_data.saving_folder)

	# Create sub-folder
	os.makedirs(input_data.saving_folder + "/images")
	os.makedirs(input_data.saving_folder + "/solutions")

	# Initializing incubation times file
	with open(input_data.saving_folder + "/incubation_times.txt", "a") as f:
		pass



def check_incubation_times(file_incubation):

	incubations_times = np.loadtxt(file_incubation)
	mean_incub = np.mean(incubations_times)
	std_incub = np.std(incubations_times)

	print(f">> Effective mean incubation time: {mean_incub} days")
	print(f">> Effective standard deviation of incubation time: {std_incub} days\n")









