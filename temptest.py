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
from scipy import interpolate as itp

# path for input data
filepath = '/Users/shiweisun/data/case_split2nest/'

# filenames
filelist = glob.glob(filepath+'wrfout*')
filename = filelist[0]

# out path for pictures
pathout = '/Users/shiweisun/pics/'


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

# load the map of provinces of China
import scipy.io as sio
chinamap = sio.loadmat('/Users/shiweisun/scripts/china.province.delHK.mat')

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

#%%
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
dbz = fo.variables['REFL_10CM'][:]
w = fo.variables['W'][:]
w = (w[:,1:,:,:]+w[:,:-1,:,:])*0.5

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
#timelist = fo.variables['XTIME'][:]
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
u_sys = 26.6667
v_sys = -6.8889

u_related = u-u_sys     # system related velocity
v_related = v-v_sys
#%%
sliceA = [116,23.5]
sliceB = [116.2,23.35]

slicelin_x = np.linspace(sliceA[0],sliceB[0],20)
slicelin_y = np.linspace(sliceA[1],sliceB[1],20)
skip = slice(None,None,1)
from mpl_toolkits.basemap import Basemap
for times in range(0,1):
    astr = timelist[times]
    for level in range(0,1):
        #m = Basemap(width=1200000,height=900000,projection='lcc',
        #            resolution='c',lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)
        fig = plt.figure(figsize=(7,5))
        plt.subplot(111)
#        m = Basemap(width=1000000,height=666600,projection='lcc',
#                    llcrnrlon = 115.,llcrnrlat = 22.7,urcrnrlon = 117.,urcrnrlat = 24.2,
#                    resolution='h',lat_1=22.,lat_2=26,lat_0=24.18,lon_0=112.55)
        
        m = Basemap(projection = proj_list[map_proj],resolution = 'i',
                    lon_0 = cenlon,lat_0 = cenlat,
                    lat_1 = lat1,lat_2 = lat2,
#                    llcrnrlon = 115.3,llcrnrlat = 22.9,urcrnrlon = 116.5,urcrnrlat = 23.85
                    llcrnrlon = 115.8,llcrnrlat = 23.1,urcrnrlon = 116.3,urcrnrlat = 23.6
                    #width = grid_w2e * dx, height = grid_s2n * dy
#                    llcrnrlon = lon[0,0],llcrnrlat = lat[0,0],
#                    urcrnrlon = lon[lon.shape[0]-1,lon.shape[1]-1],
#                    urcrnrlat = lat[lat.shape[0]-1,lat.shape[1]-1],
                    )
        #m.shadedrelief()
        m.drawcoastlines()
        m.drawcountries()
        #m.drawrivers()
        #m.drawcounties()
        parallels = np.arange(22,27,0.5)
        m.drawparallels(parallels,labels=[1,0,0,0])
        # draw meridians
        meridians = np.arange(108.,118.,0.5)
        m.drawmeridians(meridians,labels=[0,0,0,1])
        # draw China map
        temp1,temp2 = m(chinamap['long'].squeeze(),chinamap['lat'].squeeze())
        temp1[temp1>1e28]=np.nan
        temp2[temp2>1e28]=np.nan
        m.plot(temp1,temp2,color='k',linewidth=0.5)
        
        
        x,y = m(lon[0,...],lat[0,...])
        xlist = x[0,:]
        ylist = y[:,0]
        
        #%
        
        temp = w[times,level,...].copy()
#        temp = dbz[times,8,...].copy()
        pm = m.contourf(x,y,temp,
#                        levels =list( np.arange(-7,8)*1e-3),
#                        levels =list( np.arange(-7,8)*1e-3),
#                        cmap = 'gray_r',
#                        cmap=scmap,
                        cmap='PiYG',
                        extend='max',)
#                        levels=range(10,76,5))#,cmap=scmap,levels=range(10,76,5))
        
        timebjt = time.strftime(fmt2,time.localtime(
                            time.mktime(time.strptime(astr,fmt))+deltatime  ))
        timeutc = time.strftime(fmt2,time.localtime(
                            time.mktime(time.strptime(astr,fmt)) ))
        plt.title(timeutc+'UTC  '+timebjt+'BJT   w at 1km')#Vort at '+str(level) + 'level')
    
        
        # Now adding the colorbar
        #cbaxes = fig.add_axes([0.8, 0.1, 0.03, 0.8]) 
        #cb = plt.colorbar(ax1, cax = cbaxes)
        m.colorbar(mappable=pm,size='2%')
        
#        # transform vectors to projection grid.
#        uproj,vproj,xx,yy = \
#        m.transform_vector(u,v,lon[0,0,:],lat[0,:,0],50,40,returnxy=True,masked=True)
#        # now plot.
#        Q = m.quiver(xx,yy,uproj,vproj,scale=700)
        Q = m.quiver(x[skip,skip],y[skip,skip],u_related[times,8,skip,skip],v_related[times,level,skip,skip],scale=1000)
#        # make quiver key.
        qk = plt.quiverkey(Q, 0.1, 0.1, 20, '10 m/s', labelpos='W')
        
        # draw the slice location
        slicelin_x,slicelin_y = m(slicelin_x,slicelin_y)
        m.plot([slicelin_x[0],slicelin_x[-1]],[slicelin_y[0],slicelin_y[-1]],color='k',linewidth=1.5)
        
        
        temp = filename[filename.index('wrfout_d')+7:filename.index('wrfout_d')+11]
        temp = pathout + '/sm_w'+temp+timeutc+'_lev_'+str(level)
        plt.savefig(temp,dpi = 600,bbox_inches='tight')
        
        #plt.show()
        plt.close()
#%%
#plt.figure()
#plt.contourf(temp)
#plt.colorbar()
#plt.show()

#%% interp to z levels
zlist = np.concatenate((np.arange(100,1005,100),np.arange(1000,7205,150)),axis = 0)

times = 0
vrbl = vort[times,...]
def interp_z_test(vrbl):
    pass
    #%
    vrbl_new = np.zeros([zlist.shape[0],vrbl.shape[1],vrbl.shape[2]])
    for i in range(height_above_ground.shape[2]):
        for j in range(height_above_ground.shape[3]):
    #        h0 = 
    #        vrbl_0 = 
            vrbl_new[:,i,j] = np.interp(zlist,height_above_sea[times,:,i,j],vrbl[:,i,j])
    return vrbl_new

def get_slice(vrbl_new):
    for i in range(vrbl_new.shape[0]):
        func = itp.interp2d(x,y,vrbl_new[i,:,:])
        vrbl_slice = [func(slicelin_x[a],slicelin_y[a]) for a in len(slicelin_x)]
    return vrbl_slice

#%%
vrbl_new = interp_z_test(vrbl)
temp = get_slice(vrbl_new)



#%% test plot to see the interpolation
plt.figure()
plt.plot(vrbl[:,5,5],height_above_sea[times,:,5,5],'k')
plt.plot(vrbl_new[:,5,5],zlist,'b')
plt.ylim(0,7000)


#%%
                     






