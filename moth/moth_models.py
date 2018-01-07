# -*- coding: utf-8 -*-
"""
Implementations of moth-inspired navigators
"""

from __future__ import division

__authors__ = 'Noam Ben Elli'
__license__ = 'MIT'

import numpy as np
import scipy.interpolate as interp
import random

class moth_modular(object):
    def __init__(self,sim_region,x,y,nav_type = 3, cast_type = 2, wait_type = 1, beta=45,duration =0.2, speed = 200.0):
        self.x = x
        self.y = y
        self.u = 0
        self.v = 0
        
        self.sim_region = sim_region
        self.speed = speed
        
        #movement booleans and angles
        self.going_right = random.getrandbits(True)
        self.searching = False
        self.turned_on = False
        self.base_beta = (-1)**random.getrandbits(1)*np.radians(beta)
        self.beta = self.base_beta
        self.base_gamma = np.radians(90)
        self.gamma = self.base_gamma
        
        #movement types
        self.nav_type = nav_type
        self.cast_type = cast_type    
        self.wait_type = wait_type
        
        #time coefficients
        self.base_duration = duration
        self.duration = duration
        self.T = 0
        self.lamda = 0.2
        
        #odor coefficients
        self.threshold = 1500
        self.conc_max = 1
        self.base_conc = 20000

        
    """
    Moves within the field, tracking plume and wind data and navigating accordingly. 
    In this early design it is not affected by wind velocity, and can move freely.
    parameters:
    x : float
       Posistion at x
    y : float
       Position at y
    u : float
       Velocity on x axis
    v : on y axis
       Velocity on y axis
    beta : float
       Angle of attack
    D : float
       Distance travled without scent until the moth changes direction
    """
    def update_duration(self):
        if self.T%0.1:
            self.duration = self.base_duration*min(1,self.base_conc/self.conc_max)
        
    def update_gamma(self):
        #beta increseas as odor increases
        #beta is always smaller than pi/2
        if self.T%0.1:
            self.gamma = np.sign(self.gamma)*(1.5708 - ((1.5708 - np.abs(self.base_gamma)) * min(1 , self.base_conc/self.conc_max)))
            
    def calculate_wind_angle(self,wind_vel_at_pos):
        self.wind_angle = np.arcsin(wind_vel_at_pos[1]/np.sqrt(wind_vel_at_pos[0]**2+wind_vel_at_pos[1]**2))

    def change_direction(self):
        self.gamma = -self.gamma
        #in order to make sure the moth navigates in the direction in which it found the plume
        self.beta = np.sign(self.gamma)*np.abs(self.beta)
    
    def is_smelling(self,conc_array):
        """
        Basically determines whether or not the moth is sensing odor.
        A timer has been implemented in order to allow the moth navigate
        even with a lower threshold - After the odor is gone, the moth
        will still act as if smelling for time lamba.
        
        Needed inputs:
            self.x, self.y : position of the navigator 
            self.threshold : threshold of concentration
            self.timer : timer
            conc_array : array of concentration
        """
        if conc_array[self.x][self.y]>self.threshold:
            self.smell_timer = self.Timer(self.T,self.lamda)
            #nav mode three and four need to know whether the moth is smelling
            #at a specific moment.
            self.Tfirst = self.T
            return True
        elif self.turned_on:
            if self.smell_timer.is_running(self.T):
                return True
        else:
            return False

        
    class Timer(object):
        def __init__(self,T_start,duration=0.2):
            self.T_start = T_start
            self.duration = duration
        def is_running(self,T_current):
            #takes in current time and compares to start time. 
            #timer.is_running is True as long as the difference is smaller then the duration.
            return T_current - self.T_start < self.duration

    #motion functions are defined in advance
    def go_upwind(self,wind_vel_at_pos):
        self.calculate_wind_angle(wind_vel_at_pos)
        self.u = -self.speed*np.cos(self.wind_angle)
        self.v = self.speed*np.sin(self.wind_angle)

    def cast2(self,wind_vel_at_pos):
            #similar to nav_type 3
            #set timer as soon as moth isn't smelling odur, turn as soon as timer is over
            #duration grows every time timer is used
            if not self.searching:
                #start timer
                self.timer = self.Timer(self.T,self.duration)
                self.searching = True
            elif not self.timer.is_running(self.T):
                self.change_direction()
                self.timer = self.Timer(self.T,self.duration)
                self.duration = self.duration*2                    
            self.calculate_wind_angle(wind_vel_at_pos)
            self.u = -self.speed*np.cos(self.gamma+self.wind_angle)
            self.v = self.speed*np.sin(self.gamma+self.wind_angle)

    #Here the navigation types that were chosen in the initation come into play      
    def navigate(self,wind_vel_at_pos):
        if self.nav_type == 1:
            self.go_upwind(wind_vel_at_pos)

        if self.nav_type == 2:
            #traversing against wind direction at angle beta
            #wind direction
            #ground speed
            self.calculate_wind_angle(wind_vel_at_pos)
            self.u = -self.speed*np.cos(self.beta+self.wind_angle)
            self.v = self.speed*np.sin(self.beta+self.wind_angle)
          
        if self.nav_type == 3:
            #from the article, strategy 2
            #if moth is currently in sensing odor, go upwind
            #if moth has sensed odor in the last lamda, traverse at angle
            if self.Tfirst == self.T:
                self.go_upwind(wind_vel_at_pos)
            else:
                self.calculate_wind_angle(wind_vel_at_pos)
                self.u = -self.speed*np.cos(self.beta + self.wind_angle)
                self.v = self.speed*np.sin(self.beta + self.wind_angle)
                
        if self.nav_type == 4:
            #from the article, strategy 2
            self.calculate_wind_angle(wind_vel_at_pos)
            if self.T-self.Tfirst < 0.1:
                self.beta = np.sign(self.beta)*np.radians(10)
            elif self.T-self.Tfirst < 0.3: #if 0.1<t-Tfirst<0.3
                self.beta = np.sign(self.beta)*np.radians(65)
            else: # if 0.3<t-Tfirst
                self.beta = np.sign(self.beta)*np.radians(80)
            self.u = -self.speed*np.cos(self.beta+self.wind_angle)
            self.v = self.speed*np.sin(self.beta+self.wind_angle)     
                
        
        #no matter which nav mode is chosen, it turns the moth on     
        self.turned_on = True
        self.searching = False

    def cast(self,wind_vel_at_pos):
        if not self.searching:
            self.beta = -self.beta
            #in order to make sure the moth navigates in the direction in which it found the plume
            self.gamma = np.sign(self.beta)*np.abs(self.gamma)
            
        if self.cast_type == 1:
            self.u=0
            self.v=0

        if self.cast_type == 2:
            #define different betas for different casting patterns
            self.cast2(wind_vel_at_pos)

        if self.cast_type == 3:
            #same as cast_type 2, only beta and duration change according 
            self.update_gamma()
            self.update_duration()
            self.cast2(wind_vel_at_pos)


    def wait(self,wind_vel_at_pos):
        if self.wait_type == 1:
            self.u=0
            self.v=0

        if self.wait_type == 2:
            #coin toss between choosing to move left or right right
            #wind angle, constant ground speed
            self.calculate_wind_angle(wind_vel_at_pos)
            if self.going_right == 1:
                self.u = -self.speed*np.cos(np.radians(90) + self.wind_angle)
                self.v = self.speed*np.sin(np.radians(90) + self.wind_angle)
            else:
                self.u = -self.speed*np.cos(-np.radians(90) + self.wind_angle)
                self.v = self.speed*np.sin(-np.radians(90) + self.wind_angle)
            
                             
    def update(self,conc_array,wind_vel_at_pos,dt):        
        if self.is_smelling(conc_array):
            self.navigate(wind_vel_at_pos)
        elif self.turned_on:
            self.cast(wind_vel_at_pos)
        else:
            self.wait(wind_vel_at_pos)
        self.x += self.u*dt
        self.y += self.v*dt
        self.T += dt
        
    def moth_array(self, conc_array, wind_vel_at_pos):
        #draw moth position on matrix
        moth_array=np.zeros((500,500))
        for i in range(10):
            for j in range(10):
                moth_array[int(self.x)-i][int(self.y)-j]=3e4
        if self.is_smelling(conc_array):
            for i in range(6):
                for j in range(6):
                    moth_array[int(self.x)-i-2][int(self.y)-j-2]=0
        #project moth unto same matrix as the concetration
        return conc_array + moth_array

    
