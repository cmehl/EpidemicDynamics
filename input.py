import sys
import utils

import matplotlib.pyplot as plt


class input_data(object):
	""" Input parameters of the simulation"""

	def __init__(self, disease_type):

		# General parameter for the simulation
		self.population_size = 2000
		self.saving_folder = "./results"
		self.saving_frequency = 1.0  # days

		# Domain properties
		self.L_X = 1.0     # km
		self.L_Y = 1.0     # km
		self.domain_size = (self.L_X, self.L_Y)

		# Time control
		self.dt = 0.1     # days
		self.t_max = 200.0  # days

		# Particles characteristics
		self.radius = 0.002        # km
		self.mass = 1.0            # no unit (normalization)
		self.initial_momentum = 0.02      #  km/day-1 (no mass unit)

		# Disease characteristics
		self.initial_infected_positions = [(0.5, 0.5), (0.505, 0.5), (0.495, 0.5)]   # As many as we want
		self.infection_contact_prob = 0.6     # [0,1] (probability)
		# Remark: infection probability can be disease dependant but also habit dependant (hand washing, etc...)
		self.set_disease_data(disease_type)


		# Action against epidemic
		self.preventive_confinement = 0.5         # Ratio of population initially confined       
		self.symptomatics_confinement = False
		self.vaccination_rate = 0.0

	#---------------------------------
	# DISEASE DATA FROM LITERATURE
	#---------------------------------

	def set_disease_data(self, disease_data):

		# custom: user should set arbitrary data here
		if disease_data=="custom": 

			self.mortality_rate = 0.05            # [0,1] (probability)

			# Incubation time setting
			self.incubation_modeling = "Lognormal"
			params_incubation = (5.6, 2.8)
			self.compute_cdf(params_incubation, "incubation", self.incubation_modeling)

			# Death time setting (onset to death timing)
			self.onset_to_death_modeling = "Gamma"
			params_onset_to_death = (14.5, 6.7)
			self.compute_cdf(params_onset_to_death, "onset_to_death", self.onset_to_death_modeling)

			# Recovery time setting (onset to recovery timing)
			self.onset_to_recov_modeling = "Uniform"
			params_recovery = (12, 16)
			self.compute_cdf(params_recovery, "onset_to_recov", self.onset_to_recov_modeling)
		

		elif disease_data=="covid19":

			self.mortality_rate = 0.023            # [0,1] (probability)

			# Incubation time setting
			self.incubation_modeling = "Lognormal"
			params_incubation = (5.6, 2.8)
			self.compute_cdf(params_incubation, "incubation", self.incubation_modeling)

			# Death time setting (onset to death timing)
			self.onset_to_death_modeling = "Gamma"
			params_onset_to_death = (14.5, 6.7)
			self.compute_cdf(params_onset_to_death, "onset_to_death", self.onset_to_death_modeling)

			# Recovery time setting (onset to recovery timing)
			self.onset_to_recov_modeling = "Lognormal"
			params_recovery = (12, 2)
			self.compute_cdf(params_recovery, "onset_to_recov", self.onset_to_recov_modeling)

		elif disease_data=="SRAS":

			self.mortality_rate = 0.15           # [0,1] (probability)

			# Incubation time setting
			self.incubation_modeling = "Lognormal"
			params_incubation = (5.6, 2.8)
			self.compute_cdf(params_incubation, "incubation", self.incubation_modeling)

			# Death time setting (onset to death timing)
			self.onset_to_death_modeling = "Gamma"
			params_onset_to_death = (14.5, 6.7)
			self.compute_cdf(params_onset_to_death, "onset_to_death", self.onset_to_death_modeling)

			# Recovery time setting (onset to recovery timing)
			self.onset_to_recov_modeling = "Uniform"
			params_recovery = (12, 16)
			self.compute_cdf(params_recovery, "onset_to_recov", self.onset_to_recov_modeling)

		elif disease_data=="MERS":

			self.mortality_rate = 0.15           # [0,1] (probability)

			# Incubation time setting
			self.incubation_modeling = "Lognormal"
			params_incubation = (5.6, 2.8)
			self.compute_cdf(params_incubation, "incubation", self.incubation_modeling)

			# Death time setting (onset to death timing)
			self.onset_to_death_modeling = "Gamma"
			params_onset_to_death = (14.5, 6.7)
			self.compute_cdf(params_onset_to_death, "onset_to_death", self.onset_to_death_modeling)

			# Recovery time setting (onset to recovery timing)
			self.onset_to_recov_modeling = "Uniform"
			params_recovery = (12, 16)
			self.compute_cdf(params_recovery, "onset_to_recov", self.onset_to_recov_modeling)


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
			fi.write("Initial position of patients: \n")
			for i in range(len(self.initial_infected_positions)):
				fi.write(f"     >> Patient {i}: {self.initial_infected_positions[i]} km\n")
			fi.write(f"Probability of infection at contact: {100*self.infection_contact_prob} %\n")
			fi.write(f"Mortality rate: {100*self.mortality_rate} %\n")
			fi.write(f"Incubation probability law: {self.incubation_modeling} \n")
			fi.write(f"Onset to recovery probability law: {self.onset_to_death_modeling} \n")
			fi.write(f"Onset to death probability law: {self.onset_to_recov_modeling} \n\n")

			fi.write("[PREVENTION PARAMETERS]\n")
			fi.write(f"Preventive confinement: {self.preventive_confinement} % of people\n")
			fi.write(f"Confinement of symptomatic persons: {self.symptomatics_confinement}\n")
			fi.write(f"Proportion of the population vaccinated: {100.0*self.vaccination_rate} %\n")


	#---------------------------------
	# CDF's related functions
	#---------------------------------

	def compute_cdf(self, params, stage, proba_law):

		if proba_law=="Uniform":

			min_val, max_val = params[0], params[1]
			if stage== "incubation":
				self.mean_incubation = 0.5*(params[0] + params[1])
				self.incubation_proba = utils.compute_uniform_cdf(min_val, max_val, self.saving_folder)
			elif stage== "onset_to_death":
				self.mean_onset_to_death = 0.5*(params[0] + params[1])
				self.onset_to_death_proba = utils.compute_uniform_cdf(min_val, max_val, self.saving_folder)
			elif stage== "onset_to_recov":
				self.mean_onset_to_recov = 0.5*(params[0] + params[1])
				self.onset_to_recov_proba = utils.compute_uniform_cdf(min_val, max_val, self.saving_folder)

		elif proba_law=="Lognormal":

			mean_val, std_val = params[0], params[1]
			if stage== "incubation":
				self.mean_incubation = params[0]
				self.incubation_proba = utils.compute_lognormal_cdf(mean_val, std_val, self.saving_folder)
			elif stage== "onset_to_death":
				self.mean_onset_to_death = params[0]
				self.onset_to_death_proba = utils.compute_lognormal_cdf(mean_val, std_val, self.saving_folder)
			elif stage== "onset_to_recov":
				self.mean_onset_to_recov = params[0]
				self.onset_to_recov_proba = utils.compute_lognormal_cdf(mean_val, std_val, self.saving_folder)

		elif proba_law=="Gamma":

			mean_val, std_val = params[0], params[1]
			if stage== "incubation":
				self.mean_incubation = params[0]
				self.incubation_proba = utils.compute_gamma_cdf(mean_val, std_val, self.saving_folder)
			elif stage== "onset_to_death":
				self.mean_onset_to_death = params[0]
				self.onset_to_death_proba = utils.compute_gamma_cdf(mean_val, std_val, self.saving_folder)
			elif stage== "onset_to_recov":
				self.mean_onset_to_recov = params[0]
				self.onset_to_recov_proba = utils.compute_gamma_cdf(mean_val, std_val, self.saving_folder)




	def plot_cdf(self):

		# INCUBATION
		# Unpacking incubation cdf
		x_incubation = self.incubation_proba[:,0]
		pdf_incubation = self.incubation_proba[:,2]

		# ONSET TO DEATH
		# Unpacking onset to death cdf
		x_onset_to_death = self.onset_to_death_proba[:,0]
		pdf_onset_to_death = self.onset_to_death_proba[:,2]

		# ONSET TO DEATH
		# Unpacking onset to death cdf
		x_onset_to_recov = self.onset_to_recov_proba[:,0]
		pdf_onset_to_recov = self.onset_to_recov_proba[:,2]

		# Plot pdf to sanity check
		fig, ax = plt.subplots()
		ax.plot(x_incubation, pdf_incubation, color="k", lw=2, label="Incubation")
		ax.plot(x_onset_to_death, pdf_onset_to_death, color="g", lw=2, label="Onset to death")
		ax.plot(x_onset_to_recov, pdf_onset_to_recov, color="b", lw=2, label="Onset to recovery")
		ax.set_xlabel("days")
		ax.set_ylabel("pdf")
		ax.legend(fontsize=8)
		ax.grid(ls="--", alpha=0.5)
		ax.set_title(f"{self.incubation_modeling} law")
		fig.savefig(self.saving_folder + "/durations_pdf.png", dpi=250)














