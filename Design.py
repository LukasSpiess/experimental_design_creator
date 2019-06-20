"""""
TO-DO

1.) Need to implement control measures to make sure that user does not enter control vars and factors and FactStructs intermixed as input
2. ) Need to think about what to do in case a control variable is entered and it is a between-block variable  <---- this is very important though

"""""

import FactorStruct as FactorStruct
import NewControl as NewControl
import NewFactor as NewFactor
from Functions import *


class Design:
	def __init__(self, factors):
		self.factors = factors

		self.factor_type = []

		btw_indices = None
		wtn_indices = None

		self.n_cells = None
		self.n_cells_within = None
		self.n_cells_between = None
		self.probability_type = None
		self.prob_mat = None
		self.factors_ordered = None

		## Preparation and checking of input type
		if not isinstance(self.factors, list) and not isinstance(self.factors,
		                                                         FactorStruct.FactorStruct):  # put a single input factor in list format to allow for iteration later on
			self.factors = [self.factors]

		if isinstance(self.factors, FactorStruct.FactorStruct):  # if factor structure
			import copy
			self.input_type = "FactStruct"
			self.probability_type = self.factors.probability_type
			self.prob_mat = copy.copy(self.factors.probabilityMatrix)
			self.factors = copy.copy(
				self.factors.factors)  # re-assign such that it becomes regular factor, make sure the list thing works, when FS is only one factor
			#self.prob_mat = copy.copy(self.factors.probabilityMatrix)


		elif isinstance(self.factors[0], NewControl.NewControl):
			self.input_type = "Control"


		elif isinstance(self.factors[0], NewFactor.NewFactor):
			self.input_type = "Factor"

		else:
			print('Cannot determine Input type')

		#############################################
		##### Determine design of input factors #####
		#############################################




		# The code below is carried out anyway (even if factorStruct is provided; this is because we put the factors from the factStruct in self.factors)
		# Code also calculates n_cells
		if len(self.factors) == 1:  # if only a single factor is given (regardless of whether in factstruct or not)
			self.factor_type = self.factors[0].f_type
			if 'Between-subject' in self.factor_type:  # if the factor is between-subject
				self.design = "Between-subject"
				self.n_between_factors = 1
				self.n_cells = self.factors[0].n_levels
				self.n_cells_between = self.n_cells
			else:
				self.design = "Within-subject"
				self.n_within_factors = 1
				self.n_cells = self.factors[0].n_levels
				self.n_cells_within = self.n_cells

		elif len(self.factors) > 1:  # If multiple factors were given
			[self.factor_type.append(x.f_type) for x in
			 self.factors]  # <<<<<<<<------------ Check whether and which factors are between and within
			self.between = False
			self.within = False
			self.n_between_factors = 0  # counter for number of btw-factors
			btw_indices = []  # list that contains index for between subject factors
			self.n_within_factors = 0
			wtn_indices = []
			for index, i_type in enumerate(self.factor_type):
				if "Between" in i_type:
					self.between = True
					self.n_between_factors += 1
					btw_indices.append(index)
				else:
					self.within = True
					self.n_within_factors += 1
					wtn_indices.append(index)
			if self.between == True and self.within == True:
				self.design = "Mixed"
				self.factors_ordered = []  # herein, we save an ordered list of factors, in which the btw-factors come first
				self.n_cells_between = 1
				for i in range(0, len(btw_indices)):  # calculate number of cells
					self.n_cells_between *= self.factors[
						btw_indices[i]].n_levels  # how many cells the between-subject factors have
					self.factors_ordered.append(self.factors[btw_indices[i]])
				self.n_cells_within = 1
				for i in range(0, len(wtn_indices)):
					self.n_cells_within *= self.factors[wtn_indices[i]].n_levels
					self.factors_ordered.append(self.factors[wtn_indices[i]])
				self.n_cells = self.n_cells_between * self.n_cells_within  # total number of cells


			elif (self.between == True) and (self.within == False):
				self.design = "Between-subject"
				self.n_cells = prod([F.n_levels for F in self.factors])
				self.n_cells_between = self.n_cells
			elif self.between == False and self.within == True:
				self.design = "Within-subject"
				self.n_cells = prod([F.n_levels for F in self.factors])
				self.n_cells_within = self.n_cells  # just for compatibility
			else:
				print('Cannot automatically define design.')
			# if self.input_type == "FactStruct" and (self.design == "Between-subject" or self.design == "Mixed"):
			# self.trials = int(self.trials / self.n_cells_between)  # adjust mnumber of trials
		# else:
		#     print('Check Input Type -- you get here if a FactStruct was given as input')
		print('')
		print('------------------------------------------')
		if self.input_type == 'Factor' or self.input_type == "FactStruct":
			print('{} factorial design detected'.format(self.design))
		elif self.input_type == 'Control':
			print("{} control design detected".format(self.design))
		print('------------------------------------------')
		print('')
