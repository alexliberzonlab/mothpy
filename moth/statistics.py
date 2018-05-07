# -*- coding: utf-8 -*-
"""
A simple statistical analysis of the simulation
caculates average time as well as success precentage
"""

from __future__ import division

__authors__ = 'Noam Benelli'

def calc_stats(diff_dict):
    num_it= len(diff_dict)-1
    times_list = diff_dict["times_list"]

    #draw a histegram of different finishing times
    
    succuss_precentage = 100*len(times_list)/(num_it)
    if len(times_list) != 0:
        average_time = sum(times_list) / float(len(times_list))
    else:
        average_time =0

    return (succuss_precentage,average_time)



