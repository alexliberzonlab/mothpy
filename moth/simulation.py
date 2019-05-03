# -*- coding: utf-8 -*-
"""
Demonstrations of how to set up models with graphical displays produced using
matplotlib functions.
"""

from __future__ import division

__authors__ = 'Noam Benelli'


import numpy as np
import os
import imp
import mothpy_models
from pompy import models, processors, demos
  
def moth_simulation(num_it=10,navigators = (),t_max = 1,
                    char_time=3.5, amplitude = 0.1 ,
                    dt=0.01, puff_release_rate=10,
                    puff_spread_rate = 0.001,
                    draw_iter_interval = 1 ,
                    prep_plume = False):
    """
    a copy of the concetration_array_demo with the moth actions integrated
    """
    #define simulation region
    wind_region = models.Rectangle(0., -2.,10., 2.)
    sim_region = models.Rectangle(0., -1.,4., 1.)
    #establish the dictionaries and lists that will be used
    navigator_dict ={}
    del_list = [] # a list of the moth indices (i,j) that finished the track and were deleted 

    for j in range(len(navigators)):
        moth_dict = {}
        list_dict = {}
        for i in range(num_it):
            moth_dict["moth{0}".format(i)] = navigators[j]
            list_dict["moth_trajectory_list{0}".format(i)] = []
        navigator_dict["tup{0}".format(j)] = (moth_dict,list_dict)
        
        
        

        
    # set up wind model
    wind_model = mothpy_models.WindModel(wind_region, 21, 11,1,char_time,amplitude)
    # set up plume model
    pfr = puff_release_rate
    psr = puff_spread_rate
    plume_model = models.PlumeModel(sim_region, (0.1, 0., 0.), wind_model,
                                    centre_rel_diff_scale=0.75,
                                    puff_release_rate = pfr,
                                    puff_init_rad=0.001,
                                    puff_spread_rate=psr)

    #set concetration array generator
    array_gen = processors.ConcentrationArrayGenerator(sim_region, 0.01, 500,
                                                       1000, 1.)


    #run the wind and plume models for 4 seconds before navigators are started
    if prep_plume:
        for i in range(int(4/dt)):
            wind_model.update(dt)
            plume_model.update(dt)

    
    # define update and draw functions
    def update_func(dt, t):
        wind_model.update(dt)
        plume_model.update(dt)
        conc_array = array_gen.generate_single_array(plume_model.puff_array)

        for j in range(len(navigators)):
            #update each individual moth
            for i in range(num_it):
                if (i,j) not in del_list:
                    vel_at_pos = wind_model.velocity_at_pos(navigator_dict["tup{0}".format(j)][0]["moth{0}".format(i)].x,navigator_dict["tup{0}".format(j)][0]["moth{0}".format(i)].y)
                    navigator_dict["tup{0}".format(j)][0]["moth{0}".format(i)].update(conc_array,vel_at_pos,dt)


    #each of the moth lists appends the new position given by it's corresponding moth
    def draw_func():
        for j in range(len(navigators)):
            for i in range(num_it):
                if (i,j) not in del_list:
                    moth_dict = navigator_dict["tup{0}".format(j)][0]
                    moth_i = moth_dict["moth{0}".format(i)]
                    (x,y,T,odor,gamma,state,success) = (moth_i.x, moth_i.y, moth_i.T, moth_i.odor, moth_i.gamma, moth_i.state,False)
                    
                    if np.sqrt((x-25)**2+((y-500)**2))<15 :
                        success= True
                        del moth_dict["moth{0}".format(i)]
                        del_list.append((i,j))
                    #navigators that had reached the simulation's borders are deleted
                    if moth_i.y<0 or moth_i.y>999 or moth_i.x<0 or moth_i.x >499 :
                        del moth_dict["moth{0}".format(i)]
                        del_list.append((i,j))
                    navigator_dict["tup{0}".format(j)][1]["moth_trajectory_list{0}".format(i)].append((x,y,T,odor,gamma,state,success))                    

    #navigator_dict["tup{0}".format(j)] = (moth_dict,list_dict)


            
    # start simulation loop
    demos._simulation_loop(dt, t_max, 0, draw_iter_interval, update_func,
                     draw_func)

    """
    after the simulation is done, list_dict is reedited to form diff_list_dict.
    difference list dictionary is a dictionary containing lists, each list represents a diffrent moth
    and each item in the list is a tuple of the form (x,y,T,odor found/odor lost/none, is turning/isn't turning)
    """
    diff_dict_lst =[]
    #this shamefuly large tree transcribes the lists to the lists accounting for the moments of finding and losing odor
    #as well as counting when and where the moth decided to turn.
    for k in range(len(navigators)):
        diff_dict ={}
        for i in range(num_it):
            currentlist = navigator_dict["tup{0}".format(k)][1]["moth_trajectory_list{0}".format(i)]
            diff_list = []
            for j in range(len(currentlist)):
                    (x,y,T,odor,gamma,state,success) = currentlist[j] #odor and gamma will be rewritten
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
                    diff_list.append((x,y,T,odor,turning,state,success))
            diff_dict["diff_list{0}".format(i)] = diff_list
        diff_dict_lst.append(diff_dict)
      
    return diff_dict_lst

