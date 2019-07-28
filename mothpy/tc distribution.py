# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 16:53:54 2019

@author: Noam Benelli
"""

import sys
import pylab
import json


def open_data(file_name = 'data0.json'):
    with open('data0.json') as data_file:  
        dict_list = json.load(data_file) 
    print len(dict_list)
    print len(dict_list[0])
    return dict_list
    
    
def gen_points(lst):
    #recieves a trajectory
    #returns a list of tuples
    #(x,y,T,odor,gamma,state,success)
    point_lst = []
    current_tc = 0
    t_start = 0
    dt = lst[1][2] - lst[0][2]
    
    for tup in lst:
        odor = tup[3]
        last_odor = lst[lst.index(tup)-1][3]
        if odor:
            if last_odor:
                current_tc += dt
            else:
                current_tc = dt
                t_start = tup[2]
        else:
            if last_odor:
                point_lst.append((current_tc,t_start))
                current_tc = 0
    return point_lst
                
def arrange_dict_list(dict_list):
    lst = []
    for dic in dict_list:
        lst.extend(gen_points(dic["diff_list{0}".format(0)]))
    return lst
        
    
    
    
dict_list = open_data()
points = arrange_dict_list(dict_list)
print points

kzip = list(zip(*points))
x,y = kzip[0],kzip[1]

import matplotlib
matplotlib.pyplot.scatter(x,y)

    
         

                
                
                
                
            
        
    
    

