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

            search_eff = T_odor/len(diff_dict["diff_list{0}".format(0)])
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
def average_time_relative(dict_list):
    """
    let us define the optimal time as the time it would have taken the navigator
    to reach it's final position if it were to move in straight line
    the relatve navigation time is define as measured time/optimal time
    this function calculates the relative navigation time for each successful navigator
    and returns an average
    """
    ##(x,y,T,odor,gamma,state,success)
    def first_movement(diff_list):
        for i in range(len(diff_list)):
            if diff_list[i][5] != 'wait':
                #print 'state = '+ diff_list[i][5]
                return i

    def calc_speed(diff_list):
        i = first_movement(diff_list)
        x1 = diff_list[i][0]
        y1 = diff_list[i][1]
        x2 = diff_list[i+1][0]
        y2 = diff_list[i+1][1]
        dist = distance(x1,y1,x2,y2)
        dt = diff_list[i+1][2] - diff_list[i][2]
        speed = dist/dt
        return speed

    def optimal_time(diff_list):
        x1 = diff_list[0][0]
        y1 = diff_list[0][1]
        x2 = diff_list[-1][0]
        y2 = diff_list[-1][1]
        opt_dist = distance(x1,y1,x2,y2)

        speed = calc_speed(diff_list)
        optimal_time = opt_dist/speed

        return optimal_time
        
    def distance(x1,y1,x2,y2):
       x = x2-x1
       y = y2-y1
       return (x**2+y**2)**0.5

    def optimal_distance(diff_list):
        x1 = diff_list[0][0]
        y1 = diff_list[0][1]
        x2 = diff_list[-1][0]
        y2 = diff_list[-1][1]
        return distance(x1,y1,x2,y2)
    
    
    def traveled_distance(diff_list):
        dist_sum = 0.0
        for i in range(1,len(diff_list)):
            if diff_list[i][-2]:
                x1 = diff_list[i-1][0]
                y1 = diff_list[i-1][1]
                x2 = diff_list[i][0]
                y2 = diff_list[i][1]
                dist_sum += distance(x1,y1,x2,y2)
        return dist_sum

    def time_elasped(diff_list):
        i = first_movement(diff_list)
        time_ela = diff_list[i][2]-diff_list[-1][2]
        return time_ela
                
    times_list = []
    for diff_dict in dict_list:
        for key in diff_dict:
            diff_list = diff_dict[key]
            if diff_list[-1][-1]:
                """
                optimal = optimal_distance(diff_list)
                traveled = traveled_distance(diff_list)
                #print (optimal,traveled)
                relative_time = traveled/optimal
                """
                elasped = time_elasped(diff_list)
                optimal = optimal_time(diff_list)
                relative_time = elasped/optimal
                times_list.append(math.fabs(relative_time))

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
    
    succuss_precentage = winners / len(dict_list) *100      
    return succuss_precentage
        

#main function
def calc_stats(diff_dict):

    succ_prec = succuss_precentage(diff_dict)

    avg_time = average_time_relative(diff_dict)
    
    average_efficiency = search_efficiency(diff_dict)

    return [succ_prec ,avg_time,average_efficiency]






def create_graphs(tot_stats,int_loop):
    nav_titles = ('Liberzon','Benelli','Large Final Sweeps','Final Sweeps')
    colors = ('green','red','blue','yellow')
    loop = str(int_loop)
    data1 = tot_stats[0]
    data2 = tot_stats[1]
    data3 = tot_stats[2]
    data4 = tot_stats[3]

    ####################################################################
    #one graph to show all of the data
    fig = plt.figure()
    ax = fig.add_subplot(111)

    n_groups = 4
    bar_width = 0.5
    opacity = 0.4
    index = np.arange(0, 2*n_groups, 2)
    """
    chart = plt.bar(index, data1, bar_width, color='blue', edgecolor='black')
    chart = plt.bar(index+bar_width, data2, bar_width, color='red', edgecolor='black')
    chart = plt.bar(index+2*bar_width, data3, bar_width, color='green', edgecolor='black')
    """
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

    chart = plt.bar(index, succ_prec, bar_width, color = colors, edgecolor='black')
    plt.xticks(index+bar_width*0.5, nav_titles)
    title = 'Success Percentage'
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(title +loop+'.png')
    #plt.show()


    #average time
    plt.figure()
    az = fig.add_subplot(111)

    chart = plt.bar(index, average_time_, bar_width, color=('green','red','blue','yellow'), edgecolor='black')
    plt.xticks(index+bar_width*0.5, nav_titles)
    title ='Average Time'
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(title +loop+'.png')
    #plt.show()

    #average_efficiency
    plt.figure()
    az = fig.add_subplot(111)

    chart = plt.bar(index, average_efficiency, bar_width, color=('green','red','blue'), edgecolor='black')
    plt.xticks(index+bar_width*0.5, nav_titles)
    title = 'Average Efficiency'
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(title +loop+'.png')
    #plt.show()

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

def get_data(file_name,num):
    with open(file_name) as data_file1:  
        dict_list1 = json.load(data_file1)

    spliced_lists = multi_splice(dict_list1,num)
    data_list = [calc_stats(dict_list) for dict_list in spliced_lists]

    return data_list
    
def check_for_duds():
    #checks for the numer of navigators that have not moved for the entire simulation
    #for each navigator in the dictionary it check the last entry in it's trajectory list
    #if it's state is 'waiting' at the last time step, we know it hasn't navigated at all.
    with open('data0.json') as data_file1:  
        dict_list = json.load(data_file1)
    dud_number = 0
    for nav_dict in dict_list:
        for key in nav_dict:
            #(x,y,T,odor,gamma,state,success)
            if nav_dict[key][-1][-2] == 'wait':
                print('dud found')
                dud_number +=1
            else:
                print(nav_dict[key][-1][-2])
    print(dud_number)
                
if __name__ == "__main__":
    #check_for_duds()
    for i in range(1):
        loop = str(i)
        data_list = get_data('data'+loop+'.json',4)
        print(data_list[0])
        #create_graphs(data_list,loop)

