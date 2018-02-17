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
import moth
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
                     draw_func1,draw_func2 = 0):
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
            draw_func1()
            #drawfunction 2 is not always needed, or even defined - therefore a mechanism is defined for it's selective use
            if not draw_func2 == 0:
                draw_func2()
            

def wind_model_demo(dt=0.01, t_max=100, draw_iter_interval=20):
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
                                  noise_gain=10., noise_damp=0.1,
                                  noise_bandwidth=0.5, u_av=3)
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


def plume_model_demo(dt=0.01, t_max=100, draw_iter_interval=200):
    """
    Demonstration of setting up plume model and displaying with matplotlib
    plot and quiver functions.
    """
    # define simulation region
    sim_region = models.Rectangle(0., -2., 8., 2.)
    # set up wind model
    wind_model = models.WindModel(sim_region, 21., 11.,
                                  u_av=1., Kx=2., Ky=2.)
    # set up plume model
    plume_model = models.PlumeModel(sim_region, (0.5, 0., 0.), wind_model,
                                    puff_release_rate=10,
                                    centre_rel_diff_scale=1.5)
    # set up figure window
    fig, time_text = _set_up_figure('Plume model demo')
    # create quiver plot of initial velocity field
    # quiver expects first array dimension (rows) to correspond to y-axis
    # therefore need to transpose
    vf_plot = plt.quiver(wind_model.x_points, wind_model.y_points,
                         wind_model.velocity_field[:, :, 0].T,
                         wind_model.velocity_field[:, :, 1].T, width=0.001)
    # expand axis limits to make vectors at boundary of field visible
    vf_plot.axes.axis(vf_plot.axes.axis() + np.array([-0.5, 0.5, -0.5, 0.5]))
    # draw initial puff positions with scatter plot
    pp_plot = plt.scatter(plume_model.puff_array[:, 0],
                          plume_model.puff_array[:, 1],
                          100 * plume_model.puff_array[:, 3]**0.5,
                          c='r', edgecolors='none')

    # define update and draw functions

    def update_func(dt, t):
        wind_model.update(dt)
        plume_model.update(dt)

    def draw_func():
        # update velocity field quiver plot data
        vf_plot.set_UVC(wind_model.velocity_field[:, :, 0].T,
                        wind_model.velocity_field[:, :, 1].T)
        # update puff position scatter plot positions and sizes
        pp_plot.set_offsets(plume_model.puff_array[:, :2])
        pp_plot._sizes = 100*plume_model.puff_array[:, 3]**0.5

    # begin simulation loop
    _simulation_loop(dt, t_max, time_text, draw_iter_interval, update_func,
                     draw_func)
    return fig


def concentration_array_demo(dt=0.01, t_max=10, draw_iter_interval=50):
    """
    Demonstration of setting up plume model and processing the outputted
    puff arrays with the ConcentrationArrayGenerator class, the resulting
    arrays being displayed with the matplotlib imshow function.
    """
    # define simulation region
    wind_region = models.Rectangle(0., -2., 10., 2.)
    sim_region = models.Rectangle(0., -1., 2., 1.)
    # set up wind model
    wind_model = models.WindModel(wind_region, 21., 11.,noise_gain=0, u_av=1.,)
    # set up plume model
    plume_model = models.PlumeModel(sim_region, (0.1, 0., 0.), wind_model,
                                    centre_rel_diff_scale=1.5,
                                    puff_release_rate=500,
                                    puff_init_rad=0.001)
    # set up concentration array generator
    array_gen = processors.ConcentrationArrayGenerator(sim_region, 0.01, 500,
                                                       500, 1.)
    # set up figure
    fig, time_text = _set_up_figure('Concentration field array demo')
    # display initial concentration field as image
    conc_array = array_gen.generate_single_array(plume_model.puff_array)
    im_extents = (sim_region.x_min, sim_region.x_max,
                  sim_region.y_min, sim_region.y_max)
    conc_im = plt.imshow(conc_array.T, extent=im_extents, vmin=0, vmax=3e4,
                         cmap=cm.binary_r)
    conc_im.axes.set_xlabel('x / m')
    conc_im.axes.set_ylabel('y / m')

    # define update and draw functions

    def update_func(dt, t):
        wind_model.update(dt)
        plume_model.update(dt)

    draw_func = lambda: conc_im.set_data(
        array_gen.generate_single_array(plume_model.puff_array).T)
    # start simulation loop
    _simulation_loop(dt, t_max, time_text, draw_iter_interval, update_func,
                     draw_func)
    return fig


def conc_point_val_demo(dt=0.01, t_max=5, draw_iter_interval=20, x=1., y=0.0):
    """
    Demonstration of setting up plume model and processing the outputted
    puff arrays with the ConcentrationPointValueCalculator class, the
    resulting concentration time course at a point in the odour plume being
    displayed with the matplotlib plot function.
    """
    # define simulation region
    wind_region = models.Rectangle(0., -2., 10., 2.)
    sim_region = models.Rectangle(0., -1., 2., 1.)
    # set up wind model
    wind_model = models.WindModel(wind_region, 21., 11., u_av=2.)
    # set up plume model
    plume_model = models.PlumeModel(sim_region, (0.1, 0., 0.), wind_model,
                                    centre_rel_diff_scale=1.5,
                                    puff_release_rate=25,
                                    puff_init_rad=0.01)
    # let simulation run for 10s to get plume established
    for t in np.arange(0, 10, dt):
        wind_model.update(dt)
        plume_model.update(dt)
    # set up concentration point value calculator
    val_calc = processors.ConcentrationValueCalculator(0.01**2)
    conc_vals = []
    conc_vals.append(val_calc.calc_conc_point(plume_model.puff_array, x, y))
    ts = [0.]
    # set up figure
    fig, time_text = _set_up_figure('Concentration point value trace demo')
    # display initial concentration field as image
    conc_line, = plt.plot(ts, conc_vals)
    conc_line.axes.set_xlim(0., t_max)
    conc_line.axes.set_ylim(0., .5)
    conc_line.axes.set_xlabel('t / s')
    conc_line.axes.set_ylabel('Normalised concentration')
    conc_line.axes.grid(True)

    # define update and draw functions

    def update_func(dt, t):
        wind_model.update(dt)
        plume_model.update(dt)
        ts.append(t)
        conc_vals.append(
            val_calc.calc_conc_point(plume_model.puff_array, x, y))

    draw_func = lambda: conc_line.set_data(ts, conc_vals)
    # start simulation loop
    _simulation_loop(dt, t_max, time_text, draw_iter_interval, update_func,
                     draw_func)
    return fig


def wind_vel_and_conc_demo(dt=0.01, t_max=10, draw_iter_interval=50):
    """
    Demonstration of setting up plume model and processing the outputted
    puff arrays with the ConcentrationArrayGenerator class, the resulting
    arrays being displayed with the matplotlib imshow function.
    """
    # define simulation region
    wind_region = models.Rectangle(0., -1., 4., 1.)
    sim_region = models.Rectangle(0., -1., 4., 1.)
    # set up wind model
    wind_model = models.WindModel(wind_region, 11., 11., u_av=1.,
                                  noise_gain=9., noise_bandwidth=0.3)
    # set up plume model
    plume_model = models.PlumeModel(sim_region, (0.1, 0., 0.), wind_model,
                                    centre_rel_diff_scale=1.5,
                                    puff_release_rate=200,
                                    puff_init_rad=0.001)
    for t in np.arange(0, 1, dt):
        wind_model.update(dt)
        plume_model.update(dt)
    # set up concentration array generator
    array_gen = processors.ConcentrationArrayGenerator(sim_region, 0.01, 1000,
                                                       500, 1.)
    # set up figure
    fig, time_text = _set_up_figure('Concentration array demo')
    ax_c = fig.add_subplot('111')
    # ax_w = fig.add_subplot('122')
    # display initial wind velocity field as quiver plot
    vf_plot = ax_c.quiver(wind_model.x_points, wind_model.y_points,
                          wind_model.velocity_field[:, :, 0].T,
                          wind_model.velocity_field[:, :, 1].T, width=0.002)
    ax_c.set_xlabel('x / m')
    ax_c.set_ylabel('y / m')
    ax_c.set_aspect(1)
    # display initial concentration field as image
    conc_array = (
        array_gen.generate_single_array(plume_model.puff_array).T[::-1])
    im_extents = (sim_region.x_min, sim_region.x_max,
                  sim_region.y_min, sim_region.y_max)
    conc_im = ax_c.imshow(conc_array, extent=im_extents, vmin=0, vmax=5e3,
                          cmap=cm.Reds)
    ax_c.set_xlabel('x / m')
    ax_c.set_ylabel('y / m')

    # define update and draw functions

    def update_func(dt, t):
        wind_model.update(dt)
        plume_model.update(dt)

    def draw_func():
        conc_im.set_data(
            array_gen.generate_single_array(plume_model.puff_array).T[::-1, :])
        vf_plot.set_UVC(wind_model.velocity_field[:, :, 0].T,
                        wind_model.velocity_field[:, :, 1].T)

    # start simulation loop
    _simulation_loop(dt, t_max, time_text, draw_iter_interval, update_func,
                     draw_func)
    return fig

def prep_moth(dt=0.01, t_max = 2.1, draw_iter_interval=1):
    """
    saves a list of concetration arrays and wind arrays to be later taken as input by the reader moth
    """
    conc_list =[]
    wind_list =[]
    # define simulation region
    wind_region = models.Rectangle(0., -2., 10., 2.)
    sim_region = models.Rectangle(0., -1., 2., 1.)

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
        scipy.misc.imsave(str(t*100) + '.jpg', conc_array)
    
    draw_func1 = lambda : conc_list.append(conc_array)
    draw_func2 = lambda : wind_list.append((wind_model.velocity_field[:, :, 0],
                          wind_model.velocity_field[:, :, 1]))
    # start simulation loop
    _simulation_loop(dt, t_max, 0, draw_iter_interval, update_func,
                     draw_func1,draw_func2)
    return (conc_list, wind_list)

    
def reader_moth(conc_list,wind_list, x_start = 255, y_start = 50,nav_type = 3 ,cast_type = 2, wait_type = 1, dt=0.01, t_max = 2, draw_iter_interval=1):
    """
    a copy of the concetration_array_demo with the moth actions integrated
    """
    # define simulation region
    sim_region = models.Rectangle(0., -1., 2., 1.)
    #call moth model, set simulation region and starting position 
    moth_model = moth.moth_modular(sim_region, x_start, y_start, nav_type, cast_type, wait_type)
    
    #set up text file to recored the trajectory as a string of tuples
    file_name = "moth_trajectory" + "(" + str(x_start) + "," + str(y_start) + ")"
    moth_trajectory_file = open(file_name+ '.txt', "w")
    moth_trajectory_list = []

    # define update and draw functions
    def update_func(dt, t):
        x_wind_array = wind_list[int(t/dt)+1][0]#originally there should be here - wind_list[int(t/dt)][0] but it bugs out so 1 is a place holder for now
        y_wind_array = wind_list[int(t/dt)+1][1]
        wind_vector =(x_wind_array[int(moth_model.x/500*21)][int(moth_model.y/500*21)],y_wind_array[int(moth_model.x/500*21)][int(moth_model.y/500*21)])
        moth_model.update(conc_list[int(t/dt)+1],wind_vector,0.01)
            
    #moth_model.moth_array takes both models as input, calculates moth position and adds that poisition(matrix addition) to the input
    #set _data then updates the plot image using the new matrixmoth_model.moth_array(array_gen.generate_single_array(plume_model.puff_array),wind_model))
    draw_func = lambda : moth_trajectory_list.append((moth_model.x,moth_model.y,moth_model.T))
    # start simulation loop
    _simulation_loop(dt, t_max, 0, draw_iter_interval, update_func,
                     draw_func)
    #create a matrix, insert a trajectory list inside
    trajectory_array = np.zeros((500,500))
    for tup in moth_trajectory_list:
        trajectory_array[tup[0]][tup[1]] = 250
    scipy.misc.imsave(file_name + '.jpg', trajectory_array)
    moth_trajectory_file.write(str(moth_trajectory_list))
    print "done"





    
#run this to get a concentration array.
#save any frame which looks like a simple plume as an image. That is your heatmap which you can use for soundmapping

#concentration_array_demo()
# wind_vel_and_conc_demo()
#conc_point_val_demo()
#wind_model_demo()
#plume_model_demo()
prep = prep_moth()
reader_moth(prep[0],prep[1])

