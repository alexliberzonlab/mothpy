# -*- coding: utf-8 -*-
from __future__ import division
from builtins import zip

__authors__ = 'Noam Benelli'

"""
a function that take one dictionary as input and
creats a graph of several colored plots as output
"""
import matplotlib.pyplot as plt
from shapes import circle,square , cx ,cy

   
def plot(kalman_dict, title = 'single navigator in flight', ax = None):
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure

    num_it = len(kalman_dict)
    # graphic function - shows only kalman trajectories, saves as file
    color_wheel =['-b','-r']
    for i in range(num_it): #present the different kalman trajectories
        kzip = list(zip(*kalman_dict["Kalman_list{0}".format(i)]))
        kx,ky = kzip[0],kzip[1]
        slice_list = [0] #a list of indexes of where to slice the list
        #the different lists will be presented with different colors (red/blue)
        #creating a single multicolor trajectory
        for tup in kalman_dict["Kalman_list{0}".format(i)]:
            if tup[3] == 'odor found' or tup[3] == 'odor lost':
                index = kalman_dict["Kalman_list{0}".format(i)].index(tup)
                slice_list.append(index)
                
        flag = False #a marker to see if any odor was detected throughout the simulation
        for j in range(len(slice_list)-1):
            flag = True #in the case where len(slice_list)==1, the flag will remain flase
            xslice = kx[slice_list[j]:slice_list[j+1]+1]
            yslice = ky[slice_list[j]:slice_list[j+1]+1]
            ax.plot(xslice,yslice,color_wheel[j%2]) #choose a color from the color wheel 

        #draw the final stretch of the trajectory after the last odor event 
        if flag == True:
            xslice = kx[slice_list[j+1]:]
            yslice = ky[slice_list[j+1]:]        
            ax.plot(xslice,yslice,color_wheel[(j+1)%2])
        else:
            ax.plot(kx,ky,'-b')

    marker = circle(500,20,30)  
    ax.plot(marker[0],marker[1],'-r')#add a red circle for the odor source 
    ax.set_ylim(0,1000)
    ax.set_xlim(0,1000)
    ax.set_xlabel('X position')
    ax.set_ylabel('Y position')
    ax.set_title(title)
    plt.legend(loc='upper left')  
    #plt.show()
    # fig.savefig(title + '.png')
    plt.clf() 


def detection_plot(kalman_dict, title = 'det plot'):
    #draws a plot of detection vs times (binary)
    num_it = len(kalman_dict)/2
    det=0 #detection is set for binary; odor found/lost toggels det
    for i in range(num_it): #present the different kalman trajectories
        t_list = []
        det_list = []
        for tup in kalman_dict["Kalman_list{0}".format(i)]: #for tuple in the trajectory list
            if tup[3] == 'odor found':
                det = 1
            elif tup[3] == 'odor lost':
                det = 0

            det_list.append(det)
            t_list.append(tup[2])
    
    plt.plot(t_list,det_list,'-k')
    plt.ylim(0,2)
    plt.xlim(0,len(kalman_dict["Kalman_list0"])*0.01 + 10)
    plt.xlabel('X position')
    plt.ylabel('Y position')

    plt.title(title)
    #plt.legend(('calculated','kalman'))
    plt.legend(loc='upper left')  
    #plt.show()
    plt.savefig(str(title) + '.png')
    plt.clf() 
    print("done")


