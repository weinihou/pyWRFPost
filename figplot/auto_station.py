#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 16:09:19 2016

@author: shiweisun
"""

import numpy as np
import pandas as pd
import glob
import scipy.io as sio
import matplotlib.pyplot as plt
import time
from scipy import interpolate as interp

chinamap = sio.loadmat('/Users/shiweisun/scripts/china.province.delHK.mat')
filepath = '/Users/shiweisun/data/auto_stations/'
pathout = '/Users/shiweisun/pics/'

filelist = glob.glob(filepath+'*.000')

for filename in filelist:

    timestr = '20'+filename[-12:-4]
    fmt = '%Y%m%d%H'            
    fmt2 = '%m%d_%H:%M'
    deltatime = 0*3600
    timenow = time.mktime(time.strptime(timestr,fmt))+deltatime
    timestr = time.strftime(fmt2,time.localtime( timenow ))
    
    fo = np.genfromtxt(filename,skip_header = 2)
                       #missing_values = float(9999),filling_values = np.nan)
    lon = fo[:,1]
    lat = fo[:,2]
    speed = fo[:,7]
    temp = speed<50
    ##lon1 = np.ma.MaskedArray(lon,temp)
    ##lat1 = np.ma.MaskedArray(lat,temp)
    #speed = np.ma.MaskedArray(speed,temp)
    #speed = speed.reshape([1,speed.size])
    #lon = lon.reshape([1,speed.size])
    #lat = lat.reshape([1,speed.size])
    
    #speed = np.ma.masked_greater_equal(speed,50)
    speed = speed[temp]
    lon = lon[temp]
    lat = lat[temp]
    #%%
    
    xi = np.arange(104,121,0.05)
    yi = np.arange(16,28,0.05)
    GD = interp.griddata((lon,lat),speed,(xi[None,:],yi[:,None]))
    
    fig = plt.figure(figsize=(6,5))
    plt.subplot(111)
    plt.axes(aspect = 1)
    #        plt.axis('equal')
    plt.axis([104.5,121.1,16,28])
    pp = plt.plot(chinamap['long'].squeeze(),chinamap['lat'].squeeze(),color = 'black',linewidth=0.5)
    pm = plt.contourf(xi,yi,GD,levels=np.arange(2,23,2),cmap='rainbow') 
    plt.clim(2,22)
    plt.title('Wind speed at '+timestr,size = 24)
    
    
    
    # Now adding the colorbar
    cbaxes = fig.add_axes([0.925, 0.12, 0.035, 0.3]) 
    cb = plt.colorbar(pm, cax = cbaxes)
    cb.ax.yaxis.set_ticks_position('left')
    #        plt.colorbar(mappable=pm)
    
    #%
    
    plt.tight_layout()
    
    plt.savefig(pathout+'speed_'+timestr[:-3],dpi = 600)
    #        plt.show()
    plt.close()
    
    
    
    
    
    #%%
    # station destribution
#    plt.figure()
#    plt.scatter(lon,lat)
#    plt.show()
    
    
    #filter(lambda x:x is not np.nan,speed)
