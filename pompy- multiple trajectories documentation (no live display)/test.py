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

class pig():
    def __init__(self,size):
        self.size = size
d={}
for x in range(10):
    d["lst{0}".format(x)] = []


for x in range(10):
    d["lst{}".format(x)].append(x)
    print d["lst{0}".format(x)]
#print d["pig9"].size


