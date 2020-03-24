
import os
import shutil

import numpy as np


#---------------------------------
# PARTICLE RELATED FUNCTIONS
#---------------------------------

def vel_components_from_angle(vel_angle, vel_norm):
	return (np.cos(vel_angle)*vel_norm, np.sin(vel_angle)*vel_norm)


#---------------------------------
# MISC FUNCTIONS
#---------------------------------

def clean_init_directory(input_data):

	# Remove folder if they already exist
	if os.path.exists(input_data.saving_data_folder):
		shutil.rmtree(input_data.saving_data_folder)
	#
	if os.path.exists(input_data.saving_images_folder):
		shutil.rmtree(input_data.saving_images_folder)

	# Create folder for solution
	os.makedirs(input_data.saving_data_folder)
	os.makedirs(input_data.saving_images_folder)






