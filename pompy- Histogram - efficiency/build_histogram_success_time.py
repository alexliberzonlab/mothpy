# -*- coding: utf-8 -*-
"""
Demonstrations of how to set up models with graphical displays produced using
matplotlib functions.
"""

from __future__ import division

__authors__ = 'Matt Graham'
__license__ = 'MIT'


import sys
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import models
import processors
import scipy.misc


def _close_handle(event):
    print('Simulation aborted.')
    sys.exit()


def _set_up_figure(title_text):
    """ Generate figure and attach close event. """
    fig = plt.figure()
    fig.canvas.set_window_title('Odour plume simulation: ' + title_text)
    fig.canvas.mpl_connect('close_event', _close_handle)
    # add simulation time text
    time_text = fig.text(0.05, 0.95, 'Simulation time: -- seconds')
    # start matplotlib interactive mode
    plt.ion()
    return fig, time_text


def _simulation_loop(dt, t_max, time_text, draw_iter_interval, update_func,
                     draw_func):
    """ Helper function for running simulation loop.

    Runs loop with time-step updates  applied to models in update_func and any
    relevant drawing actions applied in draw_func.
    """
    num_iter = int(t_max/dt + 0.5)
    for i in range(1, num_iter + 1):
        t = i * dt
        update_func(dt, t)
        # only update display after a batch of updates to increase speed
        if i % draw_iter_interval == 0:
            draw_func()

def moth_demo(x_start = 450, y_start = 310, dt=0.01, t_max = 5, draw_iter_interval=1):
    """
    a copy of the concetration_array_demo with the moth actions integrated
    """
    # define simulation region
    wind_region = models.Rectangle(0., -2., 10., 2.)
    sim_region = models.Rectangle(0., -1., 2., 1.)
    #establish the dictionaries that will be used
    moth_dict = {}
    list_dict = {}
    array_dict = {}
    times_list = [] # a list of the time it took different moths to reach the goal, for hist purposes
    del_list = [] # a list of the moth indices that finished the track and were deleted 
    num_it=10 #number of iterations
    dist_it=5 #distance on y axis between starting points on different iterations
    for i in range(num_it):
        moth_dict["moth{0}".format(i)] = models.moth_modular(sim_region, x_start, y_start-i)
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
    #moth_trajectory_file = open(file_name+ '.txt', "w")
    

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
    """
    #moth_trajectory_file.write(str(moth_trajectory_list))
    #moth_trajectory_file.close()
    #create a matrix, insert a trajectory list inside
    for i in range(num_it):
        for tup in list_dict["moth_trajectory_list{0}".format(i)]:
            array_dict["trajectory_array{0}".format(i)][tup[0]][tup[1]] = 250
        scipy.misc.imsave(file_name + str(i)+'.jpg', array_dict["trajectory_array{0}".format(i)])
    """
    #draw a histegram of different finishing times
    plt.hist(times_list,10)
    plt.show()
    plt.clf()
    print "done"





    
#run this to get a concentration array.
#save any frame which looks like a simple plume as an image. That is your heatmap which you can use for soundmapping

#concentration_array_demo()
# wind_vel_and_conc_demo()
#conc_point_val_demo()
#wind_model_demo()
#plume_model_demo()
moth_demo()


