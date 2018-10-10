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

    #calculate the average time of flight for successful flights
    if len(times_list) != 0:
        average_time = sum(times_list) / float(len(times_list))
    else:
        average_time =0

    #calculate the ratio of time in which odor was detected/all of the flight time
    search_efficincy_list = []
    for j in ????: #itirate through navigators
        Last_dt_odor = False
        T_odor = 0
        T_no_odor = 0
        for i in range(num_it): #itirate within list 
            odor = diff_dict["diff_list{0}".format(j)][i][3] #odor found or odor lost
            if odor == None and Last_dt_odor :
                T_odor +=1
            elif odor =='odor found':
                T_odor += 1
                Last_dt_odor = True
            elif odor == 'odor lost':
                Last_dt_odor = False

        search_efficiency = T_odor/len(diff_dict["diff_list{0}".format(j)])
        search_efficincy_list.append(search_efficiency)
    return (succuss_precentage,average_time)



