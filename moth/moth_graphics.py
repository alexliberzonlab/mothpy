# -*- coding: utf-8 -*-
from __future__ import division

__authors__ = 'Noam Benelli'

"""
a function that take one dictionary as input and
creats a graph of several colored plots as output
"""
import sys
import pylab
from shapes import circle,square , cx ,cy

   
def plot(kalman_dict, title = 'single navigator in flight'):
    num_it = len(kalman_dict)
    #alternative graphic function - shows only kalman trajectories
    color_wheel =['-b','-r']
    for i in range(num_it): #present the different kalman trajectories
        slice_list = [] #a list of indexes 
        kzip = zip(*kalman_dict["Kalman_list{0}".format(i)])
        kx,ky=kzip[0],kzip[1]
        for tup in kalman_dict["Kalman_list{0}".format(i)]:
            if tup[3] == 'odor found' or tup[3] == 'odor lost':
                index = kalman_dict["Kalman_list{0}".format(i)].index(tup)
                slice_list.append(index)
                
        flag = False #a marker to see if any odor was detected throughout the simulation
        for j in range(len(slice_list)-1):
            flag = True
            xslice = kx[slice_list[j]:slice_list[j+1]+1]
            yslice = ky[slice_list[j]:slice_list[j+1]+1]
            pylab.plot(xslice,yslice,color_wheel[(j+1)%2]) #choose a color from the color wheel 
        #draw the final stretch of the between the last odor event 
        if flag == True:
            xslice = kx[slice_list[j+1]:]
            yslice = ky[slice_list[j+1]:]        
            pylab.plot(xslice,yslice,color_wheel[j%2])
        else:
            pylab.plot(kx,ky,'-b')

    marker = circle(500,20,20)  
    pylab.plot(marker[0],marker[1],'-r')#add a red circle for the odor source 
    pylab.ylim(0,1000)
    pylab.xlim(0,1000)
    pylab.xlabel('X position')
    pylab.ylabel('Y position')
    pylab.title(title)
    #pylab.legend(('calculated','kalman'))
    pylab.legend(loc='upper left')  
    #pylab.show()
    pylab.savefig(title+ '.png')
    pylab.clf() 
    print "done"


def detection_plot(kalman_dict, title = 'det plot'):
    #draws a plot of detection vs times (binary)
    num_it = len(kalman_dict)
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
    
    pylab.plot(t_list,det_list,'-k')
    pylab.ylim(0,2)
    pylab.xlim(0,len(kalman_dict["Kalman_list0"])*0.01 + 10)
    pylab.xlabel('X position')
    pylab.ylabel('Y position')
    pylab.title(title)
    #pylab.legend(('calculated','kalman'))
    pylab.legend(loc='upper left')  
    #pylab.show()
    pylab.savefig(title+ '.png')
    pylab.clf() 
    print "done"


