# -*- coding: utf-8 -*-
"""
A simple statistical analysis of the simulation
caculates average time as well as success precentage
"""

from __future__ import division
import math
import matplotlib.pyplot as plt
import numpy as np
import json
import seaborn as sns
sns.set(style="darkgrid")

__authors__ = 'Noam Benelli'



def search_efficiency(dict_list):
    #calculate the ratio of time in which odor was detected/all of the flight time
    search_efficincy_list = []
    for j in range(len(dict_list)): #itirate through navigators
        
        diff_dict = dict_list[j]
        num_it = len(diff_dict)
        Last_dt_odor = False
        T_odor = 0
        T_no_odor = 0

        diff_list = diff_dict["diff_list{0}".format(0)]
        if diff_list[-1][-1]:
            for i in range(len(diff_list)): #itirate within list 
                odor = diff_list[i][3] #odor found or odor lost
                if odor == None and Last_dt_odor :
                    T_odor += 1
                elif odor =='odor found':
                    T_odor += 1
                    Last_dt_odor = True
                elif odor == 'odor lost':
                    Last_dt_odor = False

            search_eff = 1 - T_odor/len(diff_dict["diff_list{0}".format(0)])
            #print search_eff
            search_efficincy_list.append(search_eff)
    if search_efficincy_list != []:
        average = math.fsum(search_efficincy_list) / len(search_efficincy_list)
    else:
        average = 0
    return average

def average_time(dict_list):
    #calculate the average time of flight for successful flights
    times_list = []
    for diff_dict in dict_list:
        diff_list = diff_dict["diff_list{0}".format(0)]
        if diff_list[-1][-1]:
            finishing_time = diff_list[-1][2]
            times_list.append(finishing_time)

    #print times_list
    if len(times_list) != 0:
        average = math.fsum(times_list) / float(len(times_list))
    else:
        average = 0
    return average

def succuss_precentage(dict_list):
    winners = 0.
    for diff_dict in dict_list:
        diff_list = diff_dict["diff_list{0}".format(0)]
        #print diff_list[-1]
        if diff_list[-1][-1]:
            winners += 1
    
    succuss_precentage = winners / len(dict_list)       
    return succuss_precentage


#main function
def calc_stats(diff_dict):

    succ_prec = succuss_precentage(diff_dict)

    average_time_ = average_time(diff_dict)
    
    average_efficiency = search_efficiency(diff_dict)

    return [succ_prec ,average_time_,average_efficiency]


def seaborn_graphs(tot_stats):
    g = sns.FacetGrid(tot_stats, row="sex", col="time", margin_titles=True)
    bins = np.linspace(0, 60, 13)
    sns.barplot(x="sex", y="survived", hue="class", kind="bar", data=titanic);
    sns.show()

def create_graphs(tot_stats):
    data1 = tot_stats[0]
    data2 = tot_stats[1]
    data3 = tot_stats[2]

    ####################################################################
    #one graph to show all of the data
    fig = plt.figure()
    ax = fig.add_subplot(111)

    n_groups = 3
    bar_width = 0.5
    opacity = 0.4
    index = np.arange(0, 2*n_groups, 2)

    chart = plt.bar(index, data1, bar_width, color='blue', edgecolor='black')
    chart = plt.bar(index+bar_width, data2, bar_width, color='red', edgecolor='black')
    chart = plt.bar(index+2*bar_width, data3, bar_width, color='green', edgecolor='black')

    ax.set_xlabel('Performance (%)')
    ax.set_title('Overall comparison')

    plt.xticks(index+bar_width*1.5, ('Success %', 'AVG Time', 'AVG Efficiency'))
    plt.legend()
    plt.tight_layout()

    #plt.show()
    ############################################################################

    ############################################################################
    #three seperate graphs
    #success percenrage
    plt.figure()
    (succ_prec ,average_time_,average_efficiency) = zip(*tot_stats)
    ay = fig.add_subplot(111)
    index = np.arange(0, n_groups, 1)

    chart = plt.bar(index, succ_prec, bar_width, color='blue', edgecolor='black')
    plt.xticks(index+bar_width*0.5, ('Final Sweeps', 'Large Final Sweeps', 'Liberzon'))
    plt.title('Success Percentage')
    plt.legend()
    plt.tight_layout()
    #plt.show()


    #average time
    plt.figure()
    az = fig.add_subplot(111)

    chart = plt.bar(index, average_time_, bar_width, color='green', edgecolor='black')
    plt.xticks(index+bar_width*0.5, ('Final Sweeps', 'Large Final Sweeps', 'Liberzon'))
    plt.title('Average Time')
    plt.legend()
    plt.tight_layout()
    plt.show()

    #average_efficiency
    plt.figure()
    az = fig.add_subplot(111)

    chart = plt.bar(index, average_efficiency, bar_width, color='red', edgecolor='black')
    plt.xticks(index+bar_width*0.5, ('Final Sweeps', 'Large Final Sweeps', 'Liberzon'))
    plt.title('Average Efficiency')
    plt.legend()
    plt.tight_layout()
    plt.show()


    




def multi_splice(list_dict,n):
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





if __name__ == "__main__":
    with open('data0.json') as data_file1:  
        dict_list1 = json.load(data_file1)

    spliced_lists = multi_splice(dict_list1,3)
    data_list = [calc_stats(dict_list) for dict_list in spliced_lists]

    #seaborn_graphs(tot_stats)
    create_graphs(data_list)
    
