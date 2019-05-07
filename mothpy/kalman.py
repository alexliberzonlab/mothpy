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
from pompy import models, processors, demos
import scipy.misc
# from demos import _close_handle,_set_up_figure,_simulation_loop
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
  
    
def kalman_filter(diff_dict):
    #implement the Kalman filter:
    #first we calculate dt from the list
    #(it's ugly but it's cleaner than taking it with the input)
    dt=diff_dict["diff_list{0}".format(0)][1][2] - diff_dict["diff_list{0}".format(0)][0][2]
    num_it = len(diff_dict)

    #define the matrices
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
        initial_state = np.matrix([[diff_dict["diff_list{0}".format(i)][0][0]],[0],[diff_dict["diff_list{0}".format(i)][0][1]],[0]])#initiate for x start and y start 
        kf = KalmanFilterLinear(state_transition, control_matrix, observation_matrix, initial_state, initial_probability, process_covariance, measurement_covariance)
        vx,vy =0,0 #initial velocities are 
        for j in range(1,len(diff_dict["diff_list{0}".format(i)])):
            #There is no iteration for when j==0
            x = diff_dict["diff_list{0}".format(i)][j][0]
            y = diff_dict["diff_list{0}".format(i)][j][1]
            x_minus_1 =diff_dict["diff_list{0}".format(i)][j-1][0]
            y_minus_1 =diff_dict["diff_list{0}".format(i)][j-1][1]
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
            time = diff_dict["diff_list{0}".format(i)][j][2]
            odor = diff_dict["diff_list{0}".format(i)][j][3]
            turning =diff_dict["diff_list{0}".format(i)][j][4]
            #kalman dict carries turning and odor finding information for graphing purposes
            kalman_dict["Kalman_list{0}".format(i)].append((kx,ky,time,odor,turning))          
    #print kalman_dict
    return kalman_dict
