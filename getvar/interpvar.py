#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 16:23:57 2017

interplate variables

interp_p 
interp_h
interp_agl
interp_lonlat


@author: shiweisun
"""
import numpy as np
from .datafile import NC

def get_h(NC):
    terrain = NC.variables['HGT'][:]
    ph = NC.variables['PH'][:]
    
    ph += NC.variables['PHB'][:]
    #phb = fo.variables['PHB'][:]
    #%
    g=9.81
    ph = (ph[:,:-1,:,:]+ph[:,1:,:,:])/2
    height_above_sea = ph/g
    height_above_ground = height_above_sea - terrain.reshape([12,1,498,750])
    return height_above_ground,height_above_sea

def interp_z(NC,vrbl,ztype,zlevels,):
    if zlevels is None:
        raise 'aaaaa'
    elif ztype.lower() == 'p':
#        pressure_pert = NC.getvar()
        pass
    elif ztype.lower() in ['h','agl']:
        hgt 
        ph
        phb
        
        pass
        
