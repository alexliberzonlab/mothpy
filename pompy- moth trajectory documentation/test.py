# -*- coding: utf-8 -*-
"""
Demonstrations of how to set up models with graphical displays produced using
matplotlib functions.


from __future__ import division

__authors__ = 'Matt Graham'
__license__ = 'MIT'

"""
import sys
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import processors
"""

z = np.zeros((1000,1000))
o = 250*np.ones((500,500))
for i in range(200):
    for j in range(200):
        o[500+i][500+j]=i/2+j/2

if True:
    moth_array=np.zeros((500,500))
    for i in range(10):
       for j in range(10):
           moth_array[255-i][499-j]=3e4
plt.figure()
plt.imshow(moth_array, cmap=plt.cm.gray, vmin=0, vmax=3e4)
plt.show()


moth_array=np.zeros((500,500))
print moth_array[245.0][250.0]

plt.figure()
plt.imshow(moth_array, cmap=plt.cm.gray, vmin=0, vmax=3e4)
plt.show()

print int(np.sqrt(168))
"""
print not not True
