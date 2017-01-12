#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 00:22:52 2017

Test the scipy interp2d.

The results will be different depends on the format that the input data is.

When given the short, un-meshgrid array x and y, you will get the normal answer
of bilinear interpolation. But when you give the all x and y, the function will
think you're putting irregular grid data, and so the results are different.

@author: shiweisun
"""
import matplotlib
matplotlib.use('QT5agg')
import numpy as np
from scipy import interpolate as itp
import matplotlib.pyplot as plt
pathout = '/Users/shiweisun/pics/'
a = np.array([[0, 1, 2, 3],
              [0, 0, 1, 2],
              [0, 0, 0, 1]])
x = np.array([[0, 1, 2, 3],
              [0, 1, 2, 3],
              [0, 1, 2, 3]])
y = np.array([[2, 2, 2, 2],
              [1, 1, 1, 1],
              [0, 0, 0, 0]])
#a = np.array([[0, 1, 2, 3],
#              [0, 0, 1, 2]])
#x = np.array([[0, 1, 2, 3],
#           [0, 1, 2, 3]])
#y = np.array([[1, 1, 1, 1],
#              [0, 0, 0, 0]])
temp = itp.interp2d(x,y,a,kind='linear')
xx = [0,1,2,3]
yy = [2,1,0]
temp2 = itp.interp2d(xx,yy,a,kind='linear')
xxx=np.linspace(0,3,50)
yyy=np.linspace(2,0,50)
a1 = temp(xxx,yyy)
a2 = temp2(xxx,yyy)

plt.figure(figsize=(8,4))
plt.subplot(121)
plt.contourf(xxx,yyy,a1)
plt.title('as irregular grids')
plt.subplot(122)
plt.contourf(xxx,yyy,a2)
plt.title('as regular grids')

# plt.savefig(pathout+'/interp2d',dpi = 600,bbox_inches='tight')
plt.show()
# plt.close()
