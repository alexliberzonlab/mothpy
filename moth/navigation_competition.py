from __future__ import division

__authors__ = 'Noam Benelli'
from simulation_nav import moth_simulation
from kalman import kalman_filter 
from moth_graphics import plot
from statistics import calc_stats


num_it = 10 #number of iterations
(diff_dict1,diff_dict2,diff_dict3,diff_dict4) = moth_simulation(num_it,1)


stats1 = calc_stats(diff_dict1)
stats2 = calc_stats(diff_dict2)
stats3 = calc_stats(diff_dict3)
stats4 = calc_stats(diff_dict4)

import numpy as np
import matplotlib.pyplot as plt

x = [ '1','2', '3', '4']
y = [stats1[1], stats2[1], stats3[1],stats4[1]]

width = 0.6
plt.bar(x, y, width, color="blue")
plt.xlabel("navigating type")
plt.ylabel("Average time")
plt.title("navigating - time")
fig = plt.gcf()
plt.show()


x = [ '1','2', '3', '4']
y = [stats1[0], stats2[0], stats3[0],stats4[0]] #success precentage
width = 0.6
plt.bar(x, y, width, color="blue")
plt.xlabel("navigating type")
plt.ylabel("success precentage")
plt.title("navigating - success precentage")
fig = plt.gcf()
plt.show()





