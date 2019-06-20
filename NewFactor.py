########################### Class object for creating a factor ###########################

class NewFactor:
    def __init__(self, name, n_levels, factor_type = "between", level_names = None):
        self.name = name
        self.n_levels = n_levels
        self.f_type = factor_type
        self.level_names = level_names
        if self.f_type == 'within':
            self.f_type = 'Within-subject'
        elif self.f_type == 'between':
            self.f_type = 'Between-subject'
            
        if self.level_names == None:
            self.level_names = []
            [self.level_names .append(str(k)) for k in range(0,self.n_levels)] # if no factor level names are provided use integers starting from 0
        elif not len(self.level_names) == self.n_levels:
            print("WARNING: number of level names ({}) do not match number of levels assigned ({}) to this factor".format(len(self.level_names), str(self.n_levels)))
    def __repr__(self):
        return 'NewFactor({}, {}, {})'.format(self.name, self.n_levels, self.level_names)
    def __str__(self):
        return "\n-------------------------------------------------\n Factor Name:   {}\n Factor levels: {}\n Level names:   {}\n Type:          {}\n-------------------------------------------------\n".format(self.name, self.n_levels, self.level_names, self.f_type)





