#==============================================================================
# Load the original variables from wrfout files.
#==============================================================================
'''
This is the first step of WRF post processing.

All the variables here are just in the output files directly, so we just open 
the files and get the vars.

'''
import numpy as np
import netCDF4 
#from . import constants     # can only do when this file is imported
g = 9.81
#%%
filepath = '/Users/shiweisun/data/case_split2nest/wrfout_d03_2016-04-12_20:05:00'
fo = netCDF4.Dataset(filepath,'r') 
    
U = fo.variables['U']
#%%
dx = fo.DX


lon = fo.variables['XLONG'][:]
lat = fo.variables['XLAT'][:]
timelist = fo.variables['XTIME'][:]
znu = fo.variables['ZNU'][:]


ph = fo.variables['PH'][:]
phb = fo.variables['PHB'][:]
hight = (ph + phb) / g
del ph,phb

T = fo.variables['T'][:]
T00 = fo.variables['T00'][:]

u_orig = U[:]
u = (u_orig[:,:,:,1:] + u_orig[:,:,:,:-1]) * 0.5
v_orig = fo.variables['V'][:]
v = (v_orig[:,:,1:,:] + v_orig[:,:,:-1,:]) * 0.5
dbz = fo.variables['REFL_10CM'][:]
dbzm = fo.variables['REFD_MAX'][:]

terrain = fo.variables['HGT'][0,:,:]

up_heli_max = fo.variables['UP_HELI_MAX'][:]

#%%
def compute_derivatives(U,V,axis=None):
        dargs = (dx,dx)
        dkwargs = {'axis':None}
        if len(U.shape) == 2:
            dudx, dudy = np.gradient(U,dx,dx)
            dvdx, dvdy = np.gradient(V,dx,dx)
        elif len(U.shape) == 3:
            nt = U.shape[0]
            dudx = np.zeros_like(U)
            dvdx = np.zeros_like(U)
            dudy = np.zeros_like(U)
            dvdy = np.zeros_like(U)
            for t in range(nt):
                dudx[t,...], dudy[t,...] = np.gradient(U[t,...],dx,dx)
                dvdx[t,...], dvdy[t,...] = np.gradient(V[t,...],dx,dx)
        elif len(U.shape) == 4:
            nt = U.shape[0]
            nz = U.shape[1]
            dudx = np.zeros_like(U)
            dvdx = np.zeros_like(U)
            dudy = np.zeros_like(U)
            dvdy = np.zeros_like(U)
            for t in range(nt):
                for z in range(nz):
                    dudx[t,z,...], dudy[t,z,...] = np.gradient(U[t,z,...],dx,dx)
                    dvdx[t,z,...], dvdy[t,z,...] = np.gradient(V[t,z,...],dx,dx)
        return dudx, dudy, dvdx, dvdy

def compute_vorticity(U,V):
        # Axis = 1 for vertical vorticity, if there's no time selected?
        dudx, dudy, dvdx, dvdy = compute_derivatives(U,V,)#axis=1)
        zeta = dvdx - dudy
        return zeta

vort = compute_vorticity(u,v)




#if __name__ == '__main__':
#      
#else:
#      pass