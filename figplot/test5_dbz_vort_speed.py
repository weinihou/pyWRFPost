#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 10:37:33 2016
Using basemap, adjust the region by reading the nc file (wrfout)
Using china.province... map data
dBZ in gray contourf
vort in contour
speed(lowest level) in contour


@author: shiweisun
"""
# if do not need to show the pics, or can not open the interactive backends
import matplotlib
#matplotlib.use('Agg')
import numpy as np
import netCDF4 
import time
import glob
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
#import matplotlib.cm as cm
#from . import constants     # can only do when this file is imported
#g = 9.81

# load the map of provinces of China
import scipy.io as sio
chinamap = sio.loadmat('/Users/shiweisun/scripts/china.province.delHK.mat')

# units(in degrees) of the parallels and meridians of the map 
deg_unit = 2.

# out path for pictures
pathout = '/Users/shiweisun/pics/'

# path for input data
filepath = '/Users/shiweisun/data/case_split2nest/'

# filenames
filelist = glob.glob(filepath+'wrfout*')
import matplotlib.colors as pltc

# radar colormap for dBZ in www.nmc.cn, from 10 to 75, 13 objects
sswcmap = [[ 0.00392157,  0.62745098,  0.96470588],
           [ 0.        ,  0.9254902 ,  0.9254902 ],
           [ 0.        ,  0.84705882,  0.        ],
           [ 0.00392157,  0.56470588,  0.        ],
           [ 1.        ,  1.        ,  0.        ],
           [ 0.90588235,  0.75294118,  0.        ],
           [ 1.        ,  0.56470588,  0.        ],
           [ 1.        ,  0.        ,  0.        ],
           [ 0.83921569,  0.        ,  0.        ],
           [ 0.75294118,  0.        ,  0.        ],
           [ 1.        ,  0.        ,  0.94117647],
           [ 0.58823529,  0.        ,  0.70588235],
           [ 0.67843137,  0.56470588,  0.94117647]]

scmap = pltc.ListedColormap(sswcmap,name='radarcolor')



for filename in filelist :
    print filename

    fo = netCDF4.Dataset(filename,'r')     
    #%%
    dx = fo.getncattr('DX')
    dy = fo.getncattr('DY')
    
#    cenlat = fo.getncattr('CEN_LAT')    #for nest
#    cenlon = fo.getncattr('CEN_LON')    #for nest
    cenlon = fo.getncattr('STAND_LON')  #for whole region
    cenlat = fo.getncattr('MOAD_CEN_LAT')   #for whole region
    lat1   = fo.getncattr('TRUELAT1')
    lat2   = fo.getncattr('TRUELAT2')
    grid_w2e = fo.getncattr('WEST-EAST_GRID_DIMENSION')
    grid_s2n = fo.getncattr('SOUTH-NORTH_GRID_DIMENSION')

    map_proj = fo.MAP_PROJ_CHAR
    
    proj_list = {'Lambert Conformal':'lcc'}
    temp = [ fo.variables['Times'][a] for a in np.arange(0,fo.dimensions['Time'].size)]
    timelist = [''.join(temp[a]) for a in np.arange(fo.dimensions['Time'].size)]
    fmt = '%Y-%m-%d_%H:%M:%S'            
    fmt2 = '%Y%m%d%H%M'
    deltatime = 8*3600
    
    lon = fo.variables['XLONG'][0,:]
    lat = fo.variables['XLAT'][0,:]
    #timelist = fo.variables['XTIME'][a] for a in len()
    #znu = fo.variables['ZNU'][:]
    
    #%
#    ph = fo.variables['PH'][:]
#    phb = fo.variables['PHB'][:]
#    hight = (ph + phb) / g
    #del ph,phb
    #%
    #T = fo.variables['T'][:]
    #T00 = fo.variables['T00'][:]
    
    u_orig = fo.variables['U'][:]
    u = (u_orig[:,:,:,1:] + u_orig[:,:,:,:-1]) * 0.5
    v_orig = fo.variables['V'][:]
    v = (v_orig[:,:,1:,:] + v_orig[:,:,:-1,:]) * 0.5
    u = np.float64(u)
    v = np.float64(v)
    speed_lowest = (u[:,0,:,:]*u[:,0,:,:] + v[:,0,:,:]*v[:,0,:,:]) ** 0.5
    
    dudx = np.zeros_like(u)
    dudy = np.zeros_like(u)
    dvdx = np.zeros_like(u)
    dvdy = np.zeros_like(u)
    for t in range(u.shape[0]):
        for z in range(u.shape[1]):
            dudx[t,z,...], dudy[t,z,...] = np.gradient(u[t,z,...],dx,dy)
            dvdx[t,z,...], dvdy[t,z,...] = np.gradient(v[t,z,...],dx,dy)
    vort = dvdx - dudy
    #
    
    del u,v,u_orig,v_orig,dudx,dudy,dvdx,dvdy
    dbz = fo.variables['REFL_10CM'][:]
#        dbzm = fo.variables['REFD_MAX'][a,...]
    
    terrain = fo.variables['HGT'][0,:,:]
    
    #up_heli_max = fo.variables['UP_HELI_MAX'][:]
    for a in [0]: #np.arange(0,fo.dimensions['Time'].size):
        astr = timelist[a]
              
        #%%
        level = 8
        
        matplotlib.rcParams['contour.negative_linestyle'] = 'dashed'
        fig = plt.figure(figsize=(6,5))
#        ax = fig.add_axes([0.1,0.1,0.8,0.8])
#        ax = fig.add_subplot(111)
#        ax.tick_params(labelsize = 5)
#        plt.subplot(111)
        #%
        m = Basemap(projection = proj_list[map_proj],resolution = 'i',
                    lon_0 = cenlon,lat_0 = cenlat,
                    lat_1 = lat1,lat_2 = lat2,
                    #width = grid_w2e * dx, height = grid_s2n * dy
                    llcrnrlon = lon[0,0],llcrnrlat = lat[0,0],
                    urcrnrlon = lon[lon.shape[0]-1,lon.shape[1]-1],
                    urcrnrlat = lat[lat.shape[0]-1,lat.shape[1]-1],
                    ) 
#        m.drawcoastlines()
#        m.drawcountries()
        parallels = np.arange(np.floor(lat.min()),np.ceil(lat.max()),deg_unit)
        m.drawparallels(parallels,labels=[1,0,0,0])
        meridians = np.arange(np.floor(lon.min()),np.ceil(lon.max()),deg_unit)
        m.drawmeridians(meridians,labels=[0,0,0,1])
#        ax = plt.gca()
#        ax.tick_params(labelsize = 24)
#        for ttt in (ax.get_yticklabels()+ax.get_yticklabels()):
#            ttt.set_fontsize(20)
        
        # m() will convert the longitudes and latitudes (deg) to x,y (m), 
        #    but numpy.nan will be transformed to about 1e30
        temp1,temp2 = m(chinamap['long'].squeeze(),chinamap['lat'].squeeze())
        temp1[temp1>1e28]=np.nan
        temp2[temp2>1e28]=np.nan
        
        m.plot(temp1,temp2,color='blue')
        temp = dbz[a,level,...].copy()
        x,y = m(lon,lat)
        pm = plt.contourf(x,y,dbz[a,level,...],cmap='gray_r',
                          levels=range(35,61,5),extend='max')
#        plt.clim(40,55)
        
        timebjt = time.strftime(fmt2,time.localtime(
                            time.mktime(time.strptime(astr,fmt))+deltatime  ))
        timeutc = time.strftime(fmt2,time.localtime(
                            time.mktime(time.strptime(astr,fmt)) ))
        plt.title('REF1km  '+timeutc+'UTC  '+timebjt+'BJT')
#        plt.tick_params(labelsize = 5)

        # Now adding the colorbar        
#        cbaxes = fig.add_axes([0.925, 0.12, 0.035, 0.3]) 
#        cb = plt.colorbar(pm, cax = cbaxes)
#        cb.ax.yaxis.set_ticks_position('left')
        
        m.colorbar(mappable=pm,size='2%')
        
        plt.contour(x,y,speed_lowest[a,...],levels=[16],colors='r')
        plt.contour(x,y,vort[a,5,:,:],levels=[-4e-3,4e-3],colors='y')
        
#        plt.tight_layout()
        #%
        
        temp = filename[filename.index('wrfout_d')+7:filename.index('wrfout_d')+11]
        temp = pathout + '/ref_vort_V_'+temp+timeutc
        plt.savefig(temp,dpi = 600,bbox_inches='tight')
#        fig.show()
        plt.close()
        
        


#if __name__ == '__main__':
#      main()
#else:
#      pass