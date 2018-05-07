# -*- coding: utf-8 -*-
from __future__ import division

__authors__ = 'Noam Benelli'


import sys
import pylab
from shapes import circle,square , cx ,cy

   
def plot(kalman_dict,num_it):    
    #alternative graphic function - shows only kalman trajectories
    color_wheel =['-b','-g','-c','-m','-y','-k']
    for i in range(num_it): #present the different kalman trajectories
        kzip = zip(*kalman_dict["Kalman_list{0}".format(i)])
        kx,ky=kzip[0],kzip[1]
        pylab.plot(kx,ky,color_wheel[i%6]) #choose a color from the color wheel for each trajectory
      
    pylab.plot(cx,cy,'-r')#add a circle for the odor source
    pylab.ylim(0,500)
    pylab.xlim(0,500)
    pylab.xlabel('X position')
    pylab.ylabel('Y position')
    pylab.title('competition between moths')
    #pylab.legend(('calculated','kalman'))
    pylab.legend(loc='upper left')  
    pylab.show()
    print "done"


