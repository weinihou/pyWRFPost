#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 11:23:34 2017

@author: shiweisun
"""
from .datafile import NC
    
class OUT(NC):
    def __init__(self,fpath):
        super(OUT,self).__init__(fpath)
        pass
    def getvar(self,vrbl):
        '''
        Get the variables.
        
        '''
        from .originvar import originvar
        return originvar(self,vrbl)
        
        pass

def open(fpath):
    '''
    Open the file, and get a class 'NC'
    '''
    return OUT(fpath)
