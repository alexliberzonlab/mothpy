# -*- coding: utf-8 -*-
"""
Implementations of puff-based plume model components.
"""

from __future__ import division

__authors__ = 'Matt Graham'
__license__ = 'MIT'

import numpy as np
import scipy.interpolate as interp
import random

def carde1(self, wind_vel_at_pos):
            if self.sweep_counter < 6:
                self.duration = self.base_duration
            else:
                self.duration = 6*self.base_duration
                if self.sweep_counter == 7:
                    self.sweep_counter = 0
                
            self.cast2(wind_vel_at_pos)
                
def carde2(self,wind_vel_at_pos):
            if self.sweep_counter < 6:
                self.duration = self.base_duration
            else:
                self.duration = 3*self.base_duration
                if self.sweep_counter == 7:
                    self.sweep_counter = 0
            self.cast2(wind_vel_at_pos)
