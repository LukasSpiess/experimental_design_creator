
########################### Class object for creating blocks ###########################
# When creating a block structure, we can not easily create a (regular) trial structure later. So block structure will be optional and the more advanced option compared to just making a regular trial structure
# Think about FactorStruct when implemented in a block fashion (in light of the porbabilities that were entered)
# Allow BlockStructure to be an object that can also be independently used of FactorStruct (e.g., when the last block of an exp is totally different from the previous ones, such that multiple independent blockStructures can be combined later for creating the final stimulus List

# Ask for printing block ID
# How many blocks?
# Allow input to be FactStruct and simple factors (would be nice if both can be optional such that in this case, only a block blueprint structure is given as output)
# trials per block? (optional???) --> default will be None. In this case, every unique factor combination will be put in once and a multiplier can be applied later when making trial structure
# Between-block factors? (optional) <--- a within-subject factor can (also) be a between-block factor. Think about using more than one between-block factor at once
# Add a method(?) that allows to add a new block to an already existing blockstructure
# between_block_factor should accept one or more factors
# Factors as input should be only those that are not (also) used as between-block factors
from FactorStruct import FactorStruct
from NewFactor import NewFactor
from NewBlock import NewBlock


class BlockStruct:
    def __init__(self, factors, between_block_factor = None, shuffle_trials_in_block = False ,add_block = None,n_blocks = 1, trials_per_block = 1):
        self.n_blocks = n_blocks
        self.factors = factors
        self.trials_per_block = trials_per_block
        self.shuffle_trials_in_block = shuffle_trials_in_block
        self.between_block_factor = between_block_factor
        self.add_block = add_block
        self.new_blocks = []

        ####  Some preparation stuff ####
        if not isinstance(self.factors,list):
            self.factors = [self.factors] # convert to appropriate format


        ################################################################################################################
        ############################### MAIN BODY ######################################################################
        if isinstance(self.factors, FactorStruct): # in Case input = FactStruct
            print('FactorStructure provided as input. Need to work on tht')
            'Need to take how we handle trials per block etc.'
        ########### Create n_blocks using simple factors entered as input ##############
        elif all([isinstance(x, NewFactor) for x in self.factors]) and between_block_factor == None: # if self.factors are all just single factors and no between-block-factor is set:
            for i in range(0,self.n_blocks): # loop through desired number of blocks
                dyn_name = 'Block {}'.format(i+1) # give dynamic block name
                self.new_blocks.append(NewBlock(self.factors, name = dyn_name, trials = self.trials_per_block))
                if self.shuffle_trials_in_block: # shuffle trials in block if wanted
                    self.new_blocks[i].shuffle_trials()

