from __future__ import division

__authors__ = 'Noam Benelli'
from kalman import kalman_filter 
from moth_graphics import plot
import json


def save_plot(job_file_name = 'job.json',data_file_name ='data1.json',navigators = ('2','3','carde1','carde2')):
    with open(job_file_name) as data_file:
        cd = json.load(data_file) #constants dictionary
    with open(data_file_name) as data_file2:  
        dict_list = json.load(data_file2) #dictionary tuple

    
    for i in range(len(dict_list)):
        diff_dict = dict_list[i]
        kalman_dict = kalman_filter(diff_dict)
        navigator = navigators[i]
        title = 'cast type ' + navigator +'; char_time = ' +str(cd['char_time']) + '; amp = ' +str(cd['amplitude'])
        plot(kalman_dict,title)


