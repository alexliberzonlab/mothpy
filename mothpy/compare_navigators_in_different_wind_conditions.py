from __future__ import division

__authors__ = 'Noam Benelli'


from job_generator import generate_job
from casting_competition import create_trajectory_data
from graphics_from_file import save_plot, save_detection_plot

"""
generates several job files containing the conditions of the simulations
calls upon "casting competition" to create trajectory data
(each call simulates four navigator types in one plume simulation)
plots a single plot for each one

"""

if __name__ == "__main__":
    """
    for i in range(20):
        job_file_name = 'job_pfr'+ str(i)+ '.json'
        data_file_name = 'data_pfr'+ str(i)+ '.json'
        #titles_file_name = 'titles'+ str(i)+ '.json'       
        generate_job(char_time = 7, amplitude = 0.1, job_file = job_file_name,
                     t_max =20, puff_release_rate = 100,
                     puff_spread_rate = 0.00003*(1+i),
                     dt = 0.01, num_it = 1)
        navigator_titles = create_trajectory_data(job_file_name,data_file_name)
        title = 'loop ' +str(i) 
        #save_plot(job_file_name,data_file_name,title,navigator_titles)
        #save_detection_plot(job_file_name,data_file_name,navigators_titles)
        print ('finished simulation number ' + str(i+1))
    """
    for i in range(20):
        job_file_name = 'job_amp'+ str(i)+ '.json'
        data_file_name = 'data_amp'+ str(i)+ '.json'
        #titles_file_name = 'titles'+ str(i)+ '.json'       
        generate_job(char_time = 7, amplitude = 0.3, job_file = job_file_name,
                     t_max =20, puff_release_rate = 100,
                     puff_spread_rate = 0.0003,
                     dt = 0.01, num_it = 1)
        navigator_titles = create_trajectory_data(job_file_name,data_file_name)
        title = 'loop ' +str(i) 
        #save_plot(job_file_name,data_file_name,title,navigator_titles)
        #save_detection_plot(job_file_name,data_file_name,navigators_titles)
        print ('finished simulation number ' + str(i+1))

      
