#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 10:58:41 2017
先要做东西啊喂，程序再说吧。。。

@author: shiweisun
"""

import netCDF4 
import glob
import numpy as np
import matplotlib.pyplot as plt
import time

# path for input data
filepath = '/Users/shiweisun/data/case_split2nest/'

# filenames
filelist = glob.glob(filepath+'wrfout*')
filename = filelist[0]

fo = netCDF4.Dataset(filename,'r')
#%%
terrain = fo.variables['HGT'][:]
ph = fo.variables['PH'][:]

ph += fo.variables['PHB'][:]
#phb = fo.variables['PHB'][:]
#%
g=9.81
#ph_t = ph+phb
#ph_t = (ph_t[:,:-1,:,:]+ph_t[:,1:,:,:])/2
ph = (ph[:,:-1,:,:]+ph[:,1:,:,:])/2
#%
height_above_sea = ph/g
height_above_ground = height_above_sea - terrain.reshape([12,1,498,750])

def vorticity(u,v,map_factor_m,map_factor_u,map_factor_v):
    pass
#%%
msf_m = fo.variables['MAPFAC_M'][:]     #map_scale_factor
msf_m *= msf_m      # msf_m ^2
#msf_mx = fo.variables['MAPFAC_MX'][:]
#msf_my = fo.variables['MAPFAC_MY'][:]
msf_u = fo.variables['MAPFAC_U'][:]     # ncl only use this, not the x/y component
#msf_ux = fo.variables['MAPFAC_UX'][:]
#msf_uy = fo.variables['MAPFAC_UY'][:]
msf_v = fo.variables['MAPFAC_V'][:]
#msf_vx = fo.variables['MAPFAC_VX'][:]
#msf_vy = fo.variables['MAPFAC_VY'][:]
u_orig = fo.variables['U'][:]
v_orig = fo.variables['V'][:]
dx = fo.getncattr('DX')
dy = fo.getncattr('DY')

u_div_m = u_orig/msf_u.reshape([12,1,498,751])
v_div_m = v_orig/msf_v.reshape([12,1,499,750])

#%%

temp_i1 = u_div_m[:,:,:,:-1]    # i
temp_i2 = u_div_m[:,:,:,1:]     # i+1

#temp_i1j1 = np.zeros_like(temp_i1)    # i-1,j-1
#temp_i1j2 = np.zeros_like(temp_i1)    # i-1,j+1
#temp_i2j1 = np.zeros_like(temp_i1)    # i+1,j-1
#temp_i2j2 = np.zeros_like(temp_i1)    # i+1,j+1
#temp_i1j1[:,:,0,:] = temp_i1[:,:,0,:]
#temp_i1j1[:,:,1:,:] = temp_i1[:,:,:-1,:]
#temp_i1j2[:,:,-1,:] = temp_i1[:,:,-1,:]
#temp_i1j2[:,:,:-1,:] = temp_i1[:,:,1:,:]
#
#temp_i2j1[:,:,0,:] = temp_i2[:,:,0,:]
#temp_i2j1[:,:,1:,:] = temp_i2[:,:,:-1,:]
#temp_i2j2[:,:,-1,:] = temp_i2[:,:,-1,:]
#temp_i2j2[:,:,:-1,:] = temp_i2[:,:,1:,:]
#dudy = (temp_i1j2 + temp_i2j2 - temp_i1j1 - temp_i2j1)*0.5

dudy = ( np.concatenate((temp_i1[:,:,1:,:],temp_i1[:,:,-1,:].reshape([12,50,1,750])),axis = 2) \
    - np.concatenate((temp_i1[:,:,0,:].reshape([12,50,1,750]),temp_i1[:,:,:-1,:]),axis = 2) \
    + np.concatenate((temp_i2[:,:,1:,:],temp_i2[:,:,-1,:].reshape([12,50,1,750])),axis = 2) \
    - np.concatenate((temp_i2[:,:,0,:].reshape([12,50,1,750]),temp_i2[:,:,:-1,:]),axis = 2) )*0.5 
    # (i,j+1)-(i,j-1)+(i+1,j+1)-(i+1,j-1)
    
dys = dy / msf_m  * 2
dys[:,0,:] *= 0.5 
dys[:,-1,:] *= 0.5
dudy /= dys.reshape([12,1,498,750])

dxs = dx / msf_m 
dudx = (temp_i2 - temp_i1)/dxs.reshape([12,1,498,750])

#%
temp_i1 = v_div_m[:,:,:-1,:]    # consider i as j, so they're j and j+1
temp_i2 = v_div_m[:,:,1:,:]
dvdx = ( np.concatenate((temp_i1[:,:,:,1:],temp_i1[:,:,:,-1].reshape([12,50,498,1])),axis = 3) \
    - np.concatenate((temp_i1[:,:,:,0].reshape([12,50,498,1]),temp_i1[:,:,:,:-1]),axis = 3) \
    + np.concatenate((temp_i2[:,:,:,1:],temp_i2[:,:,:,-1].reshape([12,50,498,1])),axis = 3) \
    - np.concatenate((temp_i2[:,:,:,0].reshape([12,50,498,1]),temp_i2[:,:,:,:-1]),axis = 3) )*0.5 
    # (i+1,j)-(i-1,j)+(i+1,j+1)-(i-1,j+1)
    
dxs = dx / msf_m * 2
dxs[:,:,0] *= 0.5 
dxs[:,:,-1] *= 0.5
dvdx /= dxs.reshape([12,1,498,750])

dys = dy / msf_m 
dvdy = (temp_i2 - temp_i1)/dys.reshape([12,1,498,750])
vort = dvdx - dudy
div = dudx + dvdy
#%%
u = (u_orig[:,:,:,:-1]+u_orig[:,:,:,1:])*0.5
v = (v_orig[:,:,:-1,:]+v_orig[:,:,1:,:])*0.5


#%% vort
lon = fo.variables['XLONG'][:]
lat = fo.variables['XLAT'][:]
#at = [ fo.variables['Times'][a] for a in np.arange(0,fo.dimensions['Time'].size)]
#timelist = [''.join(at[a]) for a in np.arange(fo.dimensions['Time'].size)]
timelist = fo.variables['XTIME'][:]
skip = slice(None,None,3)
from mpl_toolkits.basemap import Basemap
for times in range(0,1):
    for level in range(0,1):
        #m = Basemap(width=1200000,height=900000,projection='lcc',
        #            resolution='c',lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)
        fig = plt.figure(figsize=(6,5))
        plt.subplot(111)
        m = Basemap(width=1000000,height=666600,projection='lcc',
                    llcrnrlon = 115.,llcrnrlat = 22.7,urcrnrlon = 117.,urcrnrlat = 24.2,
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
        
        
        
        timenow = filepath[-8:-5]+'%02d' % int(timelist[times]%60)
        temp = vort[times,level,...].copy()
        pm = m.contourf(x,y,vort[times,level,...],levels =list( np.arange(-7,8)*1e-3),cmap = 'PiYG')#,cmap=scmap,levels=range(10,76,5))
        
        plt.title('Vort at '+str(level) + 'level ' +timenow)
    
    
        
        # Now adding the colorbar
        #cbaxes = fig.add_axes([0.8, 0.1, 0.03, 0.8]) 
        #cb = plt.colorbar(ax1, cax = cbaxes)
        m.colorbar(mappable=pm)
        
#        # transform vectors to projection grid.
#        uproj,vproj,xx,yy = \
#        m.transform_vector(u,v,lon[0,0,:],lat[0,:,0],50,40,returnxy=True,masked=True)
#        # now plot.
#        Q = m.quiver(xx,yy,uproj,vproj,scale=700)
        Q = m.quiver(x[skip,skip],y[skip,skip],u[times,level,skip,skip],v[times,level,skip,skip],scale=700)
#        # make quiver key.
        qk = plt.quiverkey(Q, 0.1, 0.1, 20, '10 m/s', labelpos='W')
        
        
        
        
        plt.tight_layout()
        
        plt.savefig('/Users/shiweisun/pics/vort_'+ \
        '%02d'%level+'_'+timenow,dpi = 600)
        #plt.show()
        plt.close()
#%%
plt.figure()
plt.contourf(temp)
plt.colorbar()
plt.show()
