from __future__ import division

__authors__ = 'Noam Benelli'
from kalman import kalman_filter 
from moth_graphics import plot, detection_plot
import json
import matplotlib.pyplot as plt


def save_plot(job_file_name = 'job.json',data_file_name ='data1.json',
              title='1',navigator_titles=[]):
    with open(job_file_name) as data_file:
        cd = json.load(data_file) #constants dictionary
    with open(data_file_name) as data_file2:  
        dict_list = json.load(data_file2) #dictionary tuple

    for i in range(len(dict_list)-1):
        diff_dict = dict_list[i]
        kalman_dict = kalman_filter(diff_dict)
        navigator_title = navigator_titles[i] + title
        fig, ax = plt.subplots()
        plot(kalman_dict,navigator_title,ax=ax)

def save_detection_plot(job_file_name = 'job.json',data_file_name ='data1.json',
                        navigator_titles = ('2','3','carde1','carde2','carde2')):
    with open(job_file_name) as data_file:
        cd = json.load(data_file) #constants dictionary
    with open(data_file_name) as data_file2:  
        dict_list = json.load(data_file2) #dictionary tuple

    
    for i in range(len(dict_list)):
        diff_dict = dict_list[i]
        kalman_dict = kalman_filter(diff_dict)
        #navigator = navigator_titles[i]
        ################################something should be done about these titles
        title =  '; amplitude = ' +str(cd['amplitude'])
        detection_plot(kalman_dict,title)



if __name__ == "__main__":
    save_plot('job0.json','data0.json')
