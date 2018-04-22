# -*- coding: utf-8 -*-
"""
Demonstrations of how to set up models with graphical displays produced using
matplotlib functions.
"""

from __future__ import division

__authors__ = 'Noam Benelli'


import sys
import pylab
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors
import numpy as np
import models
import processors
import scipy.misc
from demos import _close_handle,_set_up_figure,_simulation_loop
from shapes import circle,square , cx ,cy



#Now we shall add the Kalman filter, based heavily on Greg Czerniak's implementation.
class KalmanFilterLinear:
  def __init__(self,_A, _B, _H, _x, _P, _Q, _R):
    self.A = _A                      # State transition matrix.
    self.B = _B                      # Control matrix.
    self.H = _H                      # Observation matrix.
    self.current_state_estimate = _x # Initial state estimate.
    self.current_prob_estimate = _P  # Initial covariance estimate.
    self.Q = _Q                      # Estimated error in process.
    self.R = _R                      # Estimated error in measurements.
  def GetCurrentState(self):
    return self.current_state_estimate
  def Step(self,control_vector,measurement_vector):
    #---------------------------Prediction step-----------------------------
    predicted_state_estimate = self.A * self.current_state_estimate + self.B * control_vector
    predicted_prob_estimate = (self.A * self.current_prob_estimate) * np.transpose(self.A) + self.Q
    #--------------------------Observation step-----------------------------
    innovation = measurement_vector - self.H*predicted_state_estimate
    innovation_covariance = self.H*predicted_prob_estimate*np.transpose(self.H) + self.R
    #-----------------------------Update step-------------------------------
    kalman_gain = predicted_prob_estimate * np.transpose(self.H) * np.linalg.inv(innovation_covariance)
    self.current_state_estimate = predicted_state_estimate + kalman_gain * innovation
    # We need the size of the matrix so we can make an identity matrix.
    size = self.current_prob_estimate.shape[0]
    # eye(n) = nxn identity matrix.
    self.current_prob_estimate = (np.eye(size)-kalman_gain*self.H)*predicted_prob_estimate


def accelration_constraint(ax,ay,a_max):
  if ax > a_max:
    ax = a_max
  elif ax < -a_max:
    ax = -a_max
    
  if ay > a_max:
    ay = a_max
  elif ay < -a_max:
    ay = -a_max
  return np.matrix([[ax],[ay]])
  


    
def moth_demo(x_start = 450, y_start = 320, dt=0.01, t_max = 5, draw_iter_interval=1):
    """
    a copy of the concetration_array_demo with the moth actions integrated
    """
    # define simulation region
    wind_region = models.Rectangle(0., -2., 10., 2.)
    sim_region = models.Rectangle(0., -1., 2., 1.)
    #establish the dictionaries and lists that will be used
    moth_dict = {}
    list_dict = {}
    array_dict = {}
    times_list = [] # a list of the time it took different moths to reach the goal, for hist purposes
    del_list = [] # a list of the moth indices that finished the track and were deleted 

    num_it=10 #number of iterations
    dist_it=10 #distance on y axis between starting points on different iterations
    for i in range(num_it):
        moth_dict["moth{0}".format(i)] = models.moth_modular(sim_region, x_start, y_start-i*dist_it)
        list_dict["moth_trajectory_list{0}".format(i)] = []
        array_dict["trajectory_array{0}".format(i)] = np.zeros((500,500))
        
    # set up wind model
    wind_model = models.WindModel(wind_region, 21., 11.,noise_gain=0, u_av=1.,)
    # set up plume model
    plume_model = models.PlumeModel(sim_region, (0.1, 0., 0.), wind_model,
                                    centre_rel_diff_scale=1.5,
                                    puff_release_rate=500,
                                    puff_init_rad=0.001)

    #set concetration array generator
    array_gen = processors.ConcentrationArrayGenerator(sim_region, 0.01, 500,
                                                       500, 1.)
    # display initial concentration field as image
    conc_array = array_gen.generate_single_array(plume_model.puff_array)
    
    # define update and draw functions
    def update_func(dt, t):
        wind_model.update(dt)
        plume_model.update(dt)
        conc_array = array_gen.generate_single_array(plume_model.puff_array)
        #update each individual moth
        for i in range(num_it):
            if i not in del_list:
                vel_at_pos = wind_model.velocity_at_pos(moth_dict["moth{0}".format(i)].x,moth_dict["moth{0}".format(i)].y)
                moth_dict["moth{0}".format(i)].update(conc_array,vel_at_pos,0.01)

    #each of the moth lists appends the new position given by it's corresponding moth
    def draw_func():
        for i in range(num_it):
            if i not in del_list:
                moth_i = moth_dict["moth{0}".format(i)]
                (x,y,T,odor,gamma,state) = (moth_i.x, moth_i.y, moth_i.T, moth_i.odor, moth_i.gamma, moth_i.state)
                list_dict["moth_trajectory_list{0}".format(i)].append((x,y,T,odor,gamma,state))
                if np.sqrt((x-25)**2+((y-250)**2))<15 :
                    times_list.append(T)
                    del moth_dict["moth{0}".format(i)]
                    del_list.append(i)
            
    # start simulation loop
    _simulation_loop(dt, t_max, 0, draw_iter_interval, update_func,
                     draw_func)

    """
    after the simulation is done, list_dict is reedited to form diff_list_dict.
    difference list dictionary is a dictionary containing lists, each list represents a diffrent moth
    and each item in the list is a tuple of the form (x,y,T,odor found/odor lost/none, is turning/isn't turning)
    """
    diff_dict ={}
    #this shamefuly large tree transcribes the lists to the lists accounting for the moments of finding and losing odor
    #as well as counting when and where the moth decided to turn.
    for i in range(num_it):
        currentlist = list_dict["moth_trajectory_list{0}".format(i)]
        diff_list = []
        for j in range(len(currentlist)):
                (x,y,T,odor,gamma,state) = currentlist[j] #odor and gamma will be rewritten
                if j < 1: #first object on the list, nothing happens
                    odor = None
                    turning = False
                else: #describe the conditions for odor and turning documantation separately
                    if currentlist[j][3]==currentlist[j-1][3]:
                        odor = None                    
                    elif currentlist[j][3] == True and currentlist[j-1][3] == False:
                        odor = 'odor found'
                    else: #odor changed from True to false
                        odor = 'odor lost'
                    if currentlist[j][4]!=currentlist[j-1][4] or currentlist[j][5]!=currentlist[j-1][5]:
                        turning = True
                    else:
                        turning = False
                    
                diff_list.append((x,y,T,odor,turning))
        diff_dict["diff_list{0}".format(i)] = diff_list


    #implement the Kalman filter:
    #
    state_transition = np.matrix([[1,dt,0,0],[0,1,0,0],[0,0,1,dt],[0,0,0,1]])
    control_matrix = np.matrix([[(dt**2)/2,0],[0,(dt**2)/2],[dt,0],[0,dt]]) # acceleration constraint
    a_max = 0.01 
    control_vector = np.matrix([[0],[0],[0],[0]])
    observation_matrix = np.eye(4)
    initial_probability = np.eye(4)
    process_covariance =0.0001*np.eye(4) #A crucial factor in this process
    measurement_covariance = np.eye(4)*0.1 #also crucial
    
    #a dictionary of lists of the kalman corrections - (x,y) only.
    kalman_dict = {}
    #for each list in the list dictionary we will create a new kalman list 
    for i in range(num_it):
        kalman_dict["Kalman_list{0}".format(i)] = []   
        #initiate Kalman filter with our specific parameters
        initial_state = np.matrix([[x_start],[0],[y_start],[0]])       
        kf = KalmanFilterLinear(state_transition, control_matrix, observation_matrix, initial_state, initial_probability, process_covariance, measurement_covariance)
        vx,vy =0,0 #initial velocities are 
        for j in range(1,len(list_dict["moth_trajectory_list{0}".format(i)])):
            #There is no iteration for when j==0
            x = list_dict["moth_trajectory_list{0}".format(i)][j][0]
            y = list_dict["moth_trajectory_list{0}".format(i)][j][1]
            x_minus_1 =list_dict["moth_trajectory_list{0}".format(i)][j-1][0]
            y_minus_1 =list_dict["moth_trajectory_list{0}".format(i)][j-1][1]
            vx_minus_1 = vx #this iterations vx_minus1 is the last iterations vx
            vy_minus_1 = vy
            vx = (x - x_minus_1)/dt
            vy = (y - y_minus_1)/dt
            kx = (kf.GetCurrentState()[0,0])
            ky = (kf.GetCurrentState()[2,0])
            #apply the accelaration constraint
            ax=(vx-vx_minus_1)/dt
            ay=(vy-vy_minus_1)/dt
            control_vector = accelration_constraint(ax,ay,a_max)
            kf.Step(control_vector,np.matrix([[x],[vx],[y],[vy]]))
            kalman_dict["Kalman_list{0}".format(i)].append((kx,ky))


    #documantation:
    #set up text file to recored different lists
    file_name = "moth_trajectory" + "(" + str(x_start) + "," + str(y_start) + ")"
    file = open(file_name + ".txt", 'w')
    for i in range(num_it):
      file.write("moth trajectory " + str(i))
      file.write(str(diff_dict["diff_list{0}".format(i)])) 
    file.close()


    """        
    #graphics:       
    #create a matrix, insert all colored trajectories
    im = 1*np.ones((500,500,3))
    color_list =[(1,0,0),(0,1,0),(0,0,1)]
    #draw in the trajectories in different colors
    for i in range(num_it):
        for tup in diff_dict["diff_list{0}".format(i)]:
            im[tup[0]][tup[1]] = color_list[i%len(color_list)]
            #add colored markers for events on the graph
            if tup[3] == 'odor found':
                circle(im,tup[1],tup[0]) # red circle for finding odor
            if tup[3] == 'odor lost':
                circle(im,tup[1],tup[0],5,(0,0,1))#blue circle for losing odor
            if tup[4] == True:
                square(im,tup[1],tup[0])#green square for a sharp angle (timer runout)
    for i in range(num_it):
        for tup in kalman_dict["Kalman_list{0}".format(i)]:
            im[tup[0]][tup[1]] = (0.5,0.5,0.5)

    #draw the odor source as a big red circle
    circle(im,250,25,15)    
    fig, time_text = _set_up_figure('Concentration field array demo')
    # display initial concentration field as plot
    im_extents = (sim_region.x_min, sim_region.x_max,
                  sim_region.y_min, sim_region.y_max)
    conc_im = plt.imshow(conc_array.T, extent=im_extents)
    conc_im.axes.set_xlabel('x / m')
    conc_im.axes.set_ylabel('y / m')

    conc_im.set_data(im)
    plt.imshow(im)
    plt.show()

    #save plot as image
    scipy.misc.imsave('simulation of ' + str(num_it)+' moths' +'.jpg', im)
    """
    
    #alternative graphic function - shows only kalman trajectories
    color_wheel =['-b','-g','-c','-m','-y','-k']
    for i in range(num_it): #present the different kalman trajectories
      kzip = zip(*kalman_dict["Kalman_list{0}".format(i)])
      kx,ky=kzip[0],kzip[1]
      pylab.plot(kx,ky,color_wheel[i%6]) #choose a color from the color wheel for each trajectory
      
    pylab.plot(cx,cy,'-r')#add a circle for the odor source
    pylab.ylim(0,500)
    pylab.xlabel('X position')
    pylab.ylabel('Y position')
    pylab.title('competition between moths')
    #pylab.legend(('calculated','kalman'))
    pylab.legend(loc='upper left')  
    pylab.show()
    print "done"

moth_demo()


