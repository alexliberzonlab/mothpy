from __future__ import division

__authors__ = 'Noam Benelli'
import models
import Carde_navigator
from simulation import moth_simulation
from kalman import kalman_filter 
from moth_graphics import plot
from statistics import calc_stats
import json

def create_trajectory_data(job_file_name = 'job.json',data_file_name ='data.json'):
    with open(job_file_name) as data_file:
        cd = json.load(data_file) #constants dictionary
    sim_region = models.Rectangle(0., -1., 2., 1.)

    navigator1 = models.moth_modular(sim_region, cd['x_start'], cd['y_start'],cd['nav_type'] , 2)
    navigator2 = models.moth_modular(sim_region, cd['x_start'], cd['y_start'],cd['nav_type'] , 3)
    navigator3 = models.moth_modular(sim_region, cd['x_start'], cd['y_start'],cd['nav_type'] , 'carde1')
    navigator4 = models.moth_modular(sim_region, cd['x_start'], cd['y_start'],cd['nav_type'] , 'carde2')
    navigators =(navigator1,navigator2,navigator3,navigator4)

    #run the simulation - each navigator runs through the exact same condition
    dict_list = moth_simulation(cd['num_it'],navigators,cd['t_max'],cd['char_time'], cd['amplitude'])


    with open(data_file_name, 'w') as outfile:
        json.dump(dict_list, outfile)







