from __future__ import division

__authors__ = 'Noam Benelli'
from pompy import models
import mothpy_models
from simulation import moth_simulation
import json
import copy

def create_trajectory_data(job_file_name = 'job.json',data_file_name ='data.json',
                           titles_file_name = 'titles.json'):
    with open(job_file_name) as data_file:
        cd = json.load(data_file) #constants dictionary
    sim_region = models.Rectangle(0.,-1.,4., 1.)


    #call the base navigator. the competing navigators in the simulation retain
    #any parameter of navigator1 that isn't changed
    navigator1 = mothpy_models.MothModular(sim_region, cd['x_start'], cd['y_start'],cd['nav_type'] , 2, cd['wait_type'])
    navigator1.base_turn_angle = cd['base_turn_angle']
    navigator1.threshold = cd['threshold']
    navigator1.duration = cd['duration']

    
    #set up a large number of navigators with different properties
    navigators = []
    navigator_titles = []


    def call_navigators(wait,cast,nav):
        for j in range(10):
            for i in range(20):
                new_navigator = copy.copy(navigator1)
                new_navigator.wait_type = wait
                new_navigator.cast_type = cast
                new_navigator.nav_type = nav
                new_navigator.y = 450 - i*3
                new_navigator.x = 499 - j

            title =  \
                ' cast - ' + str(new_navigator.cast_type) \
                + '; nav - ' + str(new_navigator.nav_type) \
                + str(len(navigators))
                
            navigators.append(new_navigator)
            navigator_titles.append(title)
    
    call_navigators(1,2,'alex')
    call_navigators(1,3,'alex')
    call_navigators(1,'carde2',1)
    call_navigators(1,'carde1',1)
     
    #run the simulation - each navigator runs through the exact same conditions
    dict_list = moth_simulation(cd['num_it'],
                                navigators,cd['t_max'],cd['char_time'],
                                cd['amplitude'], cd['dt'], cd['puff_release_rate'],
                                cd['puff_spread_rate'],
                                1,
                                False)


    with open(data_file_name, 'w') as outfile:
        json.dump(dict_list, outfile)
    return navigator_titles





