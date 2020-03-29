import random

import numpy as np
import scipy.spatial.distance as d

import h5py

from particle import particle


class particles_cloud(object):

	#---------------------------------
	# INITIALIZATION
	#---------------------------------

	def __init__(self, input_data):

		# Radius of particles (sames for all)
		self.radius = input_data.radius

		# Storing domain size
		self.domain_size = input_data.domain_size

		# Initial number of particles is population size
		self.Nb_particles = input_data.population_size

		# Ensemble of particles is stored in a dictionary
		self.particles_list = []

		# We make one particle to be ill
		index_ill = random.randrange(input_data.population_size)

		# Initialize cloud of particles
		for i in range(input_data.population_size):
			part_id = i
			if i==index_ill:
				state = 1
			else:
				state = 0
			new_particle = particle(part_id, state, input_data)
			self.particles_list.append(new_particle)

		# R_factor initially set to zero
		self.R_factor = 0.0


	#---------------------------------
	# PEOPLE MOVEMENTS
	#---------------------------------

	def move(self, dt):
		""" Routine to update particles positions """
		for part in self.particles_list:
			part.move_particle(dt)



	def resolve_wall_collisions(self):
		""" Reflect particles that are close to walls"""

		# Loop on particles
		for part in self.particles_list:

			# x direction
			if((part.x <= part.radius and part.vx<0)
				or (part.x >= self.domain_size[0]-part.radius and part.vx>0)):
				part.reflect_wall("x")

			# y direction
			if((part.y <= part.radius and part.vy<0)
				or (part.y >= self.domain_size[1]-part.radius and part.vy>0)):
				part.reflect_wall("y")



	def resolve_particle_collisions(self, time, input_data):

		# Get positions matrix
		position = self.get_position_matrix()
		nop = self.Nb_particles

		# make 3D arrays with repeated position vectors to form combinations
		# diff_i[i][j] = position[i]
		# diff_j[i][j] = position[j]
		# diff[i][j] = vector pointing from i to j
		# norm[i][j] = sqrt( diff[i][j]**2 )
		diff_i = np.repeat(position.reshape(1, nop, 2) , nop, axis=1).reshape(nop, nop, 2)
		diff_j = np.repeat(position.reshape(1, nop, 2) , nop, axis=0)
		diff = diff_j - diff_i
		norm = np.linalg.norm(diff, axis=2)

		# make norm upper triangular (excluding diagonal)
		# This prevents double counting the i,j and j,i pairs
		collided = np.triu(norm <2.0 * self.radius, k=1)

		for i, j in zip(*np.nonzero(collided)):
			# unit vector from i to j
			unit = diff[i][j] / norm[i][j]

			# flip their velocity along the axis given by `unit`
			# and reduce momentum on that axis by 10%
			vel_diff_i = 2.0 * np.dot(unit, self.particles_list[i].V) * unit
			self.particles_list[i].vx -= vel_diff_i[0]
			self.particles_list[i].vy -= vel_diff_i[1]
			#
			vel_diff_j = 2.0 * np.dot(unit, self.particles_list[j].V) * unit
			self.particles_list[j].vx -= vel_diff_j[0]
			self.particles_list[j].vy -= vel_diff_j[1]

			# Update velocities vectors
			self.particles_list[i].V[0] = self.particles_list[i].vx
			self.particles_list[i].V[1] = self.particles_list[i].vy
			#
			self.particles_list[j].V[0] = self.particles_list[j].vx
			self.particles_list[j].V[1] = self.particles_list[j].vy

			# push particle j to be 1 unit from i
			dist_diff_j = ( 2.0 * self.radius - norm[i][j] ) * unit
			self.particles_list[j].x  += dist_diff_j[0]
			self.particles_list[j].y  += dist_diff_j[1]


			# Propagating infection: particle j
			if ((self.particles_list[i].state==1 or self.particles_list[i].state==2) and
				self.particles_list[j].state==0 and self.particles_list[j].is_vaccinated==False):

				# Infection of particle j with a probability infection_contact_prob
				rand_num = random.uniform(0.0, 1.0)

				if rand_num < input_data.infection_contact_prob:

					# Set state to infected without symptoms
					self.particles_list[j].get_infected()
					self.particles_list[j].set_infection_time(time)

					# Set a random incubation period
					incubation_period = random.uniform(input_data.incubation_period[0], 
														input_data.incubation_period[1])

					self.particles_list[j].set_incubation_period(incubation_period)

					# Updating nb of particles infected by i
					self.particles_list[i].nb_infections_provoked += 1

			# Propagating infection: particle i
			if ((self.particles_list[j].state==1 or self.particles_list[j].state==2) and
				self.particles_list[i].state==0 and self.particles_list[i].is_vaccinated==False):

				# Infection of particle j with a probability infection_contact_prob
				rand_num = random.uniform(0.0, 1.0)

				if rand_num < input_data.infection_contact_prob:

					# Set state to infected without symptoms
					self.particles_list[i].get_infected()
					self.particles_list[i].set_infection_time(time)
					# Set a random incubation period

					incubation_period = random.uniform(input_data.incubation_period[0], 
														input_data.incubation_period[1])

					self.particles_list[i].set_incubation_period(incubation_period)

					# Updating nb of particles infected by j
					self.particles_list[j].nb_infections_provoked += 1


	#---------------------------------
	# PEOPLE CHANGE OF HEALTH STATE
	#---------------------------------

	def change_person_state(self, time, input_data):

		# Loop on particles
		for part in self.particles_list:

			# Check if infected without symptoms will get symptoms
			if part.state==1:
				# Number of days between current time and infection time
				delta_time_infection = time - part.infection_time

				if delta_time_infection >= part.incubation_period:

					# Get symptoms
					part.get_symptoms()

					# Confine if measure is taken
					if input_data.symptomatics_confinement:
						self.confine_symptomatics()

					# Decide if the person will die or not and set death/recovery times
					rand_die = random.uniform(0.0, 1.0)
					if rand_die < input_data.mortality_rate:
						part.will_die = True
						# set duration after which person dies
						death_time = random.uniform(input_data.death_after_symptoms[0],
													input_data.death_after_symptoms[1])
						part.set_death_time(death_time)
					else:  # person recovers
						part.will_die = False
						# set duration after which person recovers
						recover_time = random.uniform(input_data.recovery_after_symptoms[0],
														input_data.recovery_after_symptoms[1])
						part.set_recovery_time(recover_time)

			# Person with symptoms
			elif part.state==2:

				# Number of days between current time and declaration of symptoms
				incubation_time = part.infection_time + part.incubation_period
				delta_time_symptoms = time - incubation_time

				# Check if person with symptoms recovers
				if part.will_die==False:
					if delta_time_symptoms >= part.recovery_time:
						# Recover
						part.recover()

						# If confinement measures were take for symptomatics;
						# we enable person to go out again
						# Warning: not allowed if preventively confined
						if input_data.symptomatics_confinement and part.is_prev_confined==False:
							part.set_initial_push(input_data)

				# Check if person with symptoms dies
				else:
					if delta_time_symptoms >= part.death_time:
						# Death
						part.die()
                        


	def remove_deads(self):

		# Loop and check particles with state 4 (death)
		for part in self.particles_list:
			if part.state==4:
				self.particles_list.remove(part)

		# Updating population size
		self.Nb_particles = len(self.particles_list)


	#---------------------------------
	# PREVENTION MEASURES
	#---------------------------------

	def confine_symptomatics(self):
		# Loop and check particles with state 2 (persons with symptoms)
		for part in self.particles_list:
			if part.state==2:
				part.freeze()


	def set_preventive_confinement(self, input_data):
		# Confine a proportion of the population
		# No need to shuffle as particles positions are already random
		nb_confined = int(input_data.preventive_confinement*input_data.population_size)
		for part in self.particles_list:
			if part.part_id<nb_confined:
				part.freeze()
				part.is_prev_confined = True


	def perform_vaccination_campaign(self, input_data):
		# Vaccine a proportion of the population
		# No need to shuffle as particles positions are already random
		nb_vaccined = int(input_data.vaccination_rate*input_data.population_size)
		for part in self.particles_list:
			if part.part_id<nb_vaccined:
				part.is_vaccinated = True

	#---------------------------------
	# POPULATION STATE
	#---------------------------------

	def check_if_infected(self):

		pop_infected = False

		for part in self.particles_list:
			if part.state==1 or part.state==2:
				pop_infected = True
				break

		return pop_infected

	#---------------------------------
	# R-FACTOR COMPUTATION
	#---------------------------------

	def compute_R_factor(self, time, input_data):
		""" Computation of effective reproduction factor R """

		# Initializing numerator and denominator
		total_nb_infected = 0
		total_nb_estimated_transmissions = 0

		# Loop on particles
		for part in self.particles_list:
			if part.state==1 or part.state==2:

				# Adding to total number of particles infected
				total_nb_infected += 1

				# Infection duration so far
				infected_since = time - part.infection_time
				# Number of persons infected so far
				nb_infected = part.nb_infections_provoked

				# Modeling the infection duration
				mean_duration_before_death = 0.5*(input_data.death_after_symptoms[1]+input_data.death_after_symptoms[0])
				mean_duration_before_recov = 0.5*(input_data.recovery_after_symptoms[1]+input_data.recovery_after_symptoms[0])
				mean_infection_duration = input_data.mortality_rate*mean_duration_before_death + (1.0-input_data.mortality_rate)*mean_duration_before_recov

				# Estimation of the number of infections during the total period
				if infected_since==0.0:
					nb_estimated_transmissions = 0.0
				else:
					nb_estimated_transmissions = (mean_infection_duration*nb_infected)/infected_since

				# Number of total estimated transmission for the period of infection
				total_nb_estimated_transmissions += nb_estimated_transmissions

		# R factor (by definition, if denom is zero, R is 0)
		if(total_nb_infected==0):
			self.R_factor = 0.0
		else:
			self.R_factor = total_nb_estimated_transmissions / total_nb_infected


		return self.R_factor


	#---------------------------------
	# SECONDARY ROUTINES
	#---------------------------------

	def get_position_matrix(self):
		""" Get matrix with particles position"""

		X = np.zeros((self.Nb_particles, 2))

		for i in range(self.Nb_particles):
			X[i,0] = self.particles_list[i].x
			X[i,1] = self.particles_list[i].y

		return X



	def export_state_to_file(self, time, nb_timestep, save_folder):
		""" Function to save state in h5 file """

		# Creating vectors with particles_data
		PartID_vect = np.zeros(self.Nb_particles)
		X_vect = np.zeros(self.Nb_particles)
		Y_vect = np.zeros(self.Nb_particles)
		VX_vect = np.zeros(self.Nb_particles)
		VY_vect = np.zeros(self.Nb_particles)
		PartState_vect = np.zeros(self.Nb_particles)
		#
		for i in range(self.Nb_particles):
			PartID_vect[i] = self.particles_list[i].part_id
			X_vect[i] = self.particles_list[i].x
			Y_vect[i] = self.particles_list[i].y
			VX_vect[i] = self.particles_list[i].vx
			VY_vect[i] = self.particles_list[i].vy
			PartState_vect[i] = self.particles_list[i].state

		# File to store data of current iteration
		file_data = save_folder + "/solutions/solution_step_{:04d}_{:3.2f}days.h5".format(nb_timestep, time)

		# Open h5 file to write inside
		hf = h5py.File(file_data, 'w')

		# Writing datasets in file
		hf.create_dataset('TIME', data=np.array((time)))
		hf.create_dataset('NB_TIMESTEP', data=np.array((nb_timestep)))
		hf.create_dataset('ID', data=PartID_vect)
		hf.create_dataset('X', data=X_vect)
		hf.create_dataset('Y', data=Y_vect)
		hf.create_dataset('VX', data=VX_vect)
		hf.create_dataset('VY', data=VY_vect)
		hf.create_dataset('STATE', data=PartState_vect)
		hf.create_dataset('R_FACTOR', data=np.array((self.R_factor)))

		# Close file
		hf.close()



