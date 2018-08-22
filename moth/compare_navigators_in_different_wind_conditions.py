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
        job_file_ = 'job'+ str(i)+ '.json'
        data_file = 'data'+ str(i)+ '.json'
        generate_job(char_time =3.5, amplitude =0.1, job_file = job_file_,
                     threshold = 1500,base_turn_angle = 35,t_max = 50.,
                     dt = 0.05, num_it = 1, base_duration = 0.02*i)
        create_trajectory_data(job_file_,data_file)
        title = 'crw cast_carde2 nav1; duration = ' + str(0.02*i) + '; threshold = ' +str(1500) 
        save_plot(job_file_,data_file,title)
        save_detection_plot(job_file_,data_file)
