import sys
import utils

class input_data(object):
	""" Input parameters of the simulation"""

	def __init__(self, disease_type):

		# General parameter for the simulation
		self.population_size = 2000
		self.saving_folder = "./results"
		self.saving_frequency = 0.5  # days

		# Domain properties
		self.L_X = 1.0     # km
		self.L_Y = 1.0     # km
		self.domain_size = (self.L_X, self.L_Y)

		# Time control
		self.dt = 0.1     # days

		# Particles characteristics
		self.radius = 0.002        # km
		self.mass = 1.0            # no unit (normalization)
		self.initial_momentum = 0.02      #  km/day-1 (no mass unit)

		# Disease characteristics
		self.patient0_position = (0.5, 0.5)
		self.infection_contact_prob = 1.0     # [0,1] (probability)
		# Remark: infection probability can be disease dependant but also habit dependant (hand washing, etc...)
		self.set_disease_data(disease_type)


		# Action against epidemic
		self.preventive_confinement = 0.0         # Ratio of population initially confined       
		self.symptomatics_confinement = False
		self.vaccination_rate = 0.0

	#---------------------------------
	# DISEASE DATA FROM LITERATURE
	#---------------------------------

	def set_disease_data(self, disease_data):

		# custom: user should set arbitrary data here
		if disease_data=="custom": 

			self.mortality_rate = 0.05            # [0,1] (probability)
			self.death_after_symptoms = (1.0, 3.0)             # days
			self.incubation_period = (2.0, 1.0)         # [min, max, mean, std] days
			self.recovery_after_symptoms = (3.0, 5.0)   # days

		elif disease_data=="covid19":

			self.mortality_rate = 0.023            # [0,1] (probability)
			self.death_after_symptoms = (2.0, 4.0)       # days
			self.incubation_period = (4.0, 2.0)    # [min, max, mean, std] days
			self.recovery_after_symptoms = (5.0, 8.0)   # days

		elif disease_data=="SRAS":

			self.mortality_rate = 0.15           # [0,1] (probability)
			self.death_after_symptoms = (2.0, 4.0)       # days
			self.incubation_period = (4.0, 2.0)    # [min, max, mean, std] days
			self.recovery_after_symptoms = (5.0, 8.0)   # days


		# For incubation period, we set a CDF (truncated gaussian pdf)
		# min_val = self.incubation_period[0]
		# max_val = self.incubation_period[1]
		mean_val = self.incubation_period[0]
		std_val = self.incubation_period[1]
		self.incubation_CDF = utils.gamma_cdf(mean_val, std_val, self.saving_folder)


	#---------------------------------
	# CHECKING AND EXPORT OF INPUTS
	#---------------------------------

	def check_inputs(self):

		if(self.preventive_confinement <0.0 or self.preventive_confinement>1.0):
			sys.exit("Variable preventine_confinement should be in [0, 1]")

		if(self.vaccination_rate <0.0 or self.vaccination_rate>1.0):
			sys.exit("Variable vaccination_rate should be in [0, 1]")

		if(self.mortality_rate <0.0 or self.mortality_rate>1.0):
			sys.exit("Variable mortality_rate should be in [0, 1]")

		if(self.infection_contact_prob <0.0 or self.infection_contact_prob>1.0):
			sys.exit("Variable infection_contact_prob should be in [0, 1]")

		if(self.preventive_confinement > 0.0 and self.vaccination_rate>0.0):
			sys.exit("There is no need to confine if a vaccine is available")


	def export_input(self):

		file_input = self.saving_folder + "/input_params.txt"

		# Writing input parameters to a file
		with open(file_input, "w") as fi:

			fi.write("[POPULATION PARAMETERS]\n")
			fi.write(f"Population size: {self.population_size}\n")
			fi.write(f"Domain: {self.domain_size} km \n")
			fi.write(f"Infection radius: {1000.0*self.radius} m\n\n")

			fi.write("[EPIDEMIC PARAMETERS]\n")
			fi.write(f"Initial position of patient 0: {self.patient0_position} km \n")
			fi.write(f"Probability of infection at contact: {100*self.infection_contact_prob} %\n")
			fi.write(f"Mortality rate: {100*self.mortality_rate} %\n")
			fi.write(f"Incubation period: {self.incubation_period} days\n")
			fi.write(f"Recovery duration after symptoms: {self.recovery_after_symptoms} days\n")
			fi.write(f"Death after symptoms: {self.death_after_symptoms} days\n\n")

			fi.write("[PREVENTION PARAMETERS]\n")
			fi.write(f"Preventive confinement: {self.preventive_confinement} % of people\n")
			fi.write(f"Confinement of symptomatic persons: {self.symptomatics_confinement}\n")
			fi.write(f"Proportion of the population vaccinated: {100.0*self.vaccination_rate} %\n")





