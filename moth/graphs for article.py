# -*- coding: utf-8 -*-
from __future__ import division

__authors__ = 'Noam Benelli'

"""
a function that take one dictionary as input and
creats a graph of several colored plots as output
"""
import sys
import pylab
import json
from kalman import kalman_filter
from shapes import circle,square , cx ,cy

   
def plot(kalman_dict, title = 'Typical paths of navigators'):
    num_it = len(kalman_dict)
    # graphic function - shows only kalman trajectories, saves as file
    color_wheel =['-g','-c','-m','-y','-k']
    for i in range(num_it): #present the different kalman trajectories
        kzip = zip(*kalman_dict["Kalman_list{0}".format(i)])
        kx,ky = kzip[0],kzip[1]       
        pylab.plot(kx,ky,color_wheel[i])

    marker = circle(500,20,30)  
    #pylab.plot(marker[0],marker[1],'-r')#add a red circle for the odor source 
    pylab.ylim(200,800)
    pylab.xlim(0,600)
    pylab.xlabel('X position')
    pylab.ylabel('Y position')
    pylab.title(title)
    pylab.legend(('Liberzon','Final sweeps','Large final sweeps'))
    pylab.legend(loc='upper left')  
    #pylab.show()
    pylab.savefig(title + '.png')
    pylab.clf() 


if __name__ == "__main__":
    with open('data4.json') as data_file2:  
        dict_list = json.load(data_file2) #dictionary tuple
    new_dict ={}
    kalman_dict0 = dict_list[07]
    kalman_dict1 = dict_list[12]
    kalman_dict2 = dict_list[15]
    new_dict["diff_list0"] = kalman_dict0["diff_list{0}".format(0)] 
    new_dict["diff_list1"] = kalman_dict1["diff_list{0}".format(0)]
    new_dict["diff_list2"] = kalman_dict2["diff_list{0}".format(0)]
    
    kalman_dict = kalman_filter(new_dict)
    plot(kalman_dict)

