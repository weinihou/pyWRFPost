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
    def getvar(self,vrbl,ztype=None,zlevels=None):
        '''
        Get the variables.
        
        '''
        from .originvar import originvar
        temp = originvar(self,vrbl)
        if ztype is None:
            var = temp
            pass
        else:
            from .interpvar import interp_z
            var = interp_z(self,temp,ztype,zlevels)
            
        return var
        pass

def open(fpath):
    '''
    Open the file, and get a class 'NC'
    '''
    return OUT(fpath)
