from __future__ import division

__authors__ = 'Noam Benelli'
from kalman import kalman_filter 
from moth_graphics import plot
from statistics import calc_stats
import json




with open('data.json') as data_file:
    dict_tuple = json.load(data_file) #dictionary tuple


#run the simulation - each navigator runs through the exact same condition
(diff_dict1,diff_dict2,diff_dict3,diff_dict4) = dict_tuple



    


stats1 = calc_stats(diff_dict1)
stats2 = calc_stats(diff_dict2)
stats3 = calc_stats(diff_dict3)
stats4 = calc_stats(diff_dict4)

import numpy as np
import matplotlib.pyplot as plt

x = [ '1','2', '3', '4']
y = [stats1[1], stats2[1], stats3[1],stats4[1]] #average time

width = 0.6
plt.bar(x, y, width, color="blue")
plt.xlabel("Casting type")
plt.ylabel("Average time")
plt.title("Casting - time")
fig = plt.gcf()
plt.show()


x = [ '1','2', '3', '4']
y = [stats1[0], stats2[0], stats3[0],stats4[0]] #success precentage

plt.bar(x, y, width, color="blue")
plt.xlabel("Casting type")
plt.ylabel("success precentage")
plt.title("Casting - success")
fig = plt.gcf()
plt.show()
plt.close()



