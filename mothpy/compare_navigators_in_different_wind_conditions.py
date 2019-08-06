from __future__ import division

__authors__ = 'Noam Benelli'


from job_generator import generate_job
from casting_competition import create_trajectory_data
from graphics_from_file import save_plot, save_detection_plot

import pandas as pd

"""
generates several job files containing the conditions of the simulations
calls upon "casting competition" to create trajectory data
(each call simulates four navigator types in one plume simulation)
plots a single plot for each one

"""

if __name__ == "__main__":
    for i in range(4):
        job_file_name = 'job'+ str(i)+ '.pkl'
        data_file_name = 'data'+ str(i)+ '.pkl.gz'
        const_dict = generate_job(char_time = 1, amplitude = 0.1, job_file = job_file_name,
                     t_max = 20, puff_release_rate = 100,
                     puff_spread_rate = 0.0001*(1+i),
                     dt = 0.1, num_it = 1)
        dict_list = create_trajectory_data(const_dict,data_file_name)

        df = pd.DataFrame(dict_list)
        df.to_pickle(data_file_name)

        # title = 'loop ' +str(i) 
        # save_plot(job_file_name,data_file_name,title,navigator_titles)
        #save_detection_plot(job_file_name,data_file_name,navigators_titles)
        
        print ('finished simulation number ' + str(i+1))

      
