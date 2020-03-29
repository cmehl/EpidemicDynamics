import os

from input import input_data
import utils
import plot_utils
from particles_cloud import particles_cloud


#---------------------------------
# INITIALIZATION
#---------------------------------

# Input data (and export)
disease_type = "covid19"
input_data = input_data(disease_type)

# Check input data
input_data.check_inputs()

# Clean previous computation and initialize solution folder
utils.clean_init_directory(input_data)

# Export input parameters to keep track of it in results
input_data.export_input()

# Initialize population
population = particles_cloud(input_data)

# Preventive confinement of part of the population
population.set_preventive_confinement(input_data)

# Preventive vaccination campaign
population.perform_vaccination_campaign(input_data)

#---------------------------------
# TIME-STEPPING
#---------------------------------

print("MAIN COMPUTATION \n")

# Initial time
time = 0.0
nb_timestep = 0

# Infected population or not (initially yes)
population_is_infected = True

# Numerotation of saved solution
nb_saved_sol = 0

# Main loop: we stop when there is no one infected anymore
while(population_is_infected):

	print(f">> Updating simulation at time t={time} days")
	print(f"      >>  Size of population: {population.Nb_particles}")
	print(f"      >>  Effective reproduction rate: {population.R_factor:.2f}")
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

	# Compute R factor for current population
	population.compute_R_factor(time, input_data)

	# Save state in h5 file
	if abs(time-nb_saved_sol*input_data.saving_frequency)<0.9*input_data.dt:
		population.export_state_to_file(time, nb_saved_sol, input_data.saving_folder)
		nb_saved_sol += 1


	# Check if there is still someone infected
	population_is_infected = population.check_if_infected()

	# time update
	time += input_data.dt
	nb_timestep += 1

print("\n")

time_end = time - input_data.dt  # We remove one dt else we have a small shift on plot
print(f">> Infection has disappeared after {time_end} day \n")

#---------------------------------
# POST-TREATMENT
#---------------------------------

print("POST-TREATMENT OF COMPUTATION \n")

# Sanity check of incubation times
utils.check_incubation_times(input_data.saving_folder + "/incubation_times.txt")

# Creating images
plot_utils.create_png_images(time_end, input_data)

# Generating video
plot_utils.generate_video(input_data)



