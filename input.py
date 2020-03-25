

class input_data(object):

	def __init__(self):

		# General parameter for the simulation
		self.population_size = 1000
		self.saving_data_folder = "./temporal_states"
		self.saving_images_folder = "./images"

		# Domain properties
		self.L_X = 1.0     # km
		self.L_Y = 1.0     # km
		self.domain_size = (self.L_X, self.L_Y)

		# Time control
		self.dt = 0.1     # days

		# Particles characteristics
		self.radius = 0.002        # km
		self.mass = 1.0            # no unit (normalization)
		self.initial_momentum = 0.1       #  km/day-1 (no mass unit)

		# Disease characteristics
		self.infection_contact_prob = 1.0     # [0,1] (probability)
		self.mortality_rate = 0.5             # [0,1] (probability)
		self.death_after_symptoms = (1.0, 3.0)             # days
		self.incubation_period = (1.0, 4.0)         # days
		self.recovery_after_symptoms = (2.0, 4.0)   # days


		# Action against epidemic
		self.prenventive_confinement = 0.0         # Ratio of population initially confined       
		self.symptomatics_confinement = False



