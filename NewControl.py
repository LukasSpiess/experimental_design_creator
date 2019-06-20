########################### Class object for creating a controll object ###########################


"""""
What I need to be aware of is that if a within-subject control variable has been created and is to be used with a FS, then my program so far only balances
this control variable within each level of the FS. This can result in a situation in which, across all the factor structure factor level combinations the 
control variable is not balanced. Eg. C1.1 is 50% within F1.1 but F1.1 is p = .7 and F1.2 is p = .3. Would be good to give the user 3 options:
1. Balance the wtn control variables separately for and within each level within FS, which results in the situation above
2. Allow the user to choose that instead, the wtn control variable will be balanced on the full number of trials (e.g., F1.1 = p = .7 but total_trial = 100 --> C1.1 = 50 trials, C1.2 = 50 trials and randomized across F1.1 and F1.2)
3. Allow user to specify the conditional probabilities of the distr. of control variables given the distribution of factor levels. However, this is quite complex to implement and might not be used a lot

==> So I should allow for option 1 and 2

"""""



class NewControl:
    def __init__(self,name, n_levels, level_names = None):
        self.name = name
        self.n_levels = n_levels
        KL = int(input('Balance between subjects (=1), within subjects (=2), between-blocks within subjects (=3): '))
        if KL == 1:
            self.f_type = 'Between-subject'
        elif KL == 2:
            self.f_type = 'Within-subject'
        elif KL == 3:
            self.f_type = 'between blocks'
        self.level_names = level_names
        if self.level_names == None:
            self.level_names = []
            [self.level_names .append(str(k)) for k in range(0,self.n_levels)] # if no factor level names are provided use integers starting from 0
        elif not len(self.level_names) == self.n_levels:
            print("WARNING: number of level names ({}) do not match number of levels assigned ({}) to this factor".format(len(self.level_names), str(self.n_levels)))
    def __repr__(self):
        return 'NewControl({}, {}, {})'.format(self.name, self.n_levels, self.level_names)
    def __str__(self):
        return "\n-------------------------------------------------\nControl Name:   {}\nBalance type:   {}\nlevels:         {}\nLevel names:    {}\n-------------------------------------------------\n".format(self.name, self.f_type, self.n_levels, self.level_names)





