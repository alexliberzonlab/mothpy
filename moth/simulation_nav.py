# -*- coding: utf-8 -*-
"""
Demonstrations of how to set up models with graphical displays produced using
matplotlib functions.
"""

from __future__ import division

__authors__ = 'Noam Benelli'


import sys
import pylab
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors
import numpy as np
import models
import processors
import scipy.misc
from demos import _close_handle,_set_up_figure,_simulation_loop


  
def moth_simulation(num_it=10,nav_type = 3, cast_type = 2, wait_type = 1 ,x_start = 450, y_start = 320, dt=0.01, t_max = 6, draw_iter_interval=1):
    """
    a copy of the concetration_array_demo with the moth actions integrated
    """
    #define simulation region
    wind_region = models.Rectangle(0., -2., 10., 2.)
    sim_region = models.Rectangle(0., -1., 2., 1.)
    #establish the dictionaries and lists that will be used
    moth_dict = {}
    list_dict = {}
    times_list1= []
    times_list2= []
    times_list3= []
    times_list4= []
    del_list = [] # a list of the moth indices that finished the track and were deleted 

    dist_it=10 #distance on y axis between starting points on different iterations
    for i in range(4*num_it):
        list_dict["moth_trajectory_list{0}".format(i)] = []
        if i<num_it:
            moth_dict["moth{0}".format(i)] = models.moth_modular(sim_region, x_start, y_start,1, cast_type, wait_type)
        elif i<2*num_it:
            moth_dict["moth{0}".format(i)] = models.moth_modular(sim_region, x_start, y_start,2, cast_type, wait_type)
        elif i<3*num_it:
            moth_dict["moth{0}".format(i)] = models.moth_modular(sim_region, x_start, y_start,3, cast_type, wait_type)
        else:
            moth_dict["moth{0}".format(i)] = models.moth_modular(sim_region, x_start, y_start,4, cast_type, wait_type)
    
        
        
    # set up wind model
    wind_model = models.WindModel(wind_region, 21., 11.,noise_gain=0, u_av=1.,)
    # set up plume model
    plume_model = models.PlumeModel(sim_region, (0.1, 0., 0.), wind_model,
                                    centre_rel_diff_scale=1.5,
                                    puff_release_rate=500,
                                    puff_init_rad=0.001)

    #set concetration array generator
    array_gen = processors.ConcentrationArrayGenerator(sim_region, 0.01, 500,
                                                       500, 1.)
    # display initial concentration field as image
    conc_array = array_gen.generate_single_array(plume_model.puff_array)
    
    # define update and draw functions
    def update_func(dt, t):
        wind_model.update(dt)
        plume_model.update(dt)
        conc_array = array_gen.generate_single_array(plume_model.puff_array)
        #update each individual moth
        for i in range(4*num_it):
            if i not in del_list:
                vel_at_pos = wind_model.velocity_at_pos(moth_dict["moth{0}".format(i)].x,moth_dict["moth{0}".format(i)].y)
                moth_dict["moth{0}".format(i)].update(conc_array,vel_at_pos,0.01)

    #each of the moth lists appends the new position given by it's corresponding moth
    def draw_func():
        for i in range(4*num_it):
            if i not in del_list:
                moth_i = moth_dict["moth{0}".format(i)]
                (x,y,T,odor,gamma,state) = (moth_i.x, moth_i.y, moth_i.T, moth_i.odor, moth_i.gamma, moth_i.state)
                list_dict["moth_trajectory_list{0}".format(i)].append((x,y,T,odor,gamma,state))
                if np.sqrt((x-25)**2+((y-250)**2))<15 : #if moth has reached target delete moth
                    if int(i/num_it) == 0:
                        times_list1.append(T)
                    if int(i/num_it) == 1:
                        times_list2.append(T)
                    if int(i/num_it) == 2:
                        times_list3.append(T)
                    if int(i/num_it) == 3:
                        times_list4.append(T)
                        
                    del moth_dict["moth{0}".format(i)]
                    del_list.append(i)
                if x<0 or x>499 or y<0 or y>499:    #if moth out of bounds delete moth
                    del moth_dict["moth{0}".format(i)] 
                    del_list.append(i)
            
    # start simulation loop
    _simulation_loop(dt, t_max, 0, draw_iter_interval, update_func,
                     draw_func)

    """
    after the simulation is done, list_dict is reedited to form diff_list_dict.
    difference list dictionary is a dictionary containing lists, each list represents a diffrent moth
    and each item in the list is a tuple of the form (x,y,T,odor found/odor lost/none, is turning/isn't turning)
    """
    diff_dict ={}
    #this shamefuly large tree transcribes the lists to the lists accounting for the moments of finding and losing odor
    #as well as counting when and where the moth decided to turn.
    for i in range(4*num_it):
        currentlist = list_dict["moth_trajectory_list{0}".format(i)]
        diff_list = []
        for j in range(len(currentlist)):
                (x,y,T,odor,gamma,state) = currentlist[j] #odor and gamma will be rewritten
                if j < 1: #first object on the list, nothing happens
                    odor = None
                    turning = False
                else: #describe the conditions for odor and turning documantation separately
                    if currentlist[j][3]==currentlist[j-1][3]:
                        odor = None                    
                    elif currentlist[j][3] == True and currentlist[j-1][3] == False:
                        odor = 'odor found'
                    else: #odor changed from True to false
                        odor = 'odor lost'
                    if currentlist[j][4]!=currentlist[j-1][4] or currentlist[j][5]!=currentlist[j-1][5]:
                        turning = True
                    else:
                        turning = False
                    
                diff_list.append((x,y,T,odor,turning))
        diff_dict["diff_list{0}".format(i)] = diff_list

    #experimentla part
    diff_dict1,diff_dict2,diff_dict3,diff_dict4 = {},{},{},{}
    for i in range(4*num_it):
        if i<num_it:
            diff_dict1["diff_list{0}".format(i)] = diff_dict["diff_list{0}".format(i)]
            print 1
        elif i<2*num_it:
            diff_dict2["diff_list{0}".format(i)] = diff_dict["diff_list{0}".format(i)]
            print 2
        elif i<3*num_it:
            diff_dict3["diff_list{0}".format(i)] = diff_dict["diff_list{0}".format(i)]
            print 3
        else:
            diff_dict4["diff_list{0}".format(i)] = diff_dict["diff_list{0}".format(i)]
            print 4



    #documantation:
    #set up text file to recored different lists
    file_name = "moth_trajectory" + "(" + str(x_start) + "," + str(y_start) + ")"
    file = open(file_name + ".txt", 'w')
    for i in range(4*num_it):
        file.write("moth trajectory " + str(i))
        file.write(str(diff_dict["diff_list{0}".format(i)])) 
    file.close()

    #to keep the code compact, diff_dict also carries time_list for further histogram use
    diff_dict1["times_list"]=times_list1
    diff_dict2["times_list"]=times_list2
    diff_dict3["times_list"]=times_list3
    diff_dict4["times_list"]=times_list4

    return (diff_dict1,diff_dict2,diff_dict3,diff_dict4)
