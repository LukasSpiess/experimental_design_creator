
########################### Subclass for creating a single block object that is being called and used from and in Blockstructure ############################
# Input:
# factors = can be a list of factors or a factor structure from FactStruct
# n_trials how many unique trials? Acts as a sort of multiplier (maybe improve later); default is 1
# Trials_provided
# part_of_between_block_factorp = whether this block is part (ie. a level) of a between-block factor ( factor whoose levels only vary between blocks within a subject)
# Name of the block
# If (multiple) between-subject factors are entered, this class will produce a single block for each of the cells of the factorial combination
# NewBlock should handle between-subject factors differently when being crossed with (mutliple) within-subject factors
# --> Think about what to do when trials = 1 and FactStruct is entered

# Need to work on: if in FS a specific number of trials has been set for factor-level combinations, self.n_trials will be overwritten by that in this block and no trial checks will be done

# Need to make sure that it returns error or warning message once a user enters a control variable of the type f_type = 'between blocks'



from Design import Design
from Functions import *
from NewFactor import NewFactor
from FactorStruct import FactorStruct

class NewBlock:
    def __init__(self, factors, trials=0, name=None, control_variables=None, trials_provided=None,
                 part_of_between_block_factor=None):
        self.factors = factors
        self.name = name
        self.control_vars = control_variables
        self.trials = trials
        self.trials_provided = trials_provided
        self.part_of_between_block_factor = part_of_between_block_factor
        self.trial_list = []
        self.block_identifier = []
        self.factor_type = []
        self.design = ' '

        self.probability_type = None
        #self.prob_mat = None

        self.btw_indices = None
        self.wtn_indices = None

        ##### Initialization ####
        if self.control_vars != None:
            self.control = True
        else:
            self.control = False

        if not isinstance(self.factors, list) and not isinstance(self.factors,
                                                                 FactorStruct):  # put a single input factor in list format to allow for iteration later on
            self.factors = [self.factors]

        if not isinstance(self.control_vars, list): # convert into list if not done before
            self.control_vars = [self.control_vars]

        #############################################
        ##### Determine design of input factors #####
        #############################################
        self.factorial_design = Design(self.factors)
        #print('Right after calling Design Class. Input type is: {}'.format(self.factorial_design.input_type))

        #######################
        ##### Preparation #####
        #######################
        import copy


        if self.factorial_design.input_type == "FactStruct":  # if factor structure is given as input
            print('Factor structure provided as input. This is just beta')

            self.temp_fact_Struct = copy.copy(
                self.factors.temp_fact_Struct)  # for now we make copies of the relevant entries in FactorStruct. This is because particularly prob mat is a mutable data type and thus changes also FactStruct
            self.probability_type = copy.copy(self.factors.probability_type)
            self.prob_mat = copy.copy(self.factors.probabilityMatrix)
            self.factors = copy.copy(self.factors.factors)  # re-assign such that it becomes regular factor
            # Dealing with trials
            if not self.factorial_design.probability_type == 'trials' and self.trials == 0: # if probabilities were used in FactStruct but no trials defined, the user has to enter them here
                print('WARNING: Number of trials not specified')
                try:
                    self.trials = int(input('Please enter number of trials:  '))
                except:
                    self.trials = int(input('Please enter number of trials:  '))
            elif self.factorial_design.probability_type == 'trials':  # if user specified trials in FactStruct, we need to sum them upp
                self.trials = 0
                for iTrial in self.factorial_design.prob_mat.values():
                    self.trials += int(iTrial)
                print('{} trials in total detected'.format(self.trials))
                if self.factorial_design.design == "Between-subject" or self.factorial_design.design == "Mixed": # in these cases, we need to take care to divide the trials over the number of btw blocks
                    if float.is_integer(self.trials / self.factorial_design.n_cells_between): # if number of trials is evenly distributable across blocks go on
                        self.trials = self.trials / self.factorial_design.n_cells_between
                    else:
                        raise Exception('ERROR! Number of trials is not equal in the between-subject factor blocks')

                        self.trials = round(self.trials / self.factorial_design.n_cells_between)
                    print(self.trials)



        ###########################################
        ##### Check for good number of trials #####
        ###########################################

        if self.trials > 1:  ## if more than 1 trial is requested
            self.check = False
            self.skip = False
            if self.factorial_design.input_type == "FactStruct" and self.factorial_design.probability_type == 'trials':
                print('end here when specifying trials in FactStruct')
            else:
                while not self.check:
                    ####### IF input == FactorStruct
                    if self.factorial_design.input_type == "FactStruct":
                        # print("Haven't worked on that yet")
                        if 'probabilities' in self.factorial_design.probability_type:  # if probabilities for f-level combinations are specified
                            self.ls_prob_trials = [(self.trials * float(F)) for F in
                                                   self.factorial_design.prob_mat.values()]  # returns list with #trials for probability --> so transform probabilities in number of trials

                            if not all([float.is_integer(self.trials * float(F)) for F in
                                        self.factorial_design.prob_mat.values()]):  # check wether probabilities in light of given trials result in non-integer trial numbers for any factor-level combination
                                self.check = False
                                from collections import OrderedDict
                                self.cc1 = 0
                                self.cc2 = 0
                                while self.check == False:  # loop until problems with divisible trials have been solved in some way
                                    self.counter = 0
                                    skipper = False
                                    self.tmp_dict_prob_trials = OrderedDict()  # create empty dictionary to show user the #trials with the given probabilities and trials
                                    for ind, key in enumerate(self.factorial_design.prob_mat.keys()):
                                        self.tmp_dict_prob_trials[key] = self.ls_prob_trials[
                                            ind]  # create temporary dictionary that contains #trials for specified p

                                    print('---------------------------------------------------')
                                    print(
                                        'WARNING: Specified probabilities and trials do not result in even number of trials.')
                                    print(' ')
                                    if self.cc1 == 0:
                                        print('=> The {} trials are split up in: '.format(self.trials))
                                    elif self.cc1 > 0:
                                        print('=> The {} trials are split up in: '.format(self.trials_tmp))
                                    if self.cc2 == 0:
                                        self.k = list(self.factorial_design.prob_mat.values())
                                    elif self.cc2 > 0:
                                        self.k = list(self.tmp_prob.values())
                                    print(' ')
                                    for key, item in self.tmp_dict_prob_trials.items():  # print content of dictionary on-screen
                                        print('{} = {} trials with p = {}'.format(key, item,
                                                                                  self.k[self.counter]))
                                        self.counter += 1
                                    print('---------------------------------------------------')
                                    print('')
                                    print('3 Options to choose from:')
                                    print('')
                                    print('1 ==> Change total number of trials in block')
                                    print('2 ==> Change probabilities or trials for factor levels separately')
                                    print('3 ==> Balanced floor and ceiling (across subjects)')
                                    self.case = int(input(
                                        'Please choose any of the options above or cancel with ctr + c:  '))

                                    if self.case == 1:  # enter new amount of trials
                                        self.cc1 += 1
                                        self.trials_tmp = int(input('Please enter a new number of trials: '))
                                        if self.cc2 == 0:  # if no p's were entered before, we use self.prob_mat for probabilities
                                            self.ls_prob_trials = [(self.trials_tmp * float(F)) for F in
                                                                   self.factorial_design.prob_mat.values()]  # re-calculate with new #trials and old p's
                                        elif self.cc2 > 0:  # In case new p's have been entered before, we use the new prob's to re-calculate probabilities
                                            self.ls_prob_trials = [(self.trials_tmp * float(F)) for F in
                                                                   self.tmp_prob.values()]
                                        # print(ls_prob_trials)
                                        # update temporary dictionary
                                        for ind, key in enumerate(self.tmp_dict_prob_trials.keys()):
                                            self.tmp_dict_prob_trials[key] = self.ls_prob_trials[ind]

                                    elif self.case == 2:  # enter new p's
                                        self.cc2 += 1
                                        try:
                                            self.case_2 = int(input(
                                                'Do you want to enter (1) probabilities or (2) trials:  '))
                                        except:
                                            self.case_2 = int(input(
                                                'Do you want to enter (1) probabilities or (2) trials:  '))
                                        self.tmp_dict_prob_trials = ask_probs(len(self.factors),
                                                                              self.factorial_design.n_cells,
                                                                              self.temp_fact_Struct,
                                                                              self.case_2)
                                        self.tmp_prob = copy.copy(
                                            self.tmp_dict_prob_trials)  # here we store the probabilities that were just entered
                                        print('implement checks for valid probabilities here!')
                                        if self.case_2 == 1:  # if probabilities were entered
                                            if self.cc1 == 0:  # if case 1 hasn't been used before, we refer back to self.trials, otherwise to trials_temp
                                                self.ls_prob_trials = [(self.trials * float(F)) for F in
                                                                       self.tmp_dict_prob_trials.values()]
                                            elif self.cc1 > 0:
                                                self.ls_prob_trials = [(self.trials_tmp * float(F)) for F in
                                                                       self.tmp_dict_prob_trials.values()]
                                            # update temporary dictionary
                                            for ind, key in enumerate(self.tmp_dict_prob_trials.keys()):
                                                self.tmp_dict_prob_trials[key] = self.ls_prob_trials[
                                                    ind]  # here trials * P's are stored
                                        elif self.case_2 == 2:  # in case trials were entered (instead of probabilities)
                                            print('Trials entered')
                                            self.factorial_design.probability_type = 'trials' # change the input type for later
                                            self.trials = 0
                                            for key, value in self.tmp_prob.items():  # go through dictionary to extract trials per condition to re-calculate self.trials
                                                self.trials += int(value)
                                            if self.factorial_design.input_type == "FactStruct" and (self.factorial_design.design == "Between-subject" or self.factorial_design.design == "Mixed"):  # in these cases, we need to take care to divide the trials over the number of btw blocks
                                                if float.is_integer(self.trials / self.factorial_design.n_cells_between):  # if number of trials is evenly distributable across blocks go on
                                                    self.trials = self.trials / self.factorial_design.n_cells_between
                                                else:
                                                    print('Warning, number of trials is not equal in the between-subject factor blocks')
                                                    print('Will round it for now')
                                                    self.trials = round(self.trials / self.factorial_design.n_cells_between)
                                            print('Total number of trials per block changed to {}'.format(
                                                self.trials))
                                            skipper = True # this ensures that not later not a wrong number of trials overwrites seklf.trials
                                    elif self.case == 3:  # between subject balancing
                                        print('balanced floor and ceiling not implemented yet. Redo the loop')

                                    ###### check again whether trials are full integers ##############
                                    if self.case == 1:  # enter new trials
                                        # print('right case')
                                        if self.cc2 == 0:
                                            if all([float.is_integer(self.trials_tmp * float(F)) for F in
                                                    self.factorial_design.prob_mat.values()]):  # if everything is okay, give it a go
                                                self.check = True
                                            # print([float.is_integer(self.trials_tmp * float(F)) for F in self.prob_mat.values()])
                                        elif self.cc2 > 0:
                                            if all([float.is_integer(self.trials_tmp * float(F)) for F in
                                                    self.tmp_prob.values()]):  # if everything is okay, give it a go
                                                self.check = True
                                    elif self.case == 2:  # enter new p's
                                        if self.cc1 == 0:  # use self.trials
                                            # print('get here if you have not specified trials before')
                                            # print([float.is_integer(self.trials * float(F)) for F in self.tmp_prob.values()])
                                            if all([float.is_integer(self.trials * float(F)) for F in
                                                    self.tmp_prob.values()]):  # if everything is okay, give it a go
                                                self.check = True
                                        elif self.cc1 > 0:  # use self.trials_temp
                                            if all([float.is_integer(self.trials_tmp * float(F)) for F in
                                                    self.tmp_prob.values()]):  # if everything is okay, give it a go
                                                self.check = True
                                    elif self.case == 2 and self.case_2 == 2:  # in case the user manually entered trials, it'll be okay anyway. We'll just show the trial overview again
                                        print(
                                            'Entered trials. Will continue. But need to further work on this section wrt updating self.prob_mat')
                                        self.factorial_design.probability_type = 'trials'
                                    if self.check == True:
                                        print('Allright! Trials are fine...')
                                        print('')
                                        print('Updated trial distribution:')
                                        print('---------------------------')
                                        self.counter = 0
                                        if self.cc2 == 0:
                                            self.k = list(self.factorial_design.prob_mat.values())
                                        elif self.cc2 > 0:
                                            self.k = list(self.tmp_prob.values())
                                        for key, item in self.tmp_dict_prob_trials.items():  # print content of dictionary on-screen
                                            print('{} = {} trials with p = {}'.format(key, item,
                                                                                      self.k[self.counter]))
                                            self.counter += 1
                                        self.factorial_design.prob_mat = self.tmp_dict_prob_trials  ## To make sure that the updated probabilities or trials are stored in here
                                        if self.cc1 > 0 and skipper == False: # skipper gets True if trials, instead of probabilties, have been used to control number of trials
                                            self.trials = self.trials_tmp  # update self.trials if new amount of trials have been specified and found to be ok ######
                            elif all([float.is_integer(self.trials * float(F)) for F in
                                      self.factorial_design.prob_mat.values()]):  # trials are okay, break the while loop
                                self.check = True
                                print('Allright! Trials are fine...')
                                print('Current Trial Distribution:')
                                print('----------------------------')
                                self.counter = 0
                                self.k = list(self.factorial_design.prob_mat.values())
                                for key, item in self.factorial_design.prob_mat.items():  # print content of dictionary on-screen
                                    self.factorial_design.prob_mat[key] = self.ls_prob_trials[self.counter]   #### For instance, if probabilities were specified and n_trials is okay in light of them, self.factorial_design.prob_mat only contains the n_trials and not the probabilities anymore
                                    print('{} = {} trials with p = {}'.format(key,
                                                                              self.ls_prob_trials[self.counter],
                                                                              item))
                                    self.counter += 1
                                print('----------------------------')
                                break
                            ##### Calculate the number of cells for the 2 different design types
                            # ===>>>>> Code block below might be redundant





                    ####### IF INPUT == FACTOR LIST ########
                    # calculates number of cells
                    elif self.factorial_design.input_type == "Factor":
                        # print('Mutliple facors added')
                        if len(self.factors) == 1:  # if there is just one factor
                            n_cells_tmp = self.factors[0].n_levels
                            if self.factorial_design.design == "Between-subject":
                                self.check = True
                                self.skip = True
                        elif len(self.factors) > 1:  # if there are multiple factors
                            if self.factorial_design.design == "Within-subject":
                                n_cells_tmp = self.factorial_design.n_cells  # self.n_cells_tmp is only used for checking good number of trials
                            elif self.factorial_design.design == "Between-subject":
                                n_cells_tmp = self.factorial_design.n_cells
                                self.check = True  # there is no restriction here as there will be only 1 factor level per subject's stimulus list
                                self.skip = True
                            elif self.factorial_design.design == "Mixed":
                                n_cells_tmp = self.factorial_design.n_cells_within

                        #### Below is code that comes whenever trials > 1 but regardless of whether FactStruct or Factor List were used as input
                        # Code checks whether number of trials is okay
                        if float.is_integer(self.trials / n_cells_tmp) or self.skip == True:
                            self.check = True
                        elif self.factorial_design.input_type == "Factor":
                            print(
                                '\nWARNING:\nFactor levels ({}) cannot be easily balanced across trials ({})\n'.format(
                                    n_cells_tmp, self.trials))
                            print('\nPossible Suggestions:')
                            print('-----------------------')
                            print(
                                '1. Change number of trials to {} or use any number of trials that is a multitude of {}'.format(
                                    round(self.trials / n_cells_tmp) * n_cells_tmp, n_cells_tmp))
                            print(
                                '2. Counterbalanced floor and ceiling of number of trials as between-subject or between block factor --> to be implemented later\n')
                            self.proceed = int(input(
                                '==>Use {} trials, press 1\n==>Manually enter trials, press 2\n==>Counterbalanced floor and ceiling, press 3\n\nEnter: '.format(
                                    round(self.trials / n_cells_tmp) * n_cells_tmp)))
                            if self.proceed == 3:  # floor and ceiling to be implemented later
                                print('Will be implement later. Will stop here')
                                break
                            elif self.proceed == 1:  # Use suggestion of trials
                                self.trials = round(self.trials / n_cells_tmp) * n_cells_tmp
                            elif self.proceed == 2:  # user manually enters number of trials (again)
                                self.trials = int(input('Please enter number of trials for this block:  '))
                                print('')
                                print('')
                            # if self.input_type == "Factor":
                            ### while loop ends here






            ##############################################################
            ############## dealing with control variables ################
            ##############################################################

            if self.control:
                print('{} control variable(s) detected'.format(len(self.control_vars)))
                self.control_design = Design(self.control_vars) #### determine design of control variables



                ### checking for good number of trials when including also the control variables ###
                if self.factorial_design.input_type == "FactStruct":
                # Keep in mind that at this point, regardless of whether self.factorial_design.probability_type is trials or probabilities, prob_mat always already contains the trials and NOT(!) the probabilities anymore. That conversion took place before when checking trials for FS
                    if self.control_design.n_cells_within != None: # if there's at least one within-subject control variable
                        """""
                        # Now Users should have two options:
                        #   1.) Balance wtn control variables separately for and within each factor level combination in FS
                        #   2.) Balance wtn control variables w.r.t. total number of trials (which might be used more often
                        # Point 1 is already more or less implement. Point 2 should be really easy to do. For more on that read information in NewControl.py
                        # ==> Let users make a choice here and then use scenarios for the code below
                        # Think about what to do if both doesn't work out in terms of specified trials and cells etc... I guess in the GUI some things are much easier to handle than in command window
                        """""

                        for key, value in self.factorial_design.prob_mat.items():  # for every entry in the prob_mat we check whether number of cells of within control variables can be nicely balanced across number of trials
                            check_3 = False
                            while not check_3:  # iterate until trials are good
                                if not float.is_integer(int(value) / self.control_design.n_cells_within):  # if number of trials not optimal



                                    print(
                                        "-------------------------------------------------------------------------------------------------------------------------")
                                    print(
                                        "Counterbalancing control variables across this factor level is not fully possible:")
                                    print(
                                        "Specified {} trials for {}. However, there are {} within-subject cells.".format(
                                            int(value), key, self.control_design.n_cells_within))
                                    print("Choose from the following: ")
                                    print(
                                        "1 ==> Full counterbalancing: Automatically change number of trials for {} from {} to {}. Please note that this might result in other errors later in the program".format(
                                            key, int(value), round(int(
                                                value) / self.control_design.n_cells_within) * self.control_design.n_cells_within))
                                    print(
                                        "2 ==> Full counterbalancing: Manually change number of trials to multitude of {}".format(
                                            self.control_design.n_cells_within))
                                    print(
                                        "3 ==> Incomplete counterbalancing: Counterbalance as much as possible without changing the number of trials")
                                    print(
                                        "4 ==> Randomization: Randomize the distribution of control variables over factor levels without changing number of trials")
                                    print(" ")
                                    print(
                                        'Please choose any of the actions above by entering the respective number or cancel by pressing ctrl + c')
                                    try:
                                        case_3 = int(input("Please make a choice: "))
                                    except:
                                        case_3 = int(input("Please make a choice: "))
                                    # Go through scenarios
                                    if case_3 == 1:  # automatic trial change
                                        self.factorial_design.prob_mat[key] = str(round(int(
                                            value) / self.control_design.n_cells_within) * self.control_design.n_cells_within)
                                        print('Trials changed to {}'.format(self.factorial_design.prob_mat[key]))
                                        print('WARNING: Automated Trial change might lead to uneven number of trials across levels of one or more between-subject factors.')
                                        print('This will be updated in the near future.---> High priority')
                                        # Now, we need to update also self.trials and take care that, depending on design, we divide self.trials correctly by n_cells_between
                                        self.trials = 0
                                        for key, value in self.factorial_design.prob_mat.items():
                                            self.trials += int(value)

                                        if self.factorial_design.design == "Mixed" or self.factorial_design.design == "Between":
                                            self.trials /= self.factorial_design.n_cells_between
                                        check_3 = True
                                    elif case_3 == 2:  # manually change trials
                                        try:
                                            trial_temp = int(input(
                                                'Please enter number of trials that are multitude of {} for {}:  '.format(
                                                    key, self.control_design.n_cells_within)))
                                            print('WARNING: Here needs to come some code that checks, whether the entered trials are evenly distributed across all available between-subject factors')
                                        except:
                                            print('--------------------------------------')
                                            print('Invalid input format. Please try again')
                                            print('--------------------------------------')
                                            trial_temp = int(input(
                                                'Please enter number of trials that are multitude of {} for {}:  '.format(
                                                    key, self.control_design.n_cells_within)))
                                        self.factorial_design.prob_mat[key] = str(trial_temp)
                                        value = trial_temp
                                    elif case_3 == 3:
                                        print('Sorry! Not implemented yet')
                                    elif case_3 == 4:
                                        print('Sorry! Not implemented yet')

                                else:  # if number of trials is ok
                                    check_3 = True



                if self.factorial_design.input_type == 'Factor':
                    ### Determine optimal number of trials for including control variables as well (next to regular factor level combinations)
                    # if self.design == "Within-subject" or self.design == "Mixed" or self.control_design == 'Within-subject': # in these cases, we need to calculate n_cells_within * n_cells control and check whether self.trials is divisible
                    # print('n_cells control = {}; n_cells_between = {}'.format(self.n_cells_control,  self.n_cells_between))
                    if self.factorial_design.design == "Between-subject" and self.control_design.design == "Within-subject":
                        self.n_cells_total = self.control_design.n_cells_within
                    elif self.factorial_design.design == "Between-subject" and self.control_design.design == "Between-subject":
                        self.n_cells_total = 1
                    elif self.factorial_design.design == "Between-subject" and self.control_design.design == "Mixed":
                        self.n_cells_total = self.control_design.n_cells_within
                    elif self.factorial_design.design == "Within-subject" and self.control_design.design == "Within-subject":
                        self.n_cells_total = self.factorial_design.n_cells_within * self.control_design.n_cells_within
                    elif self.factorial_design.design == "Within-subject" and self.control_design.design == "Between-subject":
                        self.n_cells_total = self.factorial_design.n_cells_within
                    elif self.factorial_design.design == "Within-subject" and self.control_design.design == "Mixed":
                        self.n_cells_total = self.factorial_design.n_cells_within * self.control_design.n_cells_within
                    elif self.factorial_design.design == "Mixed" and self.control_design.design == "Within-subject":
                        self.n_cells_total = self.factorial_design.n_cells_within * self.control_design.n_cells_within
                    elif self.factorial_design.design == "Mixed" and self.control_design.design == "Between-subject":
                        self.n_cells_total = self.factorial_design.n_cells_within
                    elif self.factorial_design.design == "Mixed" and self.control_design.design == "Mixed":
                        self.n_cells_total = self.factorial_design.n_cells_within * self.control_design.n_cells_within

                    if not float.is_integer(
                                    self.trials / self.n_cells_total):  # if number of trials / n_cells_total is not an integer
                        print(
                            "-------------------------------------------------------------------------------------------------------------------------")
                        print(
                            "Specified {} trials. Counterbalancing control variables across factor levels is not fully possible.".format(
                                self.trials))
                        print("Choose from the following: ")
                        print("1 ==> Full counterbalancing: Automatically change number of trials to {}".format(
                            round(self.trials / self.n_cells_total) * self.n_cells_total))
                        print(
                            "2 ==> Full counterbalancing: Manually change number of trials to multitude of {}".format(
                                self.n_cells_total))
                        print(
                            "3 ==> Incomplete counterbalancing: Counterbalance as much as possible without changing the number of trials")
                        print(
                            "4 ==> Randomization: Randomize the distribution of control variables over factor levels without changing number of trials")
                        print(" ")
                        print(
                            'Please choose any of the actions above by entering the respective number or cancel by pressing ctrl + c')
                        try:
                            case_2 = int(input("Please make a choice: "))
                        except:
                            case_2 = int(input("Please make a choice: "))
                        # Deal with the cases
                        if case_2 == 1:  # full counterbalancing by changing self.trials
                            self.trials = round(self.trials / self.n_cells_total) * self.n_cells_total
                        # print('Warning: eg., in a mixed design we also then need to update n_cells and n_reps etc.')
                        elif case_2 == 2:  # manually change number of trials
                            self.trials = int(input("Please enter a new number of trials here:  "))
                            #print(
                            #    'Warning: eg., in a mixed design we also then need to update n_cells and n_reps etc.')
                        elif case_2 == 3:  # incomplete counterbalancing
                            print("This operation will not be executed here")
                            print(
                                'Check whether this does not result in a systematic assignment of control variable combinations and factor level combinations')
                        elif case_2 == 4:  # randomization
                            print("This operation will not be executed here")
                        else:
                            print("Invalid")

                    ### Make the trial list for the control variables

                    # print('Dont forget, Lukas, to deal with the different types of control variables and how they relate to the overal trial and block structure')
                    # print('This needs to be done in the code directly below')
                    # print('Idea would be to make separate trial_list for control variables that is as long as factor trial_list')
                    # print('n_cells_control = {}'.format(self.n_cells_control))
                    # print('I will move the section with making the actual trial list to a later point')




        ################################################################################################################
        ############################### MAIN BODY ######################################################################
        ################# Stimulus_Lists are created in here #######################
        # print('rt ')

        if not self.control:
            self.trial_list = MakeTrials(self.factors, self.factorial_design.input_type, int(self.trials),
                                         self.factorial_design.design, self.factorial_design.probability_type,
                                         self.factorial_design.prob_mat, factors_ordered=self.factorial_design.factors_ordered,
                                         n_cells=self.factorial_design.n_cells,
                                         n_cells_within=self.factorial_design.n_cells_within,
                                         n_cells_between=self.factorial_design.n_cells_between)
        else:
            self.trial_list = MakeTrials(self.factors, self.factorial_design.input_type, int(self.trials),
                                         self.factorial_design.design, self.factorial_design.probability_type,
                                         self.factorial_design.prob_mat, factors_ordered=self.factorial_design.factors_ordered,
                                         n_cells=self.factorial_design.n_cells,
                                         n_cells_within=self.factorial_design.n_cells_within,
                                         n_cells_between=self.factorial_design.n_cells_between,
                                         n_cells_control=self.control_design.n_cells,
                                         n_cells_control_between=self.control_design.n_cells_between,
                                         n_cells_control_within=self.control_design.n_cells_within,
                                         control_design=self.control_design.design,
                                         control_variables=self.control_vars)

        # print('made it ')


        """


        # Make a list that contains only the blockname (for later printing)
        [self.block_identifier.append(self.name) for i in range(0,self.trials)]
        """

    ################################ SOME USEFUL METHODS ASSOCIATED ##################################
    def shuffle_trials(self):
        from random import shuffle
        if self.design == "Within-subject":
            self.trial_list = shuffle(self.trial_list)
            print('Trials have been shuffled')
        elif self.design == "Between-subject":
            print("Full between-subject design encountered. Unsure what to shuffle. ")
            print('==> Left data unchanged')
        elif self.design == "Mixed":
            for i in range(0, len(self.trial_list)):
                shuffle(self.trial_list[i])  # shuffle trials independently in each block
                print('Trials have been shuffled')
        return self.trial_list

    ################################ SOME ADDITIONAL STUFF #######################################
    def __repr__(self):
        return 'NewBlock(Name = {}, factors = {}, trials_provided = {}, part_of_between_block_factor = {}, trials = {}'.format(
            self.name, self.factors, self.trials_provided, self.part_of_between_block_factor, self.trials)

    def __str__(self):
        if self.input_type == "FactStruct":
            return "Need to work on representation when using FactStruct for creating a block"
        else:
            return '\n-------------------------------------------------\nBlock: {}\nDesign: {}\nFactors: {}\nFactor type(s): {}\nTrials: {}\n-------------------------------------------------\n'.format(
                self.name, self.factors, self.factor_type, self.trials)

#print('made it ')


"""


# Make a list that contains only the blockname (for later printing)
[self.block_identifier.append(self.name) for i in range(0,self.trials)]
"""











