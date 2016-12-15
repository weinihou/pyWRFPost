#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Draw China map through .mat file


Created on Wed Dec 14 10:45:54 2016

@author: shiweisun
"""

import scipy.io as sio
import matplotlib.pylab as plt
import numpy as np

chinamap = sio.loadmat('/Users/shiweisun/scripts/china.province.delHK.mat')
#%%
plt.figure()
lon = chinamap['long'].squeeze()
lat = chinamap['lat'].squeeze()
plt.plot(lon,lat)
#chinamap['long']
#plt.xlim(50,130)
#plt.ylim(20,70)

plt.show()


