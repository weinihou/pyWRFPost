#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 15:45:57 2016
tempfile to draw dbz


@author: shiweisun
"""
import matplotlib
matplotlib.use('Agg')
import numpy as np
import netCDF4 
import time
import glob
import matplotlib.pyplot as plt
import matplotlib.colors as pltc
import scipy.io as sio
chinamap = sio.loadmat('/data/data3/swsun/scripts/china.province.delHK.mat')
#
filepath = '/gpfs1/swsun/WRF_run/CASE_2_Thompson_RRTMG_ACM2/wrfdata/'
filelist = glob.glob(filepath+'wrfout_d03*')
pathout = '/data/data3/swsun/wrf_ref/133_2nest/'

#chinamap = sio.loadmat('/Users/shiweisun/scripts/china.province.delHK.mat')

#filepath = '/Users/shiweisun/data/case_split2nest/'
#filelist = glob.glob(filepath+'wrfout_d03*')
#pathout = '/Users/shiweisun/pics/'
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
xlim = np.array([[106,108],   #10:00
                 [106,109],
                 [106,109],
                 [107,109.3],
                 [107.5,110],
                 [108,110],
                 [109,112],
                 [110.5,115],
                 [112,116],
                 [112,117.5],
                 [113,119],
                 [114,120]])    #8:00
ylim = np.array([[27,28],
                 [26,28],
                 [26,28],
                 [25,28],
                 [24.5,27],  #18:00
                 [24,27],
                 [24,26],
                 [23,25],
                 [22.8,25],
                 [22,25],
                 [22,25.5],
                 [21.8,25]])    #8:00

flag = 0  #count the time

level = 8
fig = plt.figure(figsize=(8,5))
plt.subplot(111)
plt.axes(aspect = 1)
#        plt.axis('equal')
plt.axis([108,117.2,22.2,25.7])
pp = plt.plot(chinamap['long'].squeeze(),chinamap['lat'].squeeze(),color = 'blue',linewidth=0.5)

filelist.reverse()
flag = 0
for filename in filelist :
    print filename

#filename = 'wrfout_d03_2016-04-12_20:05:00'

    fo = netCDF4.Dataset(filename,'r') 
    
    #%%
    dx = fo.DX
    temp = [ fo.variables['Times'][a] for a in np.arange(0,fo.dimensions['Time'].size)]
    timelist = [''.join(temp[a]) for a in np.arange(fo.dimensions['Time'].size)]
    fmt = '%Y-%m-%d_%H:%M:%S'            
    fmt2 = '%m-%d %H:%M'
    deltatime = 8*3600
    
    timelim1 = time.mktime(time.strptime('2016-04-12_20:00:00',fmt))
    timelim2 = time.mktime(time.strptime('2016-04-13_05:00:00',fmt))
    
    
    lon = fo.variables['XLONG'][0,:]
    lat = fo.variables['XLAT'][0,:]
   
    u_orig = fo.variables['U'][:]
    u = (u_orig[:,:,:,1:] + u_orig[:,:,:,:-1]) * 0.5
    v_orig = fo.variables['V'][:]
    v = (v_orig[:,:,1:,:] + v_orig[:,:,:-1,:]) * 0.5
    u = np.float64(u)
    v = np.float64(v)
    speed_lowest = (u[:,0,:,:]*u[:,0,:,:] + v[:,0,:,:]*v[:,0,:,:]) ** 0.5
    dbz = fo.variables['REFL_10CM'][:]
#        dbzm = fo.variables['REFD_MAX'][a,...]
    
    terrain = fo.variables['HGT'][0,:,:]
    # fo.close()
    if flag == 0 :
        fnl_dbz = np.zeros_like(dbz[0,0,...])
        fnl_spd = np.zeros_like(speed_lowest[0,...])
        flag +=1
    
    for a in np.arange(0,fo.dimensions['Time'].size):
        astr = timelist[a]
        timenow = time.mktime(time.strptime(astr,fmt))+deltatime
        if (timenow < timelim1) | (timenow > timelim2):
        
            continue
        fnl_spd = np.where(fnl_spd>speed_lowest[a,...],fnl_spd,speed_lowest[a,...])
         
        
        if timenow%3600 == 0:
        
        #        lonlim = xlim[flag,:]
        #        latlim = ylim[flag,:]
        #        temlon = np.logical_and.reduce([ lon >= lonlim[0] , lon <= lonlim[1] ,
        #                                        lat>=latlim[0] , lat <= latlim[1] ])
            temp = dbz[a,level,...].copy()
            fnl_dbz = np.where(fnl_dbz>temp,fnl_dbz,temp)
            #        temp[np.logical_not(temlon)] = 0
            
pm = plt.contourf(lon,lat,fnl_dbz,cmap='gray_r',levels=range(45,61,5),
                  extend='max')
    #        plt.clim(40,55)
    #        flag += 1
    
    	#plt.contour(lon,lat,speed_lowest[a,...],levels=[17],colors='r',linewidths=0.5)
pm2 = plt.contourf(lon,lat,fnl_spd,levels=np.arange(15,20,0.5),cmap='Reds',
			extend='max')

    #up_heli_max = fo.variables['UP_HELI_MAX'][:]
#    for a in np.arange(0,fo.dimensions['Time'].size):
#        astr = timelist[a]
#        timestr = time.strftime(fmt2,time.localtime(
#                            time.mktime(time.strptime(astr,fmt))+deltatime  ))
#              
#        
        #%%


#%%    
plt.title('REF1km windspeed swath ',size = 18)



# Now adding the colorbar
#cbaxes = fig.add_axes([0.925, 0.32, 0.035, 0.3]) 
cb = plt.colorbar(pm,orientation='vertical') # cax = cbaxes)
plt.colorbar(pm2,orientation='horizontal')
#cb.ax.yaxis.set_ticks_position('left')
#        plt.colorbar(mappable=pm)

#%

#plt.tight_layout()

plt.savefig(pathout+'ref_wind_swath',dpi = 600,bbox_inches='tight')
#        plt.show()
plt.close()

#if __name__ == '__main__':
#      main()
#else:
#      pass
