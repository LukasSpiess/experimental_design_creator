#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 15:13:29 2017

@author: Lukas

This library is intended to create counterbalanced stimulus lists

"""


"""
############# TO-DOs ################
1.) Try not to use any third-party library such as numpy.
    Replace numpy array (i.e., temp_mat with a multidimensional python list. These lists can then be used as keys in
    a dictionary with the probabilities as values
2.) Write documention for each class
3.) Do not forget to allow crossing of within- and between subject factors
4.) in class: FactorStruct make sure that and how manually entered probabilityMatrix should look like / how it should work etc.
5.) Make the program also work when there is just a single factor
6.) For later, think about importing stimuli such as sentences etc.
7.) In NewBlock, make between-subject factors always appear first

"""

from importlib import reload
from Functions import*
from FactorStruct import FactorStruct
from NewFactor import NewFactor
from NewControl import NewControl
from BlockStruct import BlockStruct
from NewBlock import NewBlock
from Design import Design




### Danaja
Shape = NewFactor('Shape', 2, ['square', 'circle'])
Tone = NewFactor('Tone', 2, ['High', 'Low'])
Target = NewFactor('Target', 2, ['left', 'right'])
Mapping_1 = FactorStruct([Shape,Tone, Target])
block_1 = NewBlock(Mapping_1, trials = 100, name = "Block_1")






# Within factors
F1 = NewFactor('F1',3, ['WF1_1','WF1_2','WF1_3'])
F2 = NewFactor('F2',3, ['WF2_1','WF2_2','WF2_3'])
F3 = NewFactor('F3',3, ['F3_1','F3_2','F3_3'])
F4 = NewFactor('F4',3, ['F4_1','F4_2','F4_3'])
# Between factors


# Within controls
C1 = NewControl('C1', 3, ['WC1_1','WC1_2','WC1_3'])
C2 = NewControl('C2', 3, ['WC2_1','WC2_2','WC2_3'])
C7 = NewControl('C7', 3, ['WC7_1','WC7_2','WC7_3'])
C8 = NewControl('C9', 3, ['WC8_1','WC8_2','WC8_3'])
# Between controls
C5 = NewControl('C5', 3, ['BC5_1','BC5_2','BC5_3'])
C6 = NewControl('C6', 3, ['BC6_1','BC6_2','BC6_3'])
C3 = NewControl('C3', 3, ['BC3_1','BC3_2','BC3_3'])
C4 = NewControl('C4', 3, ['BC4_1','BC4_2','BC4_3'])


B = NewBlock([F1,F2, F3],trials = 100, control_variables=[C1, C5])

#BS = BlockStruct(F1, n_blocks=4, trials_per_block = 99)