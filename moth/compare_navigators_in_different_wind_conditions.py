from __future__ import division

__authors__ = 'Noam Benelli'

import numpy as np
from Job_generator import generate_job
from Casting_competition import create_trajectory_data
from graphics_from_file import save_plot, save_detection_plot

"""
generates several job files containing the conditions of the simulations
calls upon "casting competition" to create trajectory data
(each call simulates four navigator types in one plume simulation)
plots a single plot for each one

"""

if __name__ == "__main__":
    for i in range(1):
        job_file_name = 'job'+ str(i)+ '.json'
        data_file_name = 'data'+ str(i)+ '.json'
        #titles_file_name = 'titles'+ str(i)+ '.json'       
        generate_job(char_time = 1+i, amplitude =0.5, job_file = job_file_name,
                     t_max =10, puff_release_rate = 200,
                     dt = 0.01, num_it = 1)
        navigator_titles = create_trajectory_data(job_file_name,data_file_name)
        title = 'loop ' +str(i) 
        save_plot(job_file_name,data_file_name,title,navigator_titles)
        #save_detection_plot(job_file_name,data_file_name,navigators_titles)
        print 'finished simulation number ' + str(i+1)

#def plot(kalman_dict,name_dict, title = 'single navigator in flight'):        
