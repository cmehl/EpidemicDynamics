import os
import glob

import h5py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import EllipseCollection



def create_png_images(time_end, input_data):

	# Vectors used in plots
	time_vect = []
	healthy_vect = []
	infected_wo_sympt_vect = []
	infected_with_sympt_vect = []
	recovered_vect = []
	deaths_vect = []

	# Loop on data files
	filelist = glob.glob(input_data.saving_data_folder + '/*.h5')
	for filename in sorted(filelist):

		# Opening h5 file
		hf = h5py.File(filename, 'r')

		# Getting desired datasets
		time = hf.get('TIME')[()]
		nb_timestep = hf.get('NB_TIMESTEP')[()]
		X_vect = hf.get('X')[()]
		Y_vect = hf.get('Y')[()]
		PartState_vect = hf.get('STATE')[()]

		# Closing h5 file
		hf.close()


		# Number of particles
		Nb_part = len(X_vect)


		# Getting statistics: healthy, infected, etc...
		nb_healthy = 0
		nb_infected_wo_sympt = 0
		nb_infected_with_sympt = 0
		nb_recovered = 0
		for i in range(Nb_part):
			a = PartState_vect[i]
			if a==0:
				nb_healthy += 1
			elif a==1:
				nb_infected_wo_sympt += 1
			elif a==2:
				nb_infected_with_sympt += 1
			elif a==3:
				nb_recovered += 1

		nb_deaths = input_data.population_size - Nb_part


		# Appending to vectors
		time_vect.append(time)
		healthy_vect.append(nb_healthy)
		infected_wo_sympt_vect.append(nb_infected_wo_sympt)
		infected_with_sympt_vect.append(nb_infected_with_sympt)
		recovered_vect.append(nb_recovered)
		deaths_vect.append(nb_deaths)

		# Cumulative vectors
		state_4 = np.array(deaths_vect)
		state_4_2 = state_4 + np.array(infected_with_sympt_vect)
		state_4_2_1 = state_4_2 + np.array(infected_wo_sympt_vect)
		state_4_2_1_0 = state_4_2_1 + np.array(healthy_vect)
		state_4_2_1_0_3 = state_4_2_1_0 + np.array(recovered_vect)

		# RGB colors by state
		color_s0 = (0, 0.44, 0.87, 1)
		color_s1 = (1.0, 0.46, 0, 1)
		color_s2 = (1.0, 0, 0.4, 1)
		color_s3 = (0.63, 0, 0.87, 1)
		color_s4 = (0.0, 0.0, 0.0, 1)

		# Creating matplotlib figures
		fig = plt.figure(constrained_layout=True)
		gs = fig.add_gridspec(3, 2)

		ax0 = fig.add_subplot(gs[0, 0])
		ax1 = fig.add_subplot(gs[0, 1])
		ax2 = fig.add_subplot(gs[1:, :])

		# GLOBAL STATISTICS
		ax1.fill_between(time_vect, 0, state_4, color=color_s4, alpha=0.5)
		ax1.fill_between(time_vect, state_4, state_4_2, color=color_s2, alpha=0.5)
		ax1.fill_between(time_vect, state_4_2, state_4_2_1, color=color_s1, alpha=0.5)
		ax1.fill_between(time_vect, state_4_2_1, state_4_2_1_0, color=color_s0, alpha=0.5)
		ax1.fill_between(time_vect, state_4_2_1_0, state_4_2_1_0_3, color=color_s3, alpha=0.5)


		ax1.set_xlim(0.0, time_end)
		ax1.set_ylim(0, input_data.population_size)

		ax1.set_title("Evolution of disease", fontsize=10)

		# Setting only min and max ticks
		ax1.set_xticks([0.0, time_end])
		ax1.set_yticks([0.0, input_data.population_size])
		
		# labels
		ax1.set_xlabel("Time [days]", fontsize=8)
		ax1.set_ylabel("Population [-]", fontsize=8)


		# REPRESENTATION OF POPULATION
		# collection related quantities
		size = 2.0*input_data.radius

		# color function of states
		color = []
		for i in range(Nb_part):
			if PartState_vect[i]==0:
				color.append(color_s0)
			elif PartState_vect[i]==1:
				color.append(color_s1)
			elif PartState_vect[i]==2:
				color.append(color_s2)
			elif PartState_vect[i]==3:
				color.append(color_s3)

		# data
		offsets = list(zip(X_vect, Y_vect))

		# Plot with points respecting given radius
		ec = EllipseCollection(widths=size, heights=size, angles=0, units='xy',
                                       offsets=offsets, transOffset=ax2.transData)
		ec.set_facecolor(color)
		ec.set_edgecolor(color)

		ax2.add_collection(ec)

		# Disabling axis
		ax2.axes.get_yaxis().set_visible(False)
		ax2.axes.get_xaxis().set_visible(False)

		ax2.set_aspect("equal")



		# PLOTS WITH LEGENDS
		# Disabling axis
		ax0.axes.get_yaxis().set_visible(False)
		ax0.axes.get_xaxis().set_visible(False)
		ax0.spines['right'].set_visible(False)
		ax0.spines['top'].set_visible(False)
		ax0.spines['bottom'].set_visible(False)
		ax0.spines['left'].set_visible(False)

		ax0.plot([0.05], [0.15], color = color_s0, ls="", marker="o", markersize=7)
		ax0.plot([0.05], [0.30], color = color_s1, ls="", marker="o", markersize=7)
		ax0.plot([0.05], [0.45], color = color_s2, ls="", marker="o", markersize=7)
		ax0.plot([0.05], [0.60], color = color_s3, ls="", marker="o", markersize=7)
		ax0.plot([0.05], [0.75], color = color_s4, ls="", marker="o", markersize=7)

		ax0.text(0.12, 0.115, "Healthy", fontsize=8)
		ax0.text(0.12, 0.265, "Infected without symptoms", fontsize=8)
		ax0.text(0.12, 0.415, "Infected with symptoms", fontsize=8)
		ax0.text(0.12, 0.565, "Recovered", fontsize=8)
		ax0.text(0.12, 0.715, "Dead", fontsize=8)

		ax0.set_xlim([0,1])
		ax0.set_ylim([0,1])
		ax0.set_aspect("equal")



		# Finalizing
		# fig.tight_layout()
		fig.savefig(input_data.saving_images_folder + "/image_step_{:05d}.png".format(nb_timestep), dpi=250)
		plt.close(fig)



def generate_video(input_data):

	os.chdir(input_data.saving_images_folder)
	os.system("ffmpeg -r 20 -i image_step_%05d.png -vcodec mpeg4 -y movie.mp4")
	os.chdir("..")

