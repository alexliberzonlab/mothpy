# -*- coding: utf-8 -*-
"""
I/O routines to read data.json and job.json files
and split them into parts
"""

import os
import json
from .bars import calc_stats

__authors__ = 'Noam Benelli'



def get_data(file_name,num,data_path='.'):
    """
    Reads data.json files and splits them into `num` 
    parts. Data files are read from `data_path` (default is '.') 
    """
    file_name = os.path.join(data_path,file_name)
    with open(file_name) as data_file1:  
        dict_list1 = json.load(data_file1)

    spliced_lists = multi_splice(dict_list1,num)
    data_list = [calc_stats(dict_list) for dict_list in spliced_lists]

    return data_list

def multi_splice(list_dict,n):
    """ Helper function that splits the `list_dict` into
    `n` parts
    """

    length =len(list_dict)
    if length%n != 0:
        raise Exception('Number of navigators could not be devided into %0.1i' %n)
    spliced_lists = []
    lenn = int(length/n)
    for i in range(n):
        if i ==0 :
            new_list = list_dict[:lenn]
        elif i == n-1:
            new_list = list_dict[i*lenn:]
        else:
            new_list = list_dict[lenn*i:lenn*(i+1)]
        spliced_lists.append(new_list)
    return spliced_lists

def process_jobs(num_jobs,data_path='.'):
    """
    process_jobs(num_jobs, data_path='.') reads the 
    JSON files named 'job0.json' from 0 up to num_jobs 
    in the data_path (default is '.')
    """
    job_list = []
    for i in range(num_jobs):
        file_name = os.path.join(data_path,'job'+str(i)+'.json')
        with open(file_name) as data_file1:  
            job = json.load(data_file1)
        job_list.append(job)
    return detect_change(job_list)

def detect_change(job_list):
    """
    docstring is missing
    
    """
    for key in job_list[0]:
        if job_list[0][key] != job_list[1][key]:
            sig_key = key
            break
    value_list =[]
    for job in job_list:
        value_list.append(job[sig_key])
        
    return (sig_key, value_list)