from __future__ import division

__authors__ = 'Noam Benelli'
from kalman import kalman_filter 
from moth_graphics import plot, detection_plot
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
        title = 'correlated random walk' +  '; base turn angle = ' +str(cd['base_turn_angle']) +' try number ' + str(i)
        plot(kalman_dict,title)

def save_detection_plot(job_file_name = 'job.json',data_file_name ='data1.json',navigators = ('2','3','carde1','carde2')):
    with open(job_file_name) as data_file:
        cd = json.load(data_file) #constants dictionary
    with open(data_file_name) as data_file2:  
        dict_list = json.load(data_file2) #dictionary tuple

    
    for i in range(len(dict_list)):
        diff_dict = dict_list[i]
        kalman_dict = kalman_filter(diff_dict)
        navigator = navigators[i]
        title = navigator + '; amplitude = ' +str(cd['amplitude'])
        detection_plot(kalman_dict,title)



if __name__ == "__main__":
    save_plot('job4.json','data4.json')
