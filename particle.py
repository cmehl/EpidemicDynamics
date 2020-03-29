
import random
import numpy as np

import utils


class particle(object):

	#---------------------------------
	# INITIALIZATION
	#---------------------------------

	def __init__(self, part_id, state, input_data):

		# Particle id
		self.part_id = part_id

		# Radius
		self.radius = input_data.radius

		# Mass
		self.mass = input_data.mass

		# Initial position is random in [0,L_X]*[0,L_Y]
		if state==0:
			self.x = random.uniform(0, input_data.domain_size[0])
			self.y = random.uniform(0, input_data.domain_size[1])
		else:
			self.x = input_data.patient0_position[0]
			self.y = input_data.patient0_position[1]

		# Initial speed: random angle with given momentum
		self.set_initial_push(input_data)


		# Time of infection: set to None if healthy at the beginning, zero else
		if state==0:
			self.infection_time = None
		else:
			self.infection_time = 0.0
			self.incubation_period = 0.0 # First particle has already symptoms

		# Person is initially in good health
		# States:
		# 0 : healthy
		# 1 : infected without symptoms
		# 2 : infected with symptoms
		# 3 : recovered
		# 4 : dead (internal state, particles are removed right after)
		self.state = state

		# Preventive confinement on or not
		self.is_prev_confined = False

		# Number of infections provoked by the particle (initially 0)
		self.nb_infections_provoked = 0

		# Initially person is not vaccined againt disease
		self.is_vaccinated = False


	#---------------------------------
	# PARTICLE MOVEMENT
	#---------------------------------

	def set_initial_push(self, input_data):
		# Velocity imposed by chosing random angle and given norm
		vel_norm = input_data.initial_momentum / input_data.mass
		angle = random.uniform(0, 2.0*np.pi)
		self.vx, self.vy = utils.vel_components_from_angle(angle, vel_norm)
		self.V = np.array([self.vx, self.vy])


	#---------------------------------
	# PARTICLE CHANGE OF STATE
	#---------------------------------

	def move_particle(self, dt):
		""" Update particle position using its velocity"""
		self.x += self.vx * dt
		self.y += self.vy * dt


	def reflect_wall(self, direction):
		""" Update particle velocity due to wall reflection"""
		if direction == "x":
			self.vx = -self.vx
			
		elif direction == "y":
			self.vy = -self.vy

		# Update also velocity vector
		self.V = np.array([self.vx, self.vy])


	def get_infected(self):
		self.state = 1


	def get_symptoms(self):
		self.state = 2


	def recover(self):
		self.state = 3


	def die(self):
		self.state = 4


	def set_infection_time(self, time):
		self.infection_time = time


	def set_incubation_period(self, time, results_folder):
		# Setting incubation time
		self.incubation_period = time
		# We write incubation times in a file
		with open(results_folder + "/incubation_times.txt", "a") as f:
			f.write(f"{self.incubation_period}\n")


	def set_death_time(self, time):
		self.death_time = time


	def set_recovery_time(self, time):
		self.recovery_time = time


	def freeze(self):
		self.vx = 0.0
		self.vy = 0.0

		# Update also velocity vector
		self.V = np.array([self.vx, self.vy])


	










