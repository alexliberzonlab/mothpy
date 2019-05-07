# -*- coding: utf-8 -*-
"""
Implementations of puff-based plume model components.
"""

from __future__ import division

__authors__ = 'Matt Graham'
__license__ = 'MIT'

import numpy as np


def carde1(self, wind_vel_at_pos):
            if self.state != 'cast':
                self.sweep_counter = 1
            if self.sweep_counter < 6:
                self.duration = self.base_duration
            else:
                self.duration = 3*self.base_duration
                if self.sweep_counter == 7:
                    self.sweep_counter = 0
            self.sweep_counter += 1
                
            self.cast2(wind_vel_at_pos)
                
def carde2(self,wind_vel_at_pos):
            if self.state != 'cast':
                self.sweep_counter = 1
            if self.sweep_counter%7!=0:
                self.duration = self.base_duration
            else:
                self.duration = 7*self.base_duration
                #print 'big sweep activated'
            self.sweep_counter += 1
            self.cast2(wind_vel_at_pos)



def crw(self,wind_vel_at_pos):
        if self.v == 0. and self.u == 0. :
            current_angle= 3.14*np.random.rand(1)[0] #start with a random angle
        else:
            current_angle = np.arctan2(self.v,self.u)
        turn_angle = 0.0174533*np.random.normal(self.base_turn_angle,1)#turn angle is distributed normally (5,1) degrees and translated to radians
        turn_angle = np.random.choice([-1,1])*turn_angle
        new_angle = current_angle + turn_angle
        self.u = self.speed*np.cos(new_angle)
        self.v = self.speed*np.sin(new_angle)
          
    
    
    
