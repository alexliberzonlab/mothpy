# -*- coding: utf-8 -*-
"""
Demonstrations of how to set up models with graphical displays produced using
matplotlib functions.
"""

from __future__ import division

__authors__ = 'Noam Benelli'


import sys
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors
import numpy as np
import models
import processors
import scipy.misc
from demos import _close_handle,_set_up_figure,_simulation_loop


def moth_demo(x_start = 450, y_start = 310, dt=0.01, t_max = 5, draw_iter_interval=1):
    """
    a copy of the concetration_array_demo with the moth actions integrated
    """
    # define simulation region
    wind_region = models.Rectangle(0., -2., 10., 2.)
    sim_region = models.Rectangle(0., -1., 2., 1.)
    #establish the dictionaries and lists that will be used
    moth_dict = {}
    list_dict = {}
    array_dict = {}
    times_list = [] # a list of the time it took different moths to reach the goal, for hist purposes
    del_list = [] # a list of the moth indices that finished the track and were deleted 

    num_it=30 #number of iterations
    dist_it=5 #distance on y axis between starting points on different iterations
    for i in range(num_it):
        moth_dict["moth{0}".format(i)] = models.moth_modular(sim_region, x_start, y_start-i*dist_it)
        list_dict["moth_trajectory_list{0}".format(i)] = []
        array_dict["trajectory_array{0}".format(i)] = np.zeros((500,500))
        
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
    
    #set up text file to recored the trajectory as a string of tuples
    file_name = "moth_trajectory" + "(" + str(x_start) + "," + str(y_start) + ")"
    

    # define update and draw functions

    def update_func(dt, t):
        wind_model.update(dt)
        plume_model.update(dt)
        conc_array = array_gen.generate_single_array(plume_model.puff_array)
        #update each individual moth
        for i in range(num_it):
            if i not in del_list:
                vel_at_pos = wind_model.velocity_at_pos(moth_dict["moth{0}".format(i)].x,moth_dict["moth{0}".format(i)].y)
                moth_dict["moth{0}".format(i)].update(conc_array,vel_at_pos,0.01)
    #moth_model.moth_array takes both models as input, calculates moth position and adds that poisition(matrix addition) to the input
    #each of the moth lists appends the new position given by it's corresponding moth
    def draw_func():
        for i in range(num_it):
            if i not in del_list:
                (x,y,T) = (moth_dict["moth{0}".format(i)].x,moth_dict["moth{0}".format(i)].y,moth_dict["moth{0}".format(i)].T)
                list_dict["moth_trajectory_list{0}".format(i)].append((x,y,T))
                if np.sqrt((x-25)**2+((y-250)**2))<15 :
                    times_list.append(T)
                    del moth_dict["moth{0}".format(i)]
                    del_list.append(i)
                    print "deleted moth number", str(i)
                

            
    # start simulation loop
    _simulation_loop(dt, t_max, 0, draw_iter_interval, update_func,
                     draw_func)
    
    #create a matrix, insert all colored trajectories
    im = 1*np.ones((500,500,3))
    color_list =[(1,0,0),(0,1,0),(0,0,1)]
    #draw in the trajectories in different colors
    for i in range(num_it):
        for tup in list_dict["moth_trajectory_list{0}".format(i)]:
            im[tup[0]][tup[1]] = color_list[i%len(color_list)]
    #color in the odor source
    for i in range(4,41):
        for j in range(230,266):
            if np.sqrt((i-25)**2+((j-250)**2))<15 :
                im[i][j] = (1,0.1,0.1)

    fig, time_text = _set_up_figure('Concentration field array demo')
    # display initial concentration field as plot
    im_extents = (sim_region.x_min, sim_region.x_max,
                  sim_region.y_min, sim_region.y_max)
    conc_im = plt.imshow(conc_array.T, extent=im_extents)
    conc_im.axes.set_xlabel('x / m')
    conc_im.axes.set_ylabel('y / m')

    conc_im.set_data(im)
    plt.imshow(im)
    plt.show()

    #save plot as image
    scipy.misc.imsave('simulation of ' + str(num_it)+' moths' +'.jpg', im)
    
    print "done"

moth_demo()


