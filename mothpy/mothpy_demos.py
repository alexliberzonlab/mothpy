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

import os
import imp
#import models
pathh = os.path.join(os.getcwd(), 'pompy', 'models.py')
models = imp.load_source('models', pathh)
import mothpy_models
#import processors
pathh = os.path.join(os.getcwd(), 'pompy', 'processors.py')
processors = imp.load_source('processors', pathh)

##############################################################################
#the following functions were taken from pompy, with minor changes 
##############################################################################
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
            time_text.set_text('Simulation time: {0} seconds'.format(t))
            plt.draw()
            plt.pause(0.001)
##############################################################################
#the following function was made as part of the mothpy project
##############################################################################
def moth_demo(dt=0.01, t_max = 15, draw_iter_interval=20):
    """
    a copy of the concetration_array_demo with the moth actions integrated

    List of specific changes to make the simulation into "widescreen" (simulation region is twice as wide)
    in moth_demo
    *sim_region = models.Rectangle(0., -1., 4., 1.)  x_max is 4
    *moth_model = models.moth_modular(sim_region, 450.0, 500.0,3,'carde1') y position is between 0 and 1000
    array_gen = processors.ConcentrationArrayGenerator(sim_region, 0.01, 500,1000, 1.)
    centre_rel_diff_scale=0.75,
    in models:
    moth_array=np.zeros((500,1000)) - considering that moth already takes in the simulation region, it should be relatively easy to make sure we don't have to change it manually every time. 
    def __init__(self, sim_region, source_pos, wind_model, model_z_disp=True,
                 centre_rel_diff_scale=2., puff_init_rad=0.03,
                 puff_spread_rate=0.001, puff_release_rate=10,
                 init_num_puffs=50, max_num_puffs=2000, prng=np.random):
    (max puffs increased to 2000)
    """
    
    
    # define simulation region
    wind_region = models.Rectangle(0., -2., 10., 2.)
    sim_region = models.Rectangle(0., -1., 4., 1.)
    #call moth model, set simulation region and starting position 
    moth_model = mothpy_models.MothModular(sim_region, 450.0, 750.0,2, 'carde2',1)
    """
    nav,cast,wait
    benelli - 2,3,1
    Liberzon - 'alex',2,1
    large sweeps - 1, 'carde2',1

    """
    #moth_model.speed = moth_model.speed*0.5
    #moth_model.lamda =0.7
    
    # set up wind model
    wind_model = models.WindModel(wind_region, 21, 11,noise_gain=0, u_av=1.,char_time =6,amplitude=0.3)
    # set up plume model
    plume_model = models.PlumeModel(sim_region, (0.1, 0., 0.), wind_model,
                                    centre_rel_diff_scale=0.3,
                                    puff_release_rate=100,
                                    puff_init_rad=0.001,puff_spread_rate=0.0001)

    # set up figure
    fig, time_text = _set_up_figure('Moth flying in Concentration field')
    # display initial concentration field as image
    #set concetration array generator
    array_gen = processors.ConcentrationArrayGenerator(sim_region, 0.01, 500,
                                                       1000, 1.)
    # display initial concentration field as image
    conc_array = array_gen.generate_single_array(plume_model.puff_array)
    im_extents = (sim_region.x_min, sim_region.x_max,
                  sim_region.y_min, sim_region.y_max)
    #conc_im is the displayed image of conc_array
    conc_im = plt.imshow(conc_array.T, extent=im_extents, vmin=0, vmax=3e4,
                         cmap=cm.binary_r)
    conc_im.axes.set_xlabel('x / m')
    conc_im.axes.set_ylabel('y / m')

    # define update and draw functions

    def update_func(dt, t):
        wind_model.update(dt)
        plume_model.update(dt)
        #moth_model.update(dt)   moth model should have an update method, even if just for syntax sake
        moth_model.update(array_gen.generate_single_array(plume_model.puff_array),wind_model.velocity_at_pos(moth_model.x,moth_model.y),0.01)
        #calculate proximity between moth and source
        if np.sqrt(moth_model.x**2+(moth_model.y-250)**2)<20:
            print "And they lived happily ever after"
        """
        #allow semi-infinite borders
        if moth_model.x<0:
            moth_model.x = 499 - moth_model.x
        if moth_model.x>499:
            moth_model.x = moth_model.x - 499
        if moth_model.y<0:
            moth_model.y = 499 - moth_model.y
        if moth_model.y>499:
            moth_model.y = moth_model.y - 499
        """
            
    #moth_model.moth_array takes both models as input, calculates moth position and adds that poisition(matrix addition) to the input
    #set _data then updates the plot image using the new matrix     
    draw_func = lambda: conc_im.set_data(
         moth_model.moth_array(array_gen.generate_single_array(plume_model.puff_array),wind_model))
        # start simulation loop
    _simulation_loop(dt, t_max, time_text, draw_iter_interval, update_func,
                     draw_func)
    return fig





    
#run this to get a concentration array.
#save any frame which looks like a simple plume as an image. That is your heatmap which you can use for soundmapping

#I Have made the color to binary_r, it is grayscale and in reverse. brighter means, more plume.
#Also I have made noise gain in wind model 0 to remove meandering.

#concentration_array_demo()
# wind_vel_and_conc_demo()
#conc_point_val_demo()
#wind_model_demo()
#plume_model_demo()
if __name__ == "__main__":
	moth_demo()
