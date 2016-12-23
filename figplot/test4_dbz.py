#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 10:37:33 2016
Using basemap, adjust the region by reading the nc file
Using china.... map data

@author: shiweisun
"""


import numpy as np
import netCDF4 
import time
import glob

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.cm as cm
#from . import constants     # can only do when this file is imported
g = 9.81
sswcmap =[[  0  ,  0.6875  ,  1.0000],
       [  0  ,  1.0000   , 1.0000],
       [      0   , 0.8902    ,     0],
       [ 0.1686  ,  0.5059   , 0.3373],
       [ 1.0000  ,  1.0000   ,      0],
       [ 1.0000  ,  0.7778   ,      0],
       [ 1.0000  ,  0.5186   ,      0],
       [ 1.0000  ,  0.2593   ,      0],
       [ 0.8529   , 0.1296   ,      0],
       [ 0.7059   ,      0   ,      0],
       [ 1.0000   ,      0  ,  1.0000],
       [ 0.5216  ,       0  ,  0.5216],
       [ 0.8000   , 0.6000  ,  1.0000]]
import matplotlib.colors as pltc
scmap = pltc.ListedColormap(sswcmap,name='radarcolor')

import scipy.io as sio

chinamap = sio.loadmat('/Users/shiweisun/scripts/china.province.delHK.mat')


#lon = chinamap['long'].squeeze()
#lat = chinamap['lat'].squeeze()


#%%
pathout = '/Users/shiweisun/pics/'
filepath = '/Users/shiweisun/data/case_split2nest/'
filelist = glob.glob(filepath+'wrfout*')

for filename in filelist :
    print filename

#filename = 'wrfout_d03_2016-04-12_20:05:00'

    fo = netCDF4.Dataset(filename,'r') 
    
    #%%
    dx = fo.DX
    cen_lat = fo.CEN_LAT
    cen_lon = fo.CEN_LON
    truelat1 = fo.TRUELAT1
    truelat2 = fo.TRUELAT2
    #U = fo.variables['U']
    at = [ fo.variables['Times'][a] for a in np.arange(0,fo.dimensions['Time'].size)]
    timelist = [''.join(at[a]) for a in np.arange(fo.dimensions['Time'].size)]
    fmt = '%Y-%m-%d_%H:%M:%S'            
    fmt2 = '%m-%d_%H:%M'
    deltatime = 8*3600
    
    lon = fo.variables['XLONG'][0,:]
    lat = fo.variables['XLAT'][0,:]
    #timelist = fo.variables['XTIME'][a] for a in len()
    #znu = fo.variables['ZNU'][:]
    
    
    #ph = fo.variables['PH'][:]
    #phb = fo.variables['PHB'][:]
    #hight = (ph + phb) / g
    #del ph,phb
    
    #T = fo.variables['T'][:]
    #T00 = fo.variables['T00'][:]
    
    #u_orig = U[:]
    #u = (u_orig[:,:,:,1:] + u_orig[:,:,:,:-1]) * 0.5
    #v_orig = fo.variables['V'][:]
    #v = (v_orig[:,:,1:,:] + v_orig[:,:,:-1,:]) * 0.5
    dbz = fo.variables['REFL_10CM'][:]
#        dbzm = fo.variables['REFD_MAX'][a,...]
    
    terrain = fo.variables['HGT'][0,:,:]
    
    #up_heli_max = fo.variables['UP_HELI_MAX'][:]
    for a in [0]: #np.arange(0,fo.dimensions['Time'].size):
        astr = timelist[a]
        timestr = time.strftime(fmt2,time.localtime(
                            time.mktime(time.strptime(astr,fmt))+deltatime  ))
              
        
        #%%
        level = 8
        #m = Basemap(width=1200000,height=900000,projection='lcc',
        #            resolution='c',lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)
        fig = plt.figure(figsize=(6,5))
#        plt.subplot(111)
        
        m = Basemap(width=1000000,height=666600,projection='lcc',
                llcrnrlon = 103.1419,llcrnrlat = 12.2463,urcrnrlon = 124.8581,urcrnrlat = 33.289,
                resolution='h',lat_1=22.,lat_2=26,lat_0=24.18,lon_0=112.55)
        
        #m.shadedrelief()
        m.drawcoastlines()
        m.drawcountries()
        #m.drawrivers()
        #m.drawcounties()
        parallels = np.arange(22,27,1.)
        m.drawparallels(parallels,labels=[1,0,0,0])
        # draw meridians
        meridians = np.arange(108.,118.,1.)
        m.drawmeridians(meridians,labels=[0,0,0,1])
    
        x,y = m(lon[0,...],lat[0,...])
        
#%%       
        
#        timenow = filepath[-8:-5]+'%02d' % int(timelist[time]%60)
        timenow = timestr
        temp = dbz[a,level,...].copy()
        pm = m.contourf(x,y,dbz[a,level,...],cmap=scmap,levels=range(10,76,5))
        
        plt.title('REF1km at '+timenow)
    
    
        
        # Now adding the colorbar
        #cbaxes = fig.add_axes([0.8, 0.1, 0.03, 0.8]) 
        #cb = plt.colorbar(ax1, cax = cbaxes)
        m.colorbar(mappable=pm)
        plt.tight_layout()
        
        plt.savefig(pathout+'/test_ref1km_'+timenow,dpi = 600)
        plt.show()
        plt.close()

#if __name__ == '__main__':
#      main()
#else:
#      pass