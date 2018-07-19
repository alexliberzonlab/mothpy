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
    color_wheel =['-b','-g','-c','-m','-y','-k']
    for i in range(num_it): #present the different kalman trajectories
        #print kalman_dict["Kalman_list{0}".format(i)]
        kzip = zip(*kalman_dict["Kalman_list{0}".format(i)])
        kx,ky=kzip[0],kzip[1]
        pylab.plot(kx,ky,color_wheel[i%6]) #choose a color from the color wheel for each trajectory
        for tup in kalman_dict["Kalman_list{0}".format(i)]:
            if tup[3] == 'odor found':
                mark = circle(tup[1],tup[0])
                pylab.plot(mark[0],mark[1],'-r')
            elif tup[3] == 'odor lost':
                mark = circle(tup[1],tup[0])
                pylab.plot(mark[0],mark[1],'-g')


        
    pylab.plot(cx,cy,'-r')#add a red circle for the odor source 
    pylab.ylim(0,500)
    pylab.xlim(0,500)
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


