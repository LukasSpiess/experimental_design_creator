"""""
This class is an object used to design and print 
oput the stimulus lists
"""""



class Table:
	def __init__(self, Blocks, N_subjects):
		self.blocks = Blocks
		self.n_subjects = N_subjects


		# Do some checks because blocks need to have same structure (all blocks need to have same factors)

	def make_table(self):
		### Get dimensionality of the data
		for iBlock in self.blocks: # loop through each block
			for between_factor in range(len(iBlock.trial_list)): # loop through each between subject factor in that block
				print(len(iBlock.trial_list[between_factor]))


