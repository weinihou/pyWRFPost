#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 16:30:49 2017

@author: shiweisun
"""
class DataFile(object):
    def __init__(self,fpath):
        """Generic superclass for data file. 
        maybe ?Could be netCDF, grib1,
            grib2...
            
            from WEM
        """
        self.fpath = fpath
        self.type_of_nwm = ''
        
class NC(DataFile):
    def __init__(self,fpath):
        """Generic netCDF import.

        Subclass of generic DataFile class.
        """
        from netCDF4 import Dataset
        super(NC,self).__init__(fpath)
        self.NC = Dataset(fpath,'r')
        temp = self.NC.TITLE
        if 'WRF' in temp:
            self.type_of_nwm = 'wrf'

            
        
