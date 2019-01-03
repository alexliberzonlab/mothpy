# -*- coding: utf-8 -*-
"""
an illustration of how a single navigator types stats 
"""

from __future__ import division
from bars import calc_stats,get_data, succuss_precentage,\
     average_time, search_efficiency
import json
import matplotlib.pyplot as plt
import numpy as np

__authors__ = 'Noam Benelli'


def create_line_graphs(tot_stats,int_loop):
    # nav_titles = ('Liberzon','Benelli','Large Final Sweeps','Final Sweeps')
    # colors = ('green','red','blue','yellow')
    # loop = str(int_loop)

    plt.figure()
    for stats in tot_stats:
        plt.plot(stats)
        # plt.ylabel('')

def detect_change(job_list):
    for key in job_list[0]:
        if job_list[0][key] != job_list[1][key]:
            sig_key = key
            break
    value_list =[]
    for job in job_list:
        value_list.append(job[sig_key])
        
    return (sig_key, value_list)

def process_jobs(num_jobs):
    job_list = []
    for i in range(num_jobs):
        file_name = 'job'+str(i)+'.json'
        with open(file_name) as data_file1:  
            job = json.load(data_file1)
        job_list.append(job)
    return detect_change(job_list)


        
   
if __name__ == "__main__":
    num_jobs = 4
    (xlabel,values)=process_jobs(num_jobs)
    legends = ('A','B','C','D')
    liberzonlist =[]
    Benellilist = []
    lfslist =[]
    fslist = []
    for i in range(num_jobs):
        loop = str(i)
        data_list = get_data('data'+loop+'.json',4)
        #print (data_list[0])
        liberzonlist.append(data_list[0])
        Benellilist.append((data_list[1]))
        lfslist.append((data_list[2]))
        fslist.append((data_list[3]))
    #[succ_prec ,average_time_,average_efficiency]
    lib_succ, lib_avg,lib_efficiency = zip(*liberzonlist)
    Bene_succ, Bene_avg,Bene_efficiency = zip(*Benellilist)
    lfs_succ, lfs_avg, lfs_efficiency = zip(*lfslist)
    fs_succ, fs_avg,fs_efficiency = zip(*fslist)

    # create first graph
    """
    plt.plot(values,lib_succ)
    plt.plot(values,Bene_succ)
    plt.plot(values,lfslist_succ)
    plt.plot(values,fslist_succ)

    plt.xlabel(xlabel)
    plt.ylabel('Success (%)')

    plt.title('Success Percentage vs '+ xlabel)
    plt.legend(legends)
    plt.show()
    """
    fig,ax = plt.subplots()

    n_groups = 4
    bar_width = 0.3
    opacity = 0.4
    index = np.arange(0, 2*n_groups, 2)
    
    data0 =(lib_succ[0],Bene_succ[0],lfs_succ[0],fs_succ[0])
    data1 =(lib_succ[1],Bene_succ[1],lfs_succ[1],fs_succ[1])
    data2 =(lib_succ[2],Bene_succ[2],lfs_succ[2],fs_succ[2])
    data3 =(lib_succ[3],Bene_succ[3],lfs_succ[3],fs_succ[3])

    chart = plt.bar(index, data0, bar_width, color='blue', edgecolor='black')
    chart = plt.bar(index+bar_width, data1, bar_width, color='red', edgecolor='black')
    chart = plt.bar(index+2*bar_width, data2, bar_width, color='green', edgecolor='black')
    chart = plt.bar(index+3*bar_width, data3, bar_width, color='yellow', edgecolor='black')

    ax.set_xlabel(xlabel)
    ax.set_ylabel('Success (%)')
    ax.set_title('Success Percentage vs '+ xlabel)
    plt.xticks(index+bar_width*1.5, (str(values[0]), str(values[1]), str(values[2]),str(values[3])))
    plt.legend(legends)
    plt.tight_layout()
    plt.show()

    #create second graph
    """
    plt.plot(values,lib_avg)
    plt.plot(values,Bene_avg)
    plt.plot(values,lfslist_avg)
    plt.plot(values,fslist_avg)
    """
    plt.xlabel(xlabel)
    plt.ylabel('Average Navigation Time (ratio)')
    
    plt.title('Average Navigation Time vs ' + xlabel)
    """
    plt.legend(legends)
    plt.show()
    """
    data0 =(lib_avg[0],Bene_avg[0],lfs_avg[0],fs_avg[0])
    data1 =(lib_avg[1],Bene_avg[1],lfs_avg[1],fs_avg[1])
    data2 =(lib_avg[2],Bene_avg[2],lfs_avg[2],fs_avg[2])
    data3 =(lib_avg[3],Bene_avg[3],lfs_avg[3],fs_avg[3])
    
    chart = plt.bar(index, data0, bar_width, color='blue', edgecolor='black')
    chart = plt.bar(index+bar_width, data1, bar_width, color='red', edgecolor='black')
    chart = plt.bar(index+2*bar_width, data2, bar_width, color='green', edgecolor='black')
    chart = plt.bar(index+3*bar_width, data3, bar_width, color='yellow', edgecolor='black')

    plt.xticks(index+bar_width*1.5, (str(values[0]), str(values[1]), str(values[2]),str(values[3])))
    #ax.set_title('Average Navigation Time vs '+ xlabel)
    plt.legend(legends)
    plt.show()


    
    #create third graph
    """ 
    plt.plot(values,lib_efficiency)
    plt.plot(values,Bene_efficiency)
    plt.plot(values,lfslist_efficiency)
    plt.plot(values,fslist_efficiency)
    """
    plt.xlabel(xlabel)
    plt.ylabel('Navigation Efficiency(ratio)')
    """
    plt.title('Navigation Efficiency vs ' + xlabel)
    plt.legend(legends)
    plt.show()
    """
    
    data0 =(lib_avg[0],Bene_avg[0],lfs_avg[0],fs_avg[0])
    data1 =(lib_avg[1],Bene_avg[1],lfs_avg[1],fs_avg[1])
    data2 =(lib_avg[2],Bene_avg[2],lfs_avg[2],fs_avg[2])
    data3 =(lib_avg[3],Bene_avg[3],lfs_avg[3],fs_avg[3])
    
    chart = plt.bar(index, data0, bar_width, color='blue', edgecolor='black')
    chart = plt.bar(index+bar_width, data1, bar_width, color='red', edgecolor='black')
    chart = plt.bar(index+2*bar_width, data2, bar_width, color='green', edgecolor='black')
    chart = plt.bar(index+3*bar_width, data3, bar_width, color='yellow', edgecolor='black')
    
    plt.xticks(index+bar_width*1.5, (str(values[0]), str(values[1]), str(values[2]),str(values[3])))
    ax.set_title('Navigation Efficiency vs '+ xlabel)
    plt.legend(legends)
    plt.show()
    

    
    

    
