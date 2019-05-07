# -*- coding: utf-8 -*-
"""
an illustration of how a single navigator types stats 
"""

from __future__ import division
from bars import get_data
import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

__authors__ = 'Noam Benelli'

matplotlib.rc('xtick', labelsize=15) 
matplotlib.rc('ytick', labelsize=15)


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


        
   

def present_graphs():
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


    fig,ax = plt.subplots()

    n_groups = 4
    bar_width = 0.3
    opacity = 0.4
    index = np.arange(0, 2*n_groups, 2)
    """
    data0 =(lib_succ[0],Bene_succ[0],lfs_succ[0],fs_succ[0])
    data1 =(lib_succ[1],Bene_succ[1],lfs_succ[1],fs_succ[1])
    data2 =(lib_succ[2],Bene_succ[2],lfs_succ[2],fs_succ[2])
    data3 =(lib_succ[3],Bene_succ[3],lfs_succ[3],fs_succ[3])
    """
    def set_charts(data0,data1,data2,data3):
        global chart
        chart = plt.bar(index, data0, bar_width,color = 'white', edgecolor='black')
        chart = plt.bar(index+bar_width, data1, bar_width,color = 'white', hatch = '+' ,edgecolor='black')
        chart = plt.bar(index+2*bar_width, data2, bar_width,color = 'white', hatch = '\\', edgecolor='black')
        chart = plt.bar(index+3*bar_width, data3, bar_width,color = 'black', hatch = '*', edgecolor='black')
    set_charts(lib_succ,Bene_succ,lfs_succ,fs_succ)
    if xlabel == 'puff_spread_rate':
        ax.set_xlabel(r'$\sigma$')
    else:
        ax.set_xlabel(xlabel)
    ax.set_ylabel('Success (%)')
    ax.xaxis.label.set_fontsize(17)
    ax.yaxis.label.set_fontsize(17)
    #ax.set_title('Success Percentage vs '+ xlabel)
    plt.xticks(index+bar_width*1.5, (str(values[0]), str(values[1]), str(values[2]),str(values[3])))
    plt.legend(legends)
    plt.tight_layout()


    plt.savefig('Success Percentage vs '+ xlabel)
    plt.show()
    
    #create second graph
    fig,ax = plt.subplots()

    n_groups = 4
    bar_width = 0.3
    opacity = 0.4
    index = np.arange(0, 2*n_groups, 2)
    
    #plt.xlabel(xlabel)
    #plt.ylabel('Average Navigation Time (ratio)')
    if xlabel == 'puff_spread_rate':
        ax.set_xlabel(r'$\sigma$')
    else:
        ax.set_xlabel(xlabel)
    ax.set_ylabel('T/'+r'$\tau$')

    
    set_charts(lib_avg,Bene_avg,lfs_avg,fs_avg)
    plt.subplots_adjust(bottom=0.15)
    plt.xticks(index+bar_width*1.5, (str(values[0]), str(values[1]), str(values[2]),str(values[3])))
    #ax.set_title('Average Navigation Time vs '+ xlabel)
    ax.xaxis.label.set_fontsize(17)
    ax.yaxis.label.set_fontsize(17)
    plt.legend(legends)
    plt.savefig('Average Navigation Time vs '+ xlabel)
    plt.show()
    
if __name__ == "__main__":
	present_graphs()

    

    

    
