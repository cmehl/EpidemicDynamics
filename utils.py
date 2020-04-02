
import os
import shutil

import numpy as np
from scipy.stats import gamma, lognorm, uniform

import matplotlib.pyplot as plt

#---------------------------------
# PARTICLE RELATED FUNCTIONS
#---------------------------------

def vel_components_from_angle(vel_angle, vel_norm):
	return (np.cos(vel_angle)*vel_norm, np.sin(vel_angle)*vel_norm)


#---------------------------------
# PROBABILITY FUNCTIONS
#---------------------------------


def compute_uniform_cdf(min_val, max_val, saving_folder):

	# range of values for which CDF is computed (100 is arbitrary and should be high enough)
	x_range = np.linspace(0,50,1000)

	# Cumulative distribution function
	pdf = uniform.pdf(x_range, loc=min_val, scale=(max_val-min_val)) 
	cdf = uniform.cdf(x_range, loc=min_val, scale=(max_val-min_val)) 

	# Storing cdf, pdf and x_range vectors together
	proba_mat = np.vstack([x_range,cdf,pdf]).T

	return proba_mat


def compute_lognormal_cdf(mean_val, std_val, saving_folder):

	# Converting mean and std to lognormal parameters mu and sigma
	sigma = np.sqrt( np.log( (std_val**2/mean_val**2) + 1.0 ))
	mu = np.log(mean_val) - 0.5 * np.log( (std_val**2/mean_val**2) + 1.0 )

	# range of values for which CDF is computed (100 is arbitrary and should be high enough)
	x_range = np.linspace(0,50,1000)

	# Cumulative distribution function
	pdf = lognorm.pdf(x_range, s=sigma, scale=np.exp(mu)) 
	cdf = lognorm.cdf(x_range, s=sigma, scale=np.exp(mu)) 

	# Storing cdf, pdf and x_range vectors together
	proba_mat = np.vstack([x_range,cdf,pdf]).T

	return proba_mat



def compute_gamma_cdf(mean_val, std_val, saving_folder):

	# Converting mean and std to gamma parameters
	k = (mean_val / std_val)**2
	theta = std_val**2 / mean_val

	# range of values for which CDF is computed
	x_range = np.linspace(0,50,1000)

	# Cumulative distribution function
	pdf = gamma.pdf(x_range, a = k, scale=theta)
	cdf = gamma.cdf(x_range, a = k, scale=theta)

	# Storing cdf, pdf and x_range vectors together
	proba_mat = np.vstack([x_range,cdf,pdf]).T

	return proba_mat



# For a given y value, invert an abitrary CDF
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



def check_disease_times(folder):

	incubation_file =  folder + "/incubation_times.txt"
	death_file =  folder + "/onset_to_death_times.txt"
	recovery_file =  folder + "/onset_to_recovery_times.txt"

	try:
		incubations_times = np.loadtxt(incubation_file)
		mean_incub = np.mean(incubations_times)
		std_incub = np.std(incubations_times)
	except OSError:
		mean_incub = 0.0
		std_incub = 0.0

	try:
		death_times = np.loadtxt(death_file)
		mean_death = np.mean(death_times)
		std_death = np.std(death_times)
	except OSError:
		mean_death = 0.0
		std_death = 0.0

	try:
		recovery_times = np.loadtxt(recovery_file)
		mean_recov = np.mean(recovery_times)
		std_recov = np.std(recovery_times)
	except OSError:
		mean_recov = 0.0
		std_recov = 0.0

	print(f">> Effective mean incubation time: {mean_incub} days")
	print(f">> Effective standard deviation of incubation time: {std_incub} days\n")
	print("")
	print(f">> Effective mean onset to death time: {mean_death} days")
	print(f">> Effective standard deviation of onset to death time: {std_death} days\n")
	print("")
	print(f">> Effective mean onset to recovery time: {mean_recov} days")
	print(f">> Effective standard deviation of onset to recovery time: {std_recov} days\n")








