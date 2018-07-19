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
      
    pylab.plot(cx,cy,'-r')#add a circle for the odor source
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


