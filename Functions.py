##############################################################
##############################################################
##############################################################
##############################################################
################# Some Helper functions ######################
##############################################################
##############################################################
##############################################################
##############################################################

def prod(integers):
	p = 1
	for i in integers:
		p *= i
	return p


##############################################################
##############################################################
##############################################################
# This function creates a multidimensional list
def multi_dim_list(number_rows, number_columns):
	return [[0] * number_rows for i in range(number_columns)]



##############################################################
##############################################################
##############################################################
# This function decomposes a string like xxx_yyy_zzz into xxx yyy zzz as separate lists
# Make sure that all the elements in input array can have same number of splits
# So far only accepts 1D arrays
def decompose(Block_class, split_str = '_'):

	#flatten the trial_list array before continuing, then you do not need the long try-except chain below
	#	and evrything becies easier; use itertools for that

	print('Implement to choose how to decompose!')
	case = None
	dims = []
	try:
		dims.append(len(Block_class.trial_list))
		n_split = len(Block_class.trial_list.split(split_str))
		string_element = Block_class.trial_list.split(split_str)

		case = 0
	except:
		try:
			dims.append(len(Block_class.trial_list[0]))
			n_split = len(Block_class.trial_list[0].split(split_str))
			string_element = Block_class.trial_list.split(split_str)
			case = 1
		except:
			try:
				dims.append(len(Block_class.trial_list[0][0]))
				n_split = len(Block_class.trial_list[0][0].split(split_str))
				string_element = Block_class.trial_list.split(split_str)
				case = 2
			except:
				try:
					dims.append(len(Block_class.trial_list[0][0][0]))
					n_split = len(Block_class.trial_list[0][0][0].split(split_str))
					string_element = Block_class.trial_list.split(split_str)
					case = 3
				except:
					try:
						dims.append(len(Block_class.trial_list[0][0][0][0]))
						n_split = len(Block_class.trial_list[0][0][0][0].split(split_str))
						string_element = Block_class.trial_list.split(split_str)
						case = 4
					except:
						print('Not implemented yet')

	dims = dims[:case] # to get the proper dimensions
	n_trials = prod(dims)
	decomposition = multi_dim_list(n_trials,n_split)


	for iCol, iString_element in enumerate(string_element): ## loop through columns
		for iTrial in range(n_trials): ## loop through trials
			tmp_str = Block_class.trial_list
			decomposition[iTrial][iCol] =2




##############################################################
##############################################################
##############################################################
# This function creates all uniquely possible factorial combinations
def factorial_combinations(n_factors, factor_levels, n_cells):
	# initialize some variables
	fact_comb = multi_dim_list(n_cells, n_factors)  # create empty list
	# factor_levels = [[1,2],[1,2,3],[1,2],[1,2,3,4]]
	index_counter = 1
	for factor_index in range(0, len(factor_levels)):  # loop through factors
		index_counter *= len(factor_levels[factor_index])  # update this special counter
		start = 0
		stop = n_cells / index_counter
		for i_rep in range(0, int(index_counter / len(
				factor_levels[factor_index]))):  # loop through repetition of a factor level sequence
			if i_rep == 0:
				start = 0
				stop = n_cells / index_counter
			for i_level in factor_levels[factor_index]:  # loop through factor levels
				for i in range(int(start), int(stop)):  # loop through each (empty) element in the list to fill it
					# print('column = {} .. row = {}.... i_level = {}.. start = {} .. stop = {}'.format(,factor_index,i,i_level, start, stop))
					fact_comb[factor_index][i] = i_level
				start += n_cells / index_counter
				stop += n_cells / index_counter
	return fact_comb


##############################################################
##############################################################
##############################################################
# This function takes as input a factorial combination matrix and asks for user input on how to set probabilities for uneven factor crossing (w.r.t. trial structure)
def ask_probs(n_factors, n_cells, factorial_combination_matrix, case):
	from collections import OrderedDict
	prob_mat = OrderedDict()  # crete empty dictionary and use it as data structure
	for i_cell in range(0, n_cells):  # loop through rows
		k = ''
		for i_fac in range(0, n_factors):  # loop through factors
			k += factorial_combination_matrix[i_fac][i_cell]
			if i_fac >= 0 and i_fac is not n_factors - 1:
				k += '_'
			if i_fac == n_factors - 1:
				if case == 1:  # When asking for probabilities / percentages
					prob_mat[k] = input('probability (0-1) for: {}   :  '.format(
						k))  # k here writes the name of the factor combinations
				else:
					prob_mat[k] = input('number of trials for: {}   :  '.format(k))
	return prob_mat


##############################################################
##############################################################
##############################################################
# This function takes as input a factorial combination matrix and returns a list with the crossed factors and their associated names
def giveName(n_factors, n_cells, factorial_combination_matrix):
	fact_comb_names = []

	for i_cell in range(0, n_cells):  # loop through rows
		k = ''
		for i_fac in range(0, n_factors):  # loop through factors
			k += factorial_combination_matrix[i_fac][i_cell]
			if i_fac >= 0 and i_fac is not n_factors - 1:
				k += '_'
			if i_fac == n_factors - 1:
				fact_comb_names.append(k)  # k here writes the name of the factor combinations
	return fact_comb_names


##############################################################
##############################################################
##############################################################
# This function makes trials
def MakeTrials(factors, input_type, trials, factorial_design, probability_type=None, prob_mat=None,
               factors_ordered=None, n_cells=None, n_cells_within=None, n_cells_between=None, n_cells_control=None,
               n_cells_control_between=None, n_cells_control_within=None, control_design=None, control_variables=None
               ):
	"""""
	print('')
	print('')
	print('factors      {}'.format(factors))
	print('input_type       {}'.format(input_type))
	print('trials       {}'.format(trials))
	print('Factorial design         {}'.format(factorial_design))
	print('probability type         {}'.format(probability_type))
	print('Prob_mat     {}'.format(prob_mat))
	print('factors_ordered      {}'.format(factors_ordered))
	print('n_cells      {}'.format(n_cells))
	print('n_cells_within       {}'.format(n_cells_within))
	print('n_cells_between      {}'.format(n_cells_between))
	print('n_cells_control      {}'.format(n_cells_control))
	print('n_cells_control_between      {}'.format(n_cells_control_between))
	print('n_cells_control_within       {}'.format(n_cells_control_within))
	print('control_design       {}'.format(control_design))
	print('control_vars     {}'.format(control_variables))
	print('')
	print('')
	print(type(trials))
	"""""

	# Preparation
	if control_variables == [None] or control_variables == None:
		control = False
	else:
		control = True
	##########################
	####### Main Body ########
	trial_list = []

	if input_type == 'Factor':
		if len(factors) == 1:
			if not control:
				unique_trials = []
				[unique_trials.append(x) for x in factors[0].level_names]  # get all unique factor (-combinations)
				trial_list = []
				if factorial_design == 'Between-subject':
					trial_list = multi_dim_list(trials, n_cells)
					for iFactor in range(0, n_cells):
						for iTrial in range(0, trials):
							trial_list[iFactor][iTrial] = unique_trials[iFactor]  # make the list
				elif factorial_design == 'Within-subject':
					n_reps = trials / n_cells
					for iRep in range(0, int(n_reps)):
						[trial_list.append(x) for x in unique_trials]
				else:
					print('Length 1 factor not correctly identified')
			############
			# If control variables are present
			elif control:
				if factorial_design == "Between-subject" and control_design == "Between-subject":
					try:
						factors_ordered = []
						for i_contr in control_variables:  # loop 'cos the're multiple control_vars
							factors_ordered.append(i_contr)
						factors_ordered.append(factors[0])  # don't loop 'cos there's just one factor
					except:
						factors_ordered = [control_variables[0], factors[0]]
					n_cells_total = n_cells_control * n_cells
					balanced_fact_Struct = factorial_combinations(len(factors_ordered),
					                                              [F.level_names for F in factors_ordered],
					                                              n_cells_total)  # create balanced factor Structure
					unique_trials = giveName(len(factors_ordered), n_cells_total, balanced_fact_Struct)
					trial_list = multi_dim_list(trials, n_cells_total)
					for iFactor in range(0, n_cells_total):  # loop through factor levels
						for iTrial in range(0, trials):  # loop through trials
							trial_list[iFactor][iTrial] = unique_trials[iFactor]  # make up the trial list


				elif factorial_design == "Between-subject" and control_design == "Within-subject":
					try:
						factors_ordered = [factors[0]]
						for i_contr in control_variables:
							factors_ordered.append(i_contr)
					except:
						factors_ordered = [factors[0], control_variables[0]]
					n_cells_total = n_cells_control_within * n_cells
					balanced_fact_Struct = factorial_combinations(len(factors_ordered),
					                                              [F.level_names for F in factors_ordered],
					                                              n_cells_total)  # create balanced factor Structure
					unique_trials = giveName(len(factors_ordered), n_cells_total, balanced_fact_Struct)
					trial_list = multi_dim_list(n_cells_control_within, n_cells)
					n_reps = trials / n_cells_control_within
					counter = 0
					for i_cell_between in range(0, n_cells):  # looop through btw-factor levels
						for i_cell_within in range(0, n_cells_control_within):  # loop through wtn-factor levels
							trial_list[i_cell_between][i_cell_within] = unique_trials[counter]
							counter += 1
						trial_list[i_cell_between] = int(n_reps) * trial_list[i_cell_between]

				elif factorial_design == "Between-subject" and control_design == "Mixed":
					# print('Have not done this yet')
					within_control_index = []
					between_control_index = []
					for index, item in enumerate(
							control_variables):  # figure out which of the control_vars is within/between
						if item.f_type == "Within-subject":
							within_control_index.append(index)
						elif item.f_type == 'Between-subject':
							between_control_index.append(index)
					# Bring everything in the right order
					factors_ordered = []
					for index in between_control_index:
						factors_ordered.append(control_variables[index])
					for iFac in factors:
						factors_ordered.append(iFac)
					for index in within_control_index:
						factors_ordered.append(control_variables[index])

					n_cells_total = n_cells * n_cells_control
					n_cells_between = n_cells * n_cells_control_between

					balanced_fact_Struct = factorial_combinations(len(factors_ordered),
					                                              [F.level_names for F in factors_ordered],
					                                              n_cells_total)  # create balanced factor Structure
					unique_trials = giveName(len(factors_ordered), n_cells_total, balanced_fact_Struct)
					trial_list = multi_dim_list(n_cells_control_within, n_cells_between)

					n_reps = trials / n_cells_control_within
					counter = 0
					for i_cell_between in range(0, n_cells_between):  # looop through btw-factor levels
						for i_cell_within in range(0, n_cells_control_within):  # loop through wtn-factor levels
							trial_list[i_cell_between][i_cell_within] = unique_trials[counter]
							counter += 1
						trial_list[i_cell_between] = int(n_reps) * trial_list[i_cell_between]


				elif factorial_design == "Within-subject" and control_design == "Between-subject":
					try:
						factors_ordered = []
						for i_contr in control_variables:
							factors_ordered.append(i_contr)
						factors_ordered.append(factors[0])
					except:
						factors_ordered = [control_variables[0], factors[0]]
					n_cells_total = n_cells_control_between * n_cells
					balanced_fact_Struct = factorial_combinations(len(factors_ordered),
					                                              [F.level_names for F in factors_ordered],
					                                              n_cells_total)  # create balanced factor Structure
					unique_trials = giveName(len(factors_ordered), n_cells_total, balanced_fact_Struct)
					trial_list = multi_dim_list(n_cells, n_cells_control_between)
					n_reps = trials / n_cells
					counter = 0
					for i_cell_between in range(0, n_cells_control_between):  # looop through btw-factor levels
						for i_cell_within in range(0, n_cells):  # loop through wtn-factor levels
							trial_list[i_cell_between][i_cell_within] = unique_trials[counter]
							counter += 1
						trial_list[i_cell_between] = int(n_reps) * trial_list[i_cell_between]


				elif factorial_design == "Within-subject" and control_design == "Within-subject":
					try:
						factors_ordered = []
						factors_ordered.append(factors[0])
						for i_contr in control_variables:
							factors_ordered.append(i_contr)
					except:
						factors_ordered = [factors[0], control_variables[0]]
					n_cells_total = n_cells * n_cells_control_within
					balanced_fact_Struct = factorial_combinations(len(factors_ordered),
					                                              [F.level_names for F in factors_ordered],
					                                              n_cells_total)  # create balanced factor Structure
					unique_trials = giveName(len(factors_ordered), n_cells_total, balanced_fact_Struct)
					trial_list = []
					n_reps = trials / n_cells_total
					for iRep in range(0, int(n_reps)):
						[trial_list.append(x) for x in unique_trials]

				elif factorial_design == "Within-subject" and control_design == "Mixed":
					#print('Have not done this yet')
					within_control_index = []
					between_control_index = []
					for index, item in enumerate(
							control_variables):  # figure out which of the control_vars is within/between
						if item.f_type == "Within-subject":
							within_control_index.append(index)
						elif item.f_type == 'Between-subject':
							between_control_index.append(index)
					# Bring everything in the right order
					factors_ordered = []
					for index in between_control_index:
						factors_ordered.append(control_variables[index])
					for iFac in factors:
						factors_ordered.append(iFac)
					for index in within_control_index:
						factors_ordered.append(control_variables[index])

					n_cells_total = n_cells * n_cells_control_within * n_cells_control_between
					n_cells_within_total = n_cells * n_cells_control_within

					balanced_fact_Struct = factorial_combinations(len(factors_ordered),
					                                              [F.level_names for F in factors_ordered],
					                                              n_cells_total)  # create balanced factor Structure
					unique_trials = giveName(len(factors_ordered), n_cells_total, balanced_fact_Struct)
					trial_list = multi_dim_list(n_cells_within_total, n_cells_control_between)

					n_reps = trials / n_cells_within_total
					counter = 0
					for i_cell_between in range(0, n_cells_control_between):  # looop through btw-factor levels
						for i_cell_within in range(0, n_cells_within_total):  # loop through wtn-factor levels
							trial_list[i_cell_between][i_cell_within] = unique_trials[counter]
							counter += 1
						trial_list[i_cell_between] = int(n_reps) * trial_list[i_cell_between]


		##################################
		# If multiple factors were entered
		elif len(factors) > 1:
			if not control:
				if factorial_design == 'Mixed':
					trial_list = multi_dim_list(n_cells_within, n_cells_between)
					balanced_fact_Struct = factorial_combinations(len(factors_ordered),
					                                              [F.level_names for F in factors_ordered], n_cells)
					unique_trials = giveName(len(factors_ordered), n_cells, balanced_fact_Struct)
					n_reps = trials / n_cells_within
					counter = 0
					for i_cell_between in range(0, n_cells_between):  # looop through btw-factor levels
						for i_cell_within in range(0, n_cells_within):  # loop through wtn-factor levels
							trial_list[i_cell_between][i_cell_within] = unique_trials[counter]
							counter += 1
						trial_list[i_cell_between] = int(n_reps) * trial_list[i_cell_between]
				elif factorial_design == 'Between-subject':
					balanced_fact_Struct = factorial_combinations(len(factors), [F.level_names for F in factors],
					                                              n_cells)  # create balanced factor Structure
					unique_trials = giveName(len(factors), n_cells, balanced_fact_Struct)
					trial_list = multi_dim_list(trials, n_cells)  # create multidimensional trial list
					for i_cell in range(0, n_cells):  # loop through cells
						for i_trial in range(0,
						                     trials):  # looop through trials in here (it's more intuitive then making copies
							trial_list[i_cell][i_trial] = unique_trials[i_cell]
				elif factorial_design == "Within-subject":
					balanced_fact_Struct = factorial_combinations(len(factors), [F.level_names for F in factors],
					                                              n_cells)  # create balanced factor Structure
					unique_trials = giveName(len(factors), n_cells, balanced_fact_Struct)
					n_reps = trials / n_cells
					if trials == 1:  # in case the trial multiplier is one, a block will only be made by unique trials
						trial_list = unique_trials  # herein, the, in this case unique, trials will be stored
					elif trials > 1:
						for iRep in range(0, int(n_reps)):
							[trial_list.append(x) for x in unique_trials]  # append the trials unshuffled to a list
			#################################
			# If controlVariables
			if control:
				# print('Need to work on that')
				if factorial_design == 'Mixed' and control_design == "Within-subject":
					factors_ordered = factors_ordered + control_variables  # attach within-subject control variable at end because factors_ordered in mixed design is already sorted
					n_cells_within_total = n_cells_within * n_cells_control_within
					n_cells_total = n_cells_between * n_cells_within_total

					trial_list = multi_dim_list(n_cells_within_total, n_cells_between)
					balanced_fact_Struct = factorial_combinations(len(factors_ordered),
					                                              [F.level_names for F in factors_ordered],
					                                              n_cells_total)
					unique_trials = giveName(len(factors_ordered), n_cells_total, balanced_fact_Struct)
					n_reps = trials / n_cells_within_total
					counter = 0
					for i_cell_between in range(0, n_cells_between):  # looop through btw-factor levels
						for i_cell_within in range(0, n_cells_within_total):  # loop through wtn-factor levels
							trial_list[i_cell_between][i_cell_within] = unique_trials[counter]
							counter += 1
						trial_list[i_cell_between] = int(n_reps) * trial_list[i_cell_between]


				elif factorial_design == 'Mixed' and control_design == "Between-subject":
					factors_ordered = control_variables + factors_ordered  # attach within-subject control variable at end because factors_ordered in mixed design is already sorted
					# n_cells_within = n_cells_within * n_cells_control_between
					n_cells_between_total = n_cells_between * n_cells_control_between
					n_cells_total = n_cells_between * n_cells_within * n_cells_control_between

					trial_list = multi_dim_list(n_cells_within, n_cells_between_total)
					balanced_fact_Struct = factorial_combinations(len(factors_ordered),
					                                              [F.level_names for F in factors_ordered],
					                                              n_cells_total)
					unique_trials = giveName(len(factors_ordered), n_cells_total, balanced_fact_Struct)
					n_reps = trials / n_cells_within
					counter = 0
					for i_cell_between in range(0, n_cells_between_total):  # looop through btw-factor levels
						for i_cell_within in range(0, n_cells_within):  # loop through wtn-factor levels
							trial_list[i_cell_between][i_cell_within] = unique_trials[counter]
							counter += 1
						trial_list[i_cell_between] = int(n_reps) * trial_list[i_cell_between]


				elif factorial_design == "Mixed" and control_design == "Mixed":
					# Create good order of factors and control variables
					within_control_index = []
					between_control_index = []
					for index, item in enumerate(
							control_variables):  # figure out which of the control_vars is within/between
						if item.f_type == "Within-subject":
							within_control_index.append(index)
						elif item.f_type == 'Between-subject':
							between_control_index.append(index)

					for i_c in within_control_index:
						factors_ordered.append(control_variables[i_c])
					for i_c in between_control_index:
						factors_ordered = [control_variables[i_c]] + factors_ordered

					n_cells_total = n_cells_control_between * n_cells_control_within * n_cells_within * n_cells_between
					n_cells_within_total = n_cells_control_within * n_cells_within
					n_cells_between_total = n_cells_control_between * n_cells_between

					trial_list = multi_dim_list(n_cells_within_total, n_cells_between_total)
					balanced_fact_Struct = factorial_combinations(len(factors_ordered),
					                                              [F.level_names for F in factors_ordered],
					                                              n_cells_total)
					unique_trials = giveName(len(factors_ordered), n_cells_total, balanced_fact_Struct)

					n_reps = trials / n_cells_within_total
					counter = 0
					for i_cell_between in range(0, n_cells_between_total):  # looop through btw-factor levels
						for i_cell_within in range(0, n_cells_within_total):  # loop through wtn-factor levels
							trial_list[i_cell_between][i_cell_within] = unique_trials[counter]
							counter += 1
						trial_list[i_cell_between] = int(n_reps) * trial_list[i_cell_between]


				elif factorial_design == 'Between-subject' and control_design == "Between-subject":
					factors_ordered = control_variables + factors
					#print(n_cells)
					#print(n_cells_control_between)
					n_cells_total = n_cells_control_between * n_cells
					balanced_fact_Struct = factorial_combinations(len(factors_ordered),
					                                              [F.level_names for F in factors_ordered],
					                                              n_cells_total)  # create balanced factor Structure
					unique_trials = giveName(len(factors_ordered), n_cells_total, balanced_fact_Struct)
					trial_list = multi_dim_list(trials, n_cells_total)
					for iFactor in range(0, n_cells_total):  # loop through factor levels
						for iTrial in range(0, trials):  # loop through trials
							trial_list[iFactor][iTrial] = unique_trials[iFactor]  # make up the trial list


				elif factorial_design == 'Between-subject' and control_design == "Within-subject":
					factors_ordered = factors
					for i_contr in control_variables:  # loop 'cos the're multiple control_vars
						factors_ordered.append(i_contr)
					n_cells_total = n_cells_control_within * n_cells
					balanced_fact_Struct = factorial_combinations(len(factors_ordered),
					                                              [F.level_names for F in factors_ordered],
					                                              n_cells_total)  # create balanced factor Structure
					unique_trials = giveName(len(factors_ordered), n_cells_total, balanced_fact_Struct)
					trial_list = multi_dim_list(n_cells_control_within, n_cells)
					n_reps = trials / n_cells_control_within
					counter = 0
					for i_cell_between in range(0, n_cells):  # looop through btw-factor levels
						for i_cell_within in range(0, n_cells_control_within):  # loop through wtn-factor levels
							trial_list[i_cell_between][i_cell_within] = unique_trials[counter]
							counter += 1
						trial_list[i_cell_between] = int(n_reps) * trial_list[i_cell_between]


				elif factorial_design == "Between-subject" and control_design == "Mixed":
					factors_ordered = factors
					within_control_index = []
					between_control_index = []
					for index, item in enumerate(
							control_variables):  # figure out which of the control_vars is within/between
						if item.f_type == "Within-subject":
							within_control_index.append(index)
						elif item.f_type == 'Between-subject':
							between_control_index.append(index)

					for i_c in within_control_index:
						factors_ordered.append(control_variables[i_c])
					for i_c in between_control_index:
						factors_ordered = [control_variables[i_c]] + factors_ordered

					n_cells_total = n_cells_control_between * n_cells_control_within * n_cells
					n_cells_between_total = n_cells * n_cells_control_between

					trial_list = multi_dim_list(n_cells_control_within, n_cells_between_total)
					balanced_fact_Struct = factorial_combinations(len(factors_ordered),
					                                              [F.level_names for F in factors_ordered],
					                                              n_cells_total)
					unique_trials = giveName(len(factors_ordered), n_cells_total, balanced_fact_Struct)

					n_reps = trials / n_cells_control_within
					counter = 0
					for i_cell_between in range(0, n_cells_between_total):  # looop through btw-factor levels
						for i_cell_within in range(0, n_cells_control_within):  # loop through wtn-factor levels
							trial_list[i_cell_between][i_cell_within] = unique_trials[counter]
							counter += 1
						trial_list[i_cell_between] = int(n_reps) * trial_list[i_cell_between]


				elif factorial_design == "Within-subject" and control_design == "Between-subject":
					factors_ordered = control_variables + factors
					n_cells_total = n_cells * n_cells_control_between
					trial_list = multi_dim_list(n_cells, n_cells_control_between)
					balanced_fact_Struct = factorial_combinations(len(factors_ordered),
					                                              [F.level_names for F in factors_ordered],
					                                              n_cells_total)  # create balanced factor Structure
					unique_trials = giveName(len(factors_ordered), n_cells_total, balanced_fact_Struct)
					n_reps = trials / n_cells
					counter = 0
					for i_cell_between in range(0, n_cells_control_between):  # looop through btw-factor levels
						for i_cell_within in range(0, n_cells):  # loop through wtn-factor levels
							trial_list[i_cell_between][i_cell_within] = unique_trials[counter]
							counter += 1
						trial_list[i_cell_between] = int(n_reps) * trial_list[i_cell_between]


				elif factorial_design == "Within-subject" and control_design == "Within-subject":
					factors_ordered = factors + control_variables
					n_cells_total = n_cells * n_cells_control_within
					balanced_fact_Struct = factorial_combinations(len(factors_ordered),
					                                              [F.level_names for F in factors_ordered],
					                                              n_cells_total)  # create balanced factor Structure
					unique_trials = giveName(len(factors_ordered), n_cells_total, balanced_fact_Struct)
					trial_list = []
					n_reps = trials / n_cells_total
					for iRep in range(0, int(n_reps)):
						[trial_list.append(x) for x in unique_trials]



				elif factorial_design == "Within-subject" and control_design == "Mixed":
					within_control_index = []
					between_control_index = []
					for index, item in enumerate(
							control_variables):  # figure out which of the control_vars is within/between
						if item.f_type == "Within-subject":
							within_control_index.append(index)
						elif item.f_type == 'Between-subject':
							between_control_index.append(index)
					# Bring everything in the right order
					factors_ordered = []
					for index in between_control_index:
						factors_ordered.append(control_variables[index])  # first put between-subj. contr. var.
					for iFac in factors:
						factors_ordered.append(iFac)  # then append within-subject factors
					for index in within_control_index:
						factors_ordered.append(control_variables[index])  # finally, append within-subject contr. vars.
					n_cells_total = n_cells * n_cells_control_within * n_cells_control_between
					n_cells_within_total = n_cells * n_cells_control_within

					balanced_fact_Struct = factorial_combinations(len(factors_ordered),
					                                              [F.level_names for F in factors_ordered],
					                                              n_cells_total)  # create balanced factor Structure
					unique_trials = giveName(len(factors_ordered), n_cells_total, balanced_fact_Struct)
					trial_list = multi_dim_list(n_cells_within_total, n_cells_control_between)

					n_reps = trials / n_cells_within_total
					counter = 0
					for i_cell_between in range(0, n_cells_control_between):  # looop through btw-factor levels
						for i_cell_within in range(0, n_cells_within_total):  # loop through wtn-factor levels
							trial_list[i_cell_between][i_cell_within] = unique_trials[counter]
							counter += 1
						trial_list[i_cell_between] = int(n_reps) * trial_list[i_cell_between]



	#####
	##### for factor structures
	#####
	# No need to distinguish between user specified trials versus probabilities here; don't know what happens when control variables were given
	elif input_type == 'FactStruct':
		print('Factor Structures are still betas')
		if not control: ### In case there are no control variables
			if factorial_design == 'Mixed': # Mixed Design
				#if probability_type == 'trials':  # If trials instead of probabilities were specified
				n_cells_total = n_cells_between * n_cells_within  # total number of cells
				#print("n_cells total = {}, n_cells_between = {}, n_cells_within = {}".format(n_cells, n_cells_between,n_cells_within))
				trial_list = multi_dim_list(trials, n_cells_between)
				#print(trial_list)
				balanced_fact_Struct = factorial_combinations(len(factors_ordered),
				                                              [F.level_names for F in factors_ordered], n_cells_total)
				unique_trials = giveName(len(factors_ordered), n_cells_total, balanced_fact_Struct)
				# Get trial numbers ( couldn't we use the code below and easily transform probabilities in trials?
				trial_numbers = []
				for key, value in prob_mat.items():
					trial_numbers.append(int(value))
				cell_counter = 0
				# Fill the list

				for i_cell_between in range(0, n_cells_between):
					trial_counter = 0
					for i_cell_within in range(0, n_cells_within):
						for i_trial in range(0, trial_numbers[cell_counter]):
							trial_list[i_cell_between][trial_counter] = unique_trials[cell_counter]
							trial_counter += 1
						cell_counter += 1

			elif factorial_design == 'Between-subject':
				print('==========>> <<========= Does this really make sense?')
				print('When trying to set up a factor structure with only between-subject factors, there should come an error message')


			elif factorial_design == "Within-subject": # works with both, probabilities or trials. That is before probabilities were transformed into trials earlier
				balanced_fact_Struct = factorial_combinations(len(factors), [F.level_names for F in factors],
				                                              n_cells)  # create balanced factor Structure
				unique_trials = giveName(len(factors), n_cells, balanced_fact_Struct)
				trial_numbers = []
				for key, value in prob_mat.items():
					trial_numbers.append(int(value))
				#print(trial_numbers)
				cell_counter = 0
				trial_counter = 0
				for i_cell_within in range(0, n_cells_within):
					for iTrial in range(0,trial_numbers[cell_counter]): # loop through number of trials per cell
						trial_list.append(unique_trials[cell_counter])
						trial_counter += 1
					cell_counter += 1




		elif control:  # if control variables were specified and input type = FactStruct
			#
			if factorial_design == 'Mixed':
				if control_design == 'Mixed':
					# Create good order of factors and control variables
					within_control_index = []
					between_control_index = []
					for index, item in enumerate(
							control_variables):  # figure out which of the control_vars is within/between
						if item.f_type == "Within-subject":
							within_control_index.append(index)
						elif item.f_type == 'Between-subject':
							between_control_index.append(index)
					# add the control variables to factors_ordered
					for i_c in within_control_index:
						factors_ordered.append(control_variables[i_c])
					for i_c in between_control_index:
						factors_ordered = [control_variables[i_c]] + factors_ordered

					n_cells_total = n_cells_control_between * n_cells_control_within * n_cells_within * n_cells_between
					n_cells_within_total = n_cells_control_within * n_cells_within
					n_cells_between_total = n_cells_control_between * n_cells_between

					# Get trial numbers for each factor level combination and store them in new array for easier accessibility later
					trial_numbers = []
					for key, value in prob_mat.items():
						trial_numbers.append(int(value))
					#print('trial_numbers = {}'.format(trial_numbers))
					trial_list = multi_dim_list(trials, n_cells_between_total)
					#print('List_trials = {}'.format(trials))
					#print('List_cells = {}'.format(n_cells_between_total))

					balanced_fact_Struct = factorial_combinations(len(factors_ordered),
					                                              [F.level_names for F in factors_ordered],
					                                              n_cells_total)
					unique_trials = giveName(len(factors_ordered), n_cells_total, balanced_fact_Struct)
					print('')
					print('Unique_trials = {}'.format(unique_trials))
					print('------------------------------------------------------------------')
					unique_counter = 0
					trial_number_counter = 0
					# We need to extend trial numbers because we have control variables
					extended_trial_numbers = []
					for i_trial_number in trial_numbers: # loop through desired trial numbers
						for i_wtn_control in range(0,n_cells_control_within): # loop through wtn cells of control variable
							extended_trial_numbers.append(i_trial_number / n_cells_control_within)
					extended_trial_numbers *= n_cells_control_between
					#print(extended_trial_numbers)

					# Fill the trial list
					unique_counter = 0
					for i_cell_between in range(0,n_cells_between_total):
						trial_counter = 0
						for i_cell_within in range(0, int(n_cells_within*n_cells_control_within)):
							for i_trial in range(0, int(extended_trial_numbers[unique_counter])): # loop through number of trial repetetions
								trial_list[i_cell_between][trial_counter] = unique_trials[unique_counter]
								trial_counter += 1
							unique_counter += 1




					"""""
					btw_counter = 0
					for i_cell_between_control in range(0, n_cells_control_between): # loop through that
						for i_cell_between in range(0, n_cells_between):  # looop through btw-factor levels
							trial_counter = 0
							for i_cell_within in range(0, n_cells_within):  # loop through wtn-factor levels
								for i_cell_within_control in range(0, n_cells_control_within):
									for iTrial in range(0,int(trial_numbers[trial_number_counter] / n_cells_control_within)):
										trial_list[btw_counter][trial_counter] = unique_trials[unique_counter]
										trial_counter += 1
										print('trial_counter = {}'.format(trial_counter))
									unique_counter += 1
									print('Unique_counter = {}'.format(unique_counter))
							trial_number_counter += 1
							print('trial number counter = {}'.format(trial_number_counter))
							btw_counter += 1
							print('btw_counter = {}'.format(btw_counter))
					"""""




				elif control_design == 'Between-subject':
					print('FactStruct + between-subject control design not yet implemented in Functions --> MakeTrials()')



				elif control_design == "Within-subject":
					# Create good order of factors and control variables
					within_control_index = []
					between_control_index = []
					for index, item in enumerate(
							control_variables):  # figure out which of the control_vars is within/between
						if item.f_type == "Within-subject":
							within_control_index.append(index)
					for i_c in within_control_index:
						factors_ordered.append(control_variables[i_c])
					# Get trial numbers
					trial_numbers = []
					for key, value in prob_mat.items():
						trial_numbers.append(int(value))

					n_cells_total =  n_cells_control_within * n_cells_within * n_cells_between
					n_cells_between_total =  n_cells_between
					trial_list = multi_dim_list(trials, n_cells_between_total)
					balanced_fact_Struct = factorial_combinations(len(factors_ordered),
					                                              [F.level_names for F in factors_ordered],
					                                              n_cells_total)
					unique_trials = giveName(len(factors_ordered), n_cells_total, balanced_fact_Struct)

					unique_counter = 0
					trial_number_counter = 0
					for i_cell_between in range(0, n_cells_between):  # loop through btw-factor levels
						trial_counter = 0
						for i_cell_within in range(0, n_cells_within):  # loop through wtn-factor levels
							for i_cell_within_control in range(0,n_cells_control_within):
								for iTrial in range(0,int(trial_numbers[trial_number_counter] / n_cells_control_within)):
									trial_list[i_cell_between][trial_counter] = unique_trials[unique_counter]
									trial_counter += 1
								unique_counter += 1
							trial_number_counter += 1


			## Things below are not yet implemented

			elif factorial_design == 'Within-subject':
				print('FactStruct(within-subj) +  within control design not yet implemented in Functions --> MakeTrials()')
				print(probability_type)
				if probability_type == 'trials':
					if control_design == 'Mixed':
						pass
					elif control_design == 'Between-subject':
						pass
					elif control_design == "Within-subject":
						pass
				else:  # if probability
					if control_design == 'Mixed':
						pass
					elif control_design == 'Between-subject':
						pass
					elif control_design == "Within-subject":
						pass


			elif factorial_design == 'Between-subject':
				print('FactStruct(between-subj) +  control design not yet implemented in Functions --> MakeTrials()')

				if probability_type == 'trials':
					if control_design == 'Mixed':
						pass
					elif control_design == 'Between-subject':
						pass
					elif control_design == "Within-subject":
						pass
				else:  # if probability
					if control_design == 'Mixed':
						pass
					elif control_design == 'Between-subject':
						pass
					elif control_design == "Within-subject":
						pass

	return trial_list
