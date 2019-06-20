
from NewFactor import NewFactor
from NewBlock import NewBlock
from FactorStruct import FactorStruct

F1 = F_congruency = NewFactor('Congruency', n_levels = 2, factor_type = 'within', level_names = ['congruent','incongruent'])
F2 = F_congruency = NewFactor('Statistic', n_levels = 2, factor_type = 'within', level_names = ['congr_maj','incongr_maj'])
F3 = F_group = NewFactor('Group', n_levels = 2, factor_type = 'between', level_names = ['Control','Treatment'])

B1 = NewBlock(factors = [F1,F2], trials = 100, name = "Block 1")
B2 = NewBlock(factors = [F1,F2,F3], trials = 100, name = "Block 2")
