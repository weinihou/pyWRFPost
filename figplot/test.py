# -*- coding: utf-8 -*-
'''
Some temporare plots
dBZ Vorticity
用 basemap
时间操作还未熟练
'''


from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
#%%
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


#%% dbz
for time in range(0,12):    #当时还未找到替换时间的方法
    level = 10
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
    
    
    
    timenow = filepath[-8:-5]+'%02d' % int(timelist[time]%60)
    temp = dbz[time,level,...].copy()
    pm = m.contourf(x,y,dbz[time,level,...],cmap=scmap,levels=range(10,76,5))
    
    plt.title('REF1km at '+timenow)


    
    # Now adding the colorbar
    #cbaxes = fig.add_axes([0.8, 0.1, 0.03, 0.8]) 
    #cb = plt.colorbar(ax1, cax = cbaxes)
    m.colorbar(mappable=pm)
    plt.tight_layout()
    
    plt.savefig('/Users/shiweisun/scripts/pythonscripts/pyWRFPost/figplot/sm_ref1km_'+timenow,dpi = 600)
    #plt.show()
    plt.close()
    
    #m.readshapefile
    
#%% vort
for time in range(0,12):
    for level in range(0,6):
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
        
        
        
        timenow = filepath[-8:-5]+'%02d' % int(timelist[time]%60)
        temp = dbz[time,level,...].copy()
        pm = m.contourf(x,y,vort[time,level,...],levels =list( np.arange(-7,8)*1e-3),cmap = 'PiYG')#,cmap=scmap,levels=range(10,76,5))
        
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
#        # make quiver key.
#        qk = plt.quiverkey(Q, 0.1, 0.1, 20, '10 m/s', labelpos='W')
        
        
        
        
        plt.tight_layout()
        
        plt.savefig('/Users/shiweisun/scripts/pythonscripts/pyWRFPost/figplot/vort_'+ \
        '%02d'%level+'_'+timenow,dpi = 600)
        #plt.show()
        plt.close()




#%%
timest = '2016-04-12-12:00'


