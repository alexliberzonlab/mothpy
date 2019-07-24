# -*- coding: utf-8 -*-
from __future__ import division

__authors__ = 'Noam Benelli'

"""
a function that takes one dictionary as input and
creats a graph of several colored plots as output
"""
import sys
import pylab
import json
from kalman import kalman_filter
from shapes import circle,square , cx ,cy

   
def plot(kalman_dict, title = 'Typical paths of navigators'):
    num_it = len(kalman_dict)
    #print num_it
    # graphic function - shows only kalman trajectories, saves as file
    color_wheel =['-g','-m','-y','-k']
    for i in range(num_it): #present the different kalman trajectories
        kzip = zip(*kalman_dict["Kalman_list{0}".format(i)])
        kx,ky = kzip[0],kzip[1]       
        pylab.plot(kx,ky,color_wheel[i])
        #print ky

    #marker = circle(500,20,30)  
    #pylab.plot(marker[0],marker[1],'-r')#add a red circle for the odor source 
    pylab.ylim(200,800)
    pylab.xlim(0,600)
    pylab.xlabel('X position')
    pylab.ylabel('Y position')
    pylab.title(title)
    pylab.legend(('A','B','C','D'))
    #pylab.legend(loc='upper left')  
    pylab.show()
    pylab.savefig(title + '.png')
    #pylab.clf() 
fake_list = [(0,0),(300,300)]

#if __name__ == "__main__":
for i in range(1):
    with open('data0.json') as data_file2:  
        dict_list = json.load(data_file2) 
    new_dict ={}
    #print type(dict_list[137])
    print len(dict_list)
    kalman_dict0 = dict_list[14]
    kalman_dict1 = dict_list[15]
    kalman_dict2 = dict_list[16]
    kalman_dict3 = dict_list[17]
    """
    kalman_dict0 = dict_list[137]
    kalman_dict1 = dict_list[369]
    kalman_dict2 = dict_list[495]
    kalman_dict3 = dict_list[789]
    """
    new_dict["diff_list0"] = kalman_dict0["diff_list{0}".format(0)] 
    #new_dict["diff_list0"] = fake_list
    new_dict["diff_list1"] = kalman_dict1["diff_list{0}".format(0)]
    new_dict["diff_list2"] = kalman_dict2["diff_list{0}".format(0)]
    new_dict["diff_list3"] = kalman_dict3["diff_list{0}".format(0)]
    #print type(kalman_dict0["diff_list{0}".format(0)])
    
    kalman_dict = kalman_filter(new_dict)
    #kalman_dict["Kalman_list{0}".format(0)] = fake_list

    title1 = 'Demonstration of Large Final Sweeps Casting' +str(i)
    title2 = 'Demonstration of different navigation strategies'
    plot(kalman_dict,title2)

