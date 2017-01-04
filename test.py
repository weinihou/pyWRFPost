# -*- coding: utf-8 -*-
'''
This is the test file to 'getver' ~


'''
#from getvar import constants
#from getvar import interpvar
import getvar


import glob
# path for input data
filepath = '/Users/shiweisun/data/case_split2nest/'

# filenames
filelist = glob.glob(filepath+'wrfout*')
fo = getvar.open(filelist[0])
