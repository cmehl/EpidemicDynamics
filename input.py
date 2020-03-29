

class input_data(object):
	""" Input parameters of the simulation"""

	def __init__(self):

		# General parameter for the simulation
		self.population_size = 1500
		self.saving_folder = "./results"

		# Domain properties
		self.L_X = 1.0     # km
		self.L_Y = 1.0     # km
		self.domain_size = (self.L_X, self.L_Y)

		# Time control
		self.dt = 0.2     # days

		# Particles characteristics
		self.radius = 0.004        # km
		self.mass = 1.0            # no unit (normalization)
		self.initial_momentum = 0.05      #  km/day-1 (no mass unit)

		# Disease characteristics
		self.infection_contact_prob = 1.0     # [0,1] (probability)
		self.mortality_rate = 0.05            # [0,1] (probability)
		self.death_after_symptoms = (1.0, 3.0)             # days
		self.incubation_period = (1.0, 4.0)         # days
		self.recovery_after_symptoms = (3.0, 5.0)   # days


		# Action against epidemic
		self.preventive_confinement = 0.0         # Ratio of population initially confined       
		self.symptomatics_confinement = False


	def export_input(self):

		file_input = self.saving_folder + "/input_params.txt"

		# Writing input parameters to a file
		with open(file_input, "w") as fi:

			fi.write("[POPULATION PARAMETERS]\n")
			fi.write(f"Population size: {self.population_size}\n")
			fi.write(f"Domain: {self.domain_size} km \n")
			fi.write(f"Infection radius: {1000.0*self.radius} m\n\n")

			fi.write("[EPIDEMIC PARAMETERS]\n")
			fi.write(f"Probability of infection at contact: {100*self.infection_contact_prob} %\n")
			fi.write(f"Mortality rate: {100*self.mortality_rate} %\n")
			fi.write(f"Incubation period: {self.incubation_period} days\n")
			fi.write(f"Recovery duration after symptoms: {self.recovery_after_symptoms} days\n")
			fi.write(f"Death after symptoms: {self.death_after_symptoms} days\n\n")

			fi.write("[PREVENTION PARAMETERS]\n")
			fi.write(f"Preventive confinement: {self.preventive_confinement} % of people\n")
			fi.write(f"Confinement of symptomatic persons: {self.symptomatics_confinement}\n")





