from __future__ import division

__authors__ = 'Noam Benelli'
import models
import Carde_navigator
from simulation import moth_simulation
from kalman import kalman_filter 
from moth_graphics import plot
#from statistics import calc_stats
import json
import copy

def create_trajectory_data(job_file_name = 'job.json',data_file_name ='data.json',
                           titles_file_name = 'titles.json'):
    with open(job_file_name) as data_file:
        cd = json.load(data_file) #constants dictionary
    sim_region = models.Rectangle(0., -1., 4., 1.)

    navigator1 = models.moth_modular(sim_region, cd['x_start'], cd['y_start'],cd['nav_type'] , 2, cd['wait_type'])
    navigator2 = models.moth_modular(sim_region, cd['x_start'], cd['y_start'],cd['nav_type'] , 'carde2', cd['wait_type'])
    navigator3 = models.moth_modular(sim_region, cd['x_start'], cd['y_start'],cd['nav_type'] , 'carde2', cd['wait_type'])
    navigator4 = models.moth_modular(sim_region, cd['x_start'], cd['y_start'],cd['nav_type'] , 'carde2', cd['wait_type'])
    navigator5 = models.moth_modular(sim_region, cd['x_start'], cd['y_start'],cd['nav_type'] , 'carde2', cd['wait_type'])
    navigators = [navigator1]
    
    ############################################################################
    #navigator setting for all navigators in the simulation
    #the parameter is set externally, as dictated by the job_generate function
    for navigator in navigators:
        navigator.threshold = cd['threshold']
        navigator.base_turn_angle = cd['base_turn_angle']
        #navigator.duration = cd['duration']
    ############################################################################
    
    #set up a large number of navigators with different properties
    navigator_titles = []
    counter = 0

    for j in range(10):
        for i in range(10):
            new_navigator = copy.copy(navigator1)
            new_navigator.wait_type = 'crw'
            new_navigator.cast_type = 'carde2'
            new_navigator.nav_type = 1
            new_navigator.y = 350
            new_navigator.x = 350
            new_navigator.base_duration  = 0.2 
            new_navigator.threshold = 200 + j*100
            
            title = 'wait = ' + str(new_navigator.wait_type) \
                +'; cast = ' + str(new_navigator.cast_type) \
                + '; nav = ' + str(new_navigator.nav_type) \
                + '; threshold = ' + str(new_navigator.threshold)\
                + ' ' + str(counter)
                
            navigators.append(new_navigator)
            navigator_titles.append(title)
            counter += 1

    for j in range(10):
        for i in range(10):
            new_navigator = copy.copy(navigator1)
            new_navigator.wait_type = 1
            new_navigator.cast_type = 1
            new_navigator.nav_type = 'alex'
            new_navigator.y = 400 - i*5
            new_navigator.x = 499 
            new_navigator.base_duration  = 0.1 
            new_navigator.threshold = 200 + j*100
            #title = str(i) 
            title = 'wait -' + str(new_navigator.wait_type) \
                +'; cast - ' + str(new_navigator.cast_type) \
                + '; nav - ' + str(new_navigator.nav_type) \
                + '; threshold = ' + str(new_navigator.threshold)\
                + ' ' + str(counter)
                
            navigators.append(new_navigator)
            navigator_titles.append(title)
            counter += 1


     




    #run the simulation - each navigator runs through the exact same conditions
    dict_list = moth_simulation(cd['num_it'],
                                navigators,cd['t_max'],cd['char_time'],
                                cd['amplitude'], cd['dt'], cd['puff_release_rate'])


    with open(data_file_name, 'w') as outfile:
        json.dump(dict_list, outfile)


        

    #print dict_list
    return navigator_titles






