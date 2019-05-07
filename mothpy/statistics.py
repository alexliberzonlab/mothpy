# -*- coding: utf-8 -*-
"""
A simple statistical analysis of the simulation
caculates average time as well as success precentage
"""

from __future__ import division
import math
import json
__authors__ = 'Noam Benelli'



def search_efficiency(diff_dict):
    #calculate the ratio of time in which odor was detected/all of the flight time
    search_efficincy_list = []
    num_it= len(diff_dict)
    for j in range(num_it): #itirate through navigators
        Last_dt_odor = False
        T_odor = 0
        T_no_odor = 0
        for i in range(num_it): #itirate within list 
            odor = diff_dict["diff_list{0}".format(j)][i][3] #odor found or odor lost
            if odor == None and Last_dt_odor :
                T_odor += 1
            elif odor =='odor found':
                T_odor += 1
                Last_dt_odor = True
            elif odor == 'odor lost':
                Last_dt_odor = False

        search_eff = T_odor/len(diff_dict["diff_list{0}".format(j)])
        print search_eff
        search_efficincy_list.append(search_eff)
    print search_efficincy_list
    average = math.fsum(search_efficincy_list) / len(search_efficincy_list)
    return average

def average_time(diff_dict):
    #calculate the average time of flight for successful flights
    if len(times_list) != 0:
        average_time = math.fsum(times_list) / float(len(times_list))
    else:
        average_time =0
    return average_time

def succuss_precentage(diff_dict):
    num_it = len(diff_dict)-1
    times_list = diff_dict["times_list"]

    #draw a histegram of different finishing times
    succuss_precentage = 100*len(times_list)/(num_it)
    return succuss_precentage


#main function
def calc_stats(diff_dict):

    succ_prec = succuss_precentage(diff_dict)

    average_time = average_time(diff_dict)
    
    average_efficiency = search_efficiency(diff_dict)

    return (succ_prec ,average_time,average_efficiency )


if __name__ == "__main__":
    with open('data4.json') as data_file2:  
        dict_list = json.load(data_file2)
    print calc_stats(dict_list[1])
