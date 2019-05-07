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
    """Helper function for running simulation loop.

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

            
def wind_model_demo(dt=0.01, t_max=20, draw_iter_interval=20):
    """
    Demonstration of setting up wind model and displaying with matplotlib
    quiver plot function.
    """
    # define simulation region
    wind_region = models.Rectangle(-8, -2, 8, 2)
    grid_spacing = 0.8
    wind_nx = int(wind_region.w / grid_spacing) + 1
    wind_ny = int(wind_region.h / grid_spacing) + 1
    # set up wind model
    wind_model = models.WindModel(wind_region, wind_nx, wind_ny,
                                  noise_gain=10., noise_damp=0,
                                  noise_bandwidth=2., u_av=3)
    # generate figure and attach close event
    fig, time_text = _set_up_figure('Wind model demo')
    # create quiver plot of initial velocity field
    vf_plot = plt.quiver(wind_model.x_points, wind_model.y_points,
                         wind_model.velocity_field[:, :, 0].T,
                         wind_model.velocity_field[:, :, 1].T, width=0.003)
    # expand axis limits to make vectors at boundary of field visible
    plt.axis(plt.axis() + np.array([-0.5, 0.5, -0.5, 0.5]))
    # define update and draw functions
    update_func = lambda dt, t: wind_model.update(dt)
    draw_func = lambda: vf_plot.set_UVC(wind_model.velocity_field[:, :, 0].T,
                                        wind_model.velocity_field[:, :, 1].T)
    # start simulation loop
    _simulation_loop(dt, t_max, time_text, draw_iter_interval, update_func,
                     draw_func) 
    return fig


#wind_model_demo()
