import os

from input import input_data
import utils
import plot_utils
from particles_cloud import particles_cloud


#---------------------------------
# INITIALIZATION
#---------------------------------

# Input data
input_data = input_data()

# Clean previous computation and initialize solution folder
utils.clean_init_directory(input_data)

# Initialize population
population = particles_cloud(input_data)

# Preventive confinement of part of the population
population.set_preventive_confinement(input_data)

#---------------------------------
# TIME-STEPPING
#---------------------------------

print("MAIN COMPUTATION \n")

# Initial time
time = 0.0
nb_timestep = 0

# Main loop
while(time<=input_data.t_max):

	print(f">> Updating simulation at time t={time} days")
	print(f"      >>  Size of population: {population.Nb_particles}")
	print(f"      >>  Deaths: {input_data.population_size-population.Nb_particles}")

	# Move particles
	population.move(input_data.dt)

	# Resolve wall collisions
	population.resolve_wall_collisions()

	# Resolve inter-particles collisions (including spreading the disease)
	population.resolve_particle_collisions(time, input_data)

	# Resolve change of state
	population.change_person_state(time, input_data)

	# Remove deads
	population.remove_deads()

	# Save state in h5 file
	population.export_state_to_file(time, nb_timestep, input_data.saving_data_folder)

	# time update
	time += input_data.dt
	nb_timestep += 1

print("\n")

#---------------------------------
# POST-TREATMENT
#---------------------------------

print("POST-TREATMENT OF COMPUTATION \n")

# Creating images
plot_utils.create_png_images(input_data)

# Generating video
plot_utils.generate_video(input_data)



