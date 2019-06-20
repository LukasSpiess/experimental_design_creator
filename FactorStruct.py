"""""
1.) When entering muzltiple factors, eg. 1 between & 2 within, the summation of the probabilities does not work correctly
"""""


########################### Class object for uneven balanced crossed Factor structure (i.e., hierarchy) ###########################
# Better work on the __repr__ and __str__ functions
# Make this class check whether input probabilities sum to 1.
# Allow user to choose between entering probabilities (in % or p) or number of trials
# Allows as input a single factor and multiple factors
# At some point make the code more concise!!!
# When probability matrix is provided, user needs to enter it as OrderedDict() from the collections module in Python >2.7 standard library

from Functions import*
import Design as DS
from collections import OrderedDict

class FactorStruct:
    # __doc__     # documentation for later
    def __init__(self,factors, probabilityMatrix = None):  # probability matrix describes the probability of a given factor-level combination and needs as many entries as there are factor levels.
        from numpy import isclose
        self.probabilityMatrix = probabilityMatrix
        self.factors = factors
        if self.probabilityMatrix is None:
            self.probabilityMatrix = {}
            self.probability_type = ' '
        else:
            #self.probabilityMatrix = OrderedDict(self.probabilityMatrix.items())
            self.probability_type = 'probabilities'
            if not isinstance(self.probabilityMatrix, OrderedDict):
                print('Keep in mind to only provide ordered dictionaries from collections module as probability matrix')
                print('Trial Lists from NewBlock Class will  most likely not be correct')
        
        self.type = ' '
        ## Do some checks
        if not isinstance(self.factors, list):  # if input is not a list convert it to one
            self.factors = [self.factors]
        try:
            if all(["Between" in F.f_type for F in
                    self.factors]):  # in case there are only between subject factors, return error
                print("ERROR: Cannot only deal with between subject factors.")
        except:
            if "Between" in self.factors[0].f_type:
                print("Only 1 factor specified, which is between-subject. Cannot continue")
        else:
            if len(self.factors) == 1:
                self.type = 'single'
            else:
                self.type = 'multi'
            if self.type == 'multi':

                btw_indices = []
                self.n_between = 0
                wtn_indices = []
                self.n_within = 0
                self.factor_type = []
                [self.factor_type.append(x.f_type) for x in self.factors]  # check factor types
                self.n_cells = prod([F.n_levels for F in self.factors])  # number of cells for factor levels
                for index, i_type in enumerate(self.factor_type):
                    if "Between" in i_type:
                        btw_indices.append(index)
                        self.n_between += 1
                    else:
                        wtn_indices.append(index)
                        self.n_within += 1 # update number of between- and within-subject factors
                self.n_cells_between = 1
                for i in range(0, len(
                        btw_indices)):  # caluclate number of cells separately for between and within subject factors
                    self.n_cells_between *= self.factors[
                        btw_indices[i]].n_levels  # how many cells the between-subject factors have
                self.n_cells_within = 1
                for i in range(0, len(wtn_indices)):
                    self.n_cells_within *= self.factors[wtn_indices[i]].n_levels

                # Order the factors ----> This ensures that on the left side always the between-subject factors are coming
                self.factors_ordered = []  # herein, we save an ordered list of factors, in which the btw-factors come first
                for i in range(0, len(btw_indices)):  # caluclate number of cells
                    self.factors_ordered.append(self.factors[btw_indices[i]])
                for i in range(0, len(wtn_indices)):
                    self.factors_ordered.append(self.factors[wtn_indices[i]])
                self.factors = self.factors_ordered

                self.factor_type = []
                [self.factor_type.append(x.f_type) for x in self.factors]  # check factor types

            else:
                self.factor_type = self.factors[0].f_type
                self.n_cells = self.factors[0].n_levels
            print('')
            FSD = DS.Design(self.factors)  # get design
            #############################################
            if self.probabilityMatrix: 
                if self.type == 'multi':
                    self.temp_fact_Struct = factorial_combinations(len(self.factors), [F.level_names for F in self.factors],
                                                                   self.n_cells)  # create all possible factorial combinations
                else:  # in case only a single factor is given we need to do it different as there can't be a factorial_combinations structure
                    # temp_fact_Struct = factorial_combinations(len(self.factors),self.factors[0].level_names, n_cells)
                    ll = multi_dim_list(self.n_cells, 1)
                    self.temp_fact_Struct = ll
                    for index, item in enumerate(self.factors[0].level_names):
                        ll[0][index] = item  # create list that contains the level names
            elif not self.probabilityMatrix:
                print("----------------------------------------------------------------------")
                print("Choose between: ")
                print("1 ==> Enter probabilities for factor level combinations")
                print("2 ==> Enter number of trials for factor level combinations")
                case = int(input('Please enter your choice: '))
                print("----------------------------------------------------------------------")
                if case == 1:
                    self.probability_type = 'probabilities'
                elif case == 2:
                    self.probability_type = 'trials'
                    print(
                        'IMPORTANT: PLEASE MAKE SURE THAT THE TOTAL NUMBER OF TRIALS IS THE SAME WITHIN ALL LEVEL COMBINATIONS OF THE BETWEEN-SUBJECT FACTORS')
                    print("----------------------------------------------------------------------")
    
                # Create all possible factorial combinations
                if self.type == 'multi':
                    self.temp_fact_Struct = factorial_combinations(len(self.factors), [F.level_names for F in self.factors],
                                                                   self.n_cells)  # create all possible factorial combinations
                else:  # in case only a single factor is given we need to do it different as there can't be a factorial_combinations structure
                    # temp_fact_Struct = factorial_combinations(len(self.factors),self.factors[0].level_names, n_cells)
                    ll = multi_dim_list(self.n_cells, 1)
                    self.temp_fact_Struct = ll
                    for index, item in enumerate(self.factors[0].level_names):
                        ll[0][index] = item  # create list that contains the level names
                # Ask for user input on the probabilities associatied with each possible factor combination
                check = False
                while not check:
                    if self.type == "multi":
                        self.probabilityMatrix = ask_probs(len(self.factors), self.n_cells, self.temp_fact_Struct,
                                                           case)  # returns a dictionary with key = crossed factor names and values  = probabilities
                    else:
                        self.probabilityMatrix = ask_probs(len(self.factors), self.n_cells, ll, case)
                    if case == 1:  # if probabilities or % entered
                        if self.type == "multi":
                            if not isclose(self.n_cells_between, sum(map(float, self.probabilityMatrix.values()))):
                                print('--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--')
                                print('Probabilities do not sum to 1 ')
                                print('Please try again:')
                                print('--------------------------------------------------------')
                            # check = True
                            elif isclose(self.n_cells_between, sum(map(float, self.probabilityMatrix.values()))):
                                print('Valid probabilities entered...countinue')
                                check = True
                        else:  # in case a single factor is entered
                            if not isclose(1, sum(map(float, self.probabilityMatrix.values()))):
                                print('--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--')
                                print('Probabilities do not sum to 1 ')
                                print('Please try again:')
                                print('--------------------------------------------------------')
                            # check = True
                            elif isclose(1, sum(map(float, self.probabilityMatrix.values()))):
                                print('Valid probabilities entered...countinue')
                                check = True
                    else:  # in case trials are entered
                        #Now check, whether the number of trials is the same across all levels of any of the btw factors.
                        btw_cell_numbers = [] # herein, we store how many cells each btw factor has
                        for i_btw_factor in range(0,self.n_between):
                            btw_cell_numbers.append(int(self.factors_ordered[i_btw_factor].n_levels))
                        # Put all the trials in a new list
                        trial_numbers = []
                        for key, value in self.probabilityMatrix.items():
                            trial_numbers.append(int(value))
                        for i_factor in range(0,len(btw_cell_numbers)): # loop through each factor
                            #print('i_Factor = {}'.format(i_factor))
                            step_0 = 0
                            step_1 = int(self.n_cells / btw_cell_numbers[i_factor])  # determine the step size to divide n_cells in even bins
                            for i_cell in range(0, btw_cell_numbers[i_factor]): # loop through each cell of that factor
                                #print('i_cell = {}'.format(i_cell))
                                #print('step_0 = {}'.format(step_0))
                                #print('step_1 = {}'.format(step_1))
                                if i_cell == 0:
                                    tmp_trials = [sum(trial_numbers[step_0:step_1])]
                                else:
                                    tmp_trials.append(sum(trial_numbers[step_0:step_1]))
                                step_0 += int(self.n_cells / btw_cell_numbers[i_factor])
                                step_1 += int(self.n_cells / btw_cell_numbers[i_factor])
                                #print(tmp_trials)
                            if len(set(tmp_trials)) != 1: # check
                                raise Exception('ERROR! Number of trials is not equal across the levels of one or more between-subject factors')
                            else:
                                check = True
                        check = True
                    print('Factor Structure created')

    ##########################
    def __repr__(self):
        return 'FactorStruct({} with probability mat = {})'.format(self.factors, self.probabilityMatrix)

    def __str__(self):
        return '\n-------------------------------------------------\nFactorStructure for {}\n-------------------------------------------------\nprobability matrix = {}\n-------------------------------------------------\n'.format(
            self.factors, self.probabilityMatrix)
