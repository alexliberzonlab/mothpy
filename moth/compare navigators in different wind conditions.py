from __future__ import division

__authors__ = 'Noam Benelli'


from Job_generator import generate_job
from Casting_competition import create_trajectory_data
from graphics_from_file import save_plot

"""
generates several job files containing the conditions of the simulations
calls upon "casting competition" to create trajectory data
(each call creats simulates four navigator types)
plots a single plot for each one

"""


for i in range(10):
    job_file = 'job'+ str(i)+ '.json'
    data_file = 'data'+ str(i)+ '.json'
    generate_job(3.5,0.1*i,job_file) #the amplitude of wind noise (sine) grows with each iteration
    create_trajectory_data(job_file,data_file)
    save_plot(job_file,data_file)
