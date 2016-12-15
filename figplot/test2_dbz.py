#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 15:45:57 2016
tempfile to draw dbz


@author: shiweisun
"""
import numpy as np
import netCDF4 
import time
import glob
import matplotlib.pyplot as plt
import matplotlib.colors as pltc
import scipy.io as sio
chinamap = sio.loadmat('/Users/shiweisun/scripts/china.province.delHK.mat')

filepath = '/Users/shiweisun/data/case_split2nest/'
filelist = glob.glob(filepath+'wrfout*')
pathout = '/Users/shiweisun/pics/'
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
scmap = pltc.ListedColormap(sswcmap,name='radarcolor')


#%%

for filename in filelist :
    print filename

#filename = 'wrfout_d03_2016-04-12_20:05:00'

    fo = netCDF4.Dataset(filename,'r') 
    
    #%%
    dx = fo.DX
    at = [ fo.variables['Times'][a] for a in np.arange(0,fo.dimensions['Time'].size)]
    timelist = [''.join(at[a]) for a in np.arange(fo.dimensions['Time'].size)]
    fmt = '%Y-%m-%d_%H:%M:%S'            
    fmt2 = '%m-%d %H:%M'
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
    
    #U = fo.variables['U']
    #u_orig = U[:]
    #u = (u_orig[:,:,:,1:] + u_orig[:,:,:,:-1]) * 0.5
    #v_orig = fo.variables['V'][:]
    #v = (v_orig[:,:,1:,:] + v_orig[:,:,:-1,:]) * 0.5
    dbz = fo.variables['REFL_10CM'][:]
#        dbzm = fo.variables['REFD_MAX'][a,...]
    
    terrain = fo.variables['HGT'][0,:,:]
    
    #up_heli_max = fo.variables['UP_HELI_MAX'][:]
    for a in np.arange(0,fo.dimensions['Time'].size):
        astr = timelist[a]
        timestr = time.strftime(fmt2,time.localtime(
                            time.mktime(time.strptime(astr,fmt))+deltatime  ))
              
        
        #%%
        level = 8
        fig = plt.figure(figsize=(6,5))
        plt.subplot(111)
        plt.axes(aspect = 1)
#        plt.axis('equal')
        plt.axis([104.5,121.1,16,28])
        pp = plt.plot(chinamap['long'].squeeze(),chinamap['lat'].squeeze(),color = 'black')

        timenow = timestr
        temp = dbz[a,level,...].copy()
        pm = plt.contourf(lon,lat,temp,cmap=scmap,levels=range(10,76,5))
        
        plt.title('REF1km at '+timenow,size = 24)
    
    
    
        # Now adding the colorbar
        cbaxes = fig.add_axes([0.925, 0.12, 0.035, 0.3]) 
        cb = plt.colorbar(pm, cax = cbaxes)
        cb.ax.yaxis.set_ticks_position('left')
#        plt.colorbar(mappable=pm)
        
        #%

        plt.tight_layout()
        
        plt.savefig(pathout+'ref1km_'+timenow,dpi = 600)
#        plt.show()
        plt.close()

#if __name__ == '__main__':
#      main()
#else:
#      pass