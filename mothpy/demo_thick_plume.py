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
from pompy import models, processors


def _close_handle(event):
    print('Simulation aborted.')
    sys.exit()


def _set_up_figure(title_text):
    """ Generate figure and attach close event. """
    fig = plt.figure()
    fig.canvas.set_window_title('Odour plume simulation: ' + title_text)
    fig.canvas.mpl_connect('close_event', _close_handle)
    
    # add simulation time text
    # start matplotlib interactive mode
    plt.ion()
    return fig 


def _simulation_loop(dt, t_max, draw_iter_interval, update_func,
                     draw_func,psr):
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
            #time_text.set_text('Simulation time: {0} seconds'.format(t))
            plt.draw()
            plt.pause(0.001)
        if t ==1.5:
            plt.savefig('puff_spread_rate = ' + str(psr)+'.png')




def concentration_array_demo(psr,dt=0.01, t_max=3.5, draw_iter_interval=50):
    """
    Demonstration of setting up plume model and processing the outputted
    puff arrays with the ConcentrationArrayGenerator class, the resulting
    arrays being displayed with the matplotlib imshow function.
    """
    # define simulation region
    wind_region = models.Rectangle(0., -2., 10., 2.)
    sim_region = models.Rectangle(0., -1., 2., 1.)
    # set up wind model
    wind_model = models.WindModel(wind_region, 21., 11.,noise_gain=0, u_av=2,)
    # set up plume model
    plume_model = models.PlumeModel(sim_region, (0.1, 0., 0.), wind_model,
                                    centre_rel_diff_scale=1.5,
                                    puff_release_rate=1000,
                                    puff_init_rad=0.001,puff_spread_rate=psr)
    # set up concentration array generator
    array_gen = processors.ConcentrationArrayGenerator(sim_region, 0.01, 500,
                                                       500, 1.)
    # set up figure
    fig = _set_up_figure('Concentration field array demo')
    # display initial concentration field as image
    conc_array = array_gen.generate_single_array(plume_model.puff_array)
    im_extents = (sim_region.x_min, sim_region.x_max,
                  sim_region.y_min, sim_region.y_max)
    conc_im = plt.imshow(conc_array.T, extent=im_extents, vmin=0, vmax=3e4,
                         cmap=cm.binary_r)
    conc_im.axes.set_xlabel('x')
    conc_im.axes.set_ylabel('y')
    

    # define update and draw functions

    def update_func(dt, t):
        wind_model.update(dt)
        plume_model.update(dt)

    draw_func = lambda: conc_im.set_data(
        array_gen.generate_single_array(plume_model.puff_array).T)
    # start simulation loop
    _simulation_loop(dt, t_max, draw_iter_interval, update_func,
                     draw_func,psr)
    plt.close()
    return fig






    
#run this to get a concentration array.
#save any frame which looks like a simple plume as an image. That is your heatmap which you can use for soundmapping

#I Have made the color to binary_r, it is grayscale and in reverse. brighter means, more plume.
#Also I have made noise gain in wind model 0 to remove meandering.

concentration_array_demo(0.0001)
concentration_array_demo(0.005)


