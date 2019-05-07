# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 16:22:41 2019

@author: Noam Benelli
"""

import numpy as np
import random
from carde_navigator import carde1, carde2, crw
from pompy import models



class WindModel(models.WindModel):
    def __init__(self, sim_region, nx=15, ny=15, u_av=0.4,char_time = 3.5,amplitude = 0.1, v_av=0., Kx=2.,
                 Ky=2., noise_gain=0., noise_damp=0.2, noise_bandwidth=0.2, #noise_gain=5 change to 0
                 noise_rand=np.random):
        super(WindModel, self).__init__(sim_region,nx=nx,ny=ny,u_av=u_av,char_time=char_time,
                                        amplitude=amplitude,v_av=v_av,Kx=Kx,Ky=Ky,
                                        noise_gain=noise_gain, noise_damp=noise_damp,
                                        noise_bandwidth=noise_bandwidth,noise_rand=noise_rand)
        # self.char_time = char_time
        # self.amplitude = amplitude
        # self.noise_gen = MeanderingGenerator(np.zeros((2, 8)), noise_damp,
        #                                         noise_bandwidth, noise_gain,
        #                                         noise_rand,self.char_time,self.amplitude)
        # compute grid node spacing
        # self.dx = abs(sim_region.w / (n_x - 1)  # x grid point spacing
        # self.dy = sim_region.h / (n_y - 1)  # y grid point spacing
        # initialise wind velocity field to mean values
        # +2s are to account for boundary grid points
        # self._u = np.ones((n_x + 2, n_y + 2)) * u_av
        # self._v = np.ones((n_x + 2, n_y + 2)) * v_av
        # create views on to field interiors (i.e. not including boundaries)
        # for notational ease - note this does not copy any data
        # self._u_int = self._u[1:-1, 1:-1]
        # self._v_int = self._v[1:-1, 1:-1]
        # preassign array of corner means values
        # self._corner_means = np.array([u_av, v_av]).repeat(4)
        # precompute linear ramp arrays with size of boundary edges for
        # linear interpolation of corner values
        # self._ramp_x = np.linspace(0., 1., nx + 2)
        # self._ramp_y = np.linspace(0., 1., ny + 2)
        # set up cubic spline interpolator for calculating off-grid wind
        # velocity field values
        # self._x_points = np.linspace(sim_region.x_min, sim_region.x_max, n_x)
        # self._y_points = np.linspace(sim_region.y_min, sim_region.y_max, n_y)
        # initialise flag to indicate velocity field interpolators not set
        self._interp_set = True
    
class MeanderingGenerator(object):

    """
    Generates a sine noise output via Euler integration of a state space
    system formulation.
    """

    def __init__(self, init_state, damping, bandwidth, gain,
                 prng=np.random,char_time = 3.5,amplitude = 0.1):

        self.T =0
        self.char_time = char_time #cycle time for wind
        self.amplitude = amplitude
        
    @property
    def output(self):
        """Coloured noise output."""
        return self._x[0, :]

    def update(self, dt):
        """Updates state of noise generator."""
        sin_noise = self.amplitude*np.sin (3.14/self.char_time*self.T)
        self._x = np.zeros((2,8))
        self._x[0,4:]= sin_noise
        self.T+=dt #timestep

        
  
class MothModular(object):
    def __init__(self,sim_region,x,y,nav_type = 1,
                 cast_type = 'carde2', wait_type = 1,
                 beta=30, duration =0.5, speed = 200.0):
        self.x = x
        self.y = y
        self.u = 0
        self.v = 0
        self.sim_region = sim_region
        self.speed = speed
        
        #movement booleans and angles
        self.searching = False
        self.turned_on = False 
        #beta = navigating angle
        self.base_beta = (-1)**random.getrandbits(1)*np.radians(beta)
        self.beta = self.base_beta
        #gamma = casting angle
        self.base_gamma = np.radians(90)
        self.gamma = (-1)**random.getrandbits(1)*self.base_gamma
        #carde navigators
        self.base_turn_angle = 5 #for crw
        self.sweep_counter = 0 # counts the number of turns for big sweep cast modes

        
        #movement types
        self.nav_type = nav_type
        self.cast_type = cast_type    
        self.wait_type = wait_type
        self.title = ' '
        self.state = 'wait' # or 'nav' or 'cast'
        
        #time coefficients
        self.base_duration = duration
        self.duration = duration
        self.T = 0
        self.lamda = 0.1
        self.alex_factor = 1.5
        
        #odor coefficients
        self.threshold = 500
        self.conc_max = 1
        self.base_conc = 20000
        self.odor = False
        self.last_dt_odor = False #used in 'alex' navigation

        
        
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
    Duration : float
       Time travled without odor until the moth changes direction
    """
    def update_duration(self):
        #used in navigation modes three and four
        if self.T%0.1:
            self.duration = self.base_duration*min(1,self.base_conc/self.conc_max)
        
    def update_gamma(self):
        #used in navigation modes three and four
        #beta increseas as odor increases
        #beta is always smaller than pi/2
        if self.T%0.1:
            self.gamma = np.sign(self.gamma)*(1.5708 - ((1.5708 - np.abs(self.base_gamma)) * min(1 , self.base_conc/self.conc_max)))
            
    def calculate_wind_angle(self,wind_vel_at_pos):
        #The angle of the wind as percieved from the ground. Does not use the moth's speed.
        self.wind_angle = np.arcsin(wind_vel_at_pos[1]/np.sqrt(wind_vel_at_pos[0]**2+wind_vel_at_pos[1]**2))

    def change_direction(self):
        self.gamma = -self.gamma
        #In order to make sure the moth navigates in the direction in which it found the plume
        #the sign of beta is always the same as the sign of gamma
        self.beta = np.sign(self.gamma)*np.abs(self.beta)
        #Input self.gamma,self.beta
        self.sweep_counter +=1
    
    def is_smelling(self,conc_array):
        """
        Determines whether or not the moth is sensing odor.
        A timer has been implemented in order to allow the moth navigate
        even with a lower threshold - After the odor is gone, the moth
        will still act as if it is smelling it for time lamba.

        Input - conc_array, self.T, self.lamda
        output - true or false, changes self.Tfirst
        """
        if conc_array[int(self.x)][int(self.y)]>self.threshold:
            self.smell_timer = self.Timer(self.T,self.lamda)
            #Nav mode three and four need to know whether the moth is smelling
            #at a specific moment, for that reason they use Tfirst.
            self.Tfirst = self.T
            self.odor = True #this datum will be useful in the graphical functions
            return True
        elif self.turned_on:
            self.odor = False
            if self.smell_timer.is_running(self.T):
                return True #note - even though the there is no detection, the navigator stay in nav mode.
        else:
            self.odor = False
            return False

        
    class Timer(object):
        #timer starts at a certein time (t start)
        #for a set duration (self.duration)
        #at each moment a timer can be called upon to check whether that duration passed
        #return True/False
        def __init__(self,T_start,duration=10):
            self.T_start = T_start
            self.duration = duration
        def is_running(self,T_current):
            #takes in current time and compares to self.T_start. 
            #timer.is_running is True as long as the difference is smaller then the duration.
            return T_current - self.T_start < self.duration

    class Stopper(object):
        # a device for measuring the time passed between events
        # stopper.measure(self.T) returns the amount of time (simulated) passed since the stopper started
        def __init__(self,T_start):
            self.T_start = T_start
        def measure(self,T_stop):
            elasped = T_stop - self.T_start
            return elasped

    #motion functions are defined in advance
    def go_upwind(self,wind_vel_at_pos):
        self.calculate_wind_angle(wind_vel_at_pos)
        self.u = -self.speed*np.cos(self.wind_angle)
        self.v = self.speed*np.sin(self.wind_angle)

    def cast2(self,wind_vel_at_pos):
            #similar to nav_type 3
            #set timer as soon as moth isn't smelling odor, turn as soon as timer is over
            if not self.searching:
                #start timer
                self.timer = self.Timer(self.T,self.duration)
                self.searching = True
                self.duration = self.base_duration
            elif not self.timer.is_running(self.T):
                self.change_direction()
                self.timer = self.Timer(self.T,self.duration)                  
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
            #from Li,w. 2001 - strategy 2:  Constant crosswind with counterturn
            #if moth is currently in sensing odor, go upwind
            #if moth has sensed odor in the last lamda, traverse at angle
            if self.Tfirst == self.T:
                self.go_upwind(wind_vel_at_pos)
            else:
                self.calculate_wind_angle(wind_vel_at_pos)
                self.u = -self.speed*np.cos(self.beta + self.wind_angle)
                self.v = self.speed*np.sin(self.beta + self.wind_angle)
                
        if self.nav_type == 4:
            #from Li,w. 2001 -  strategy 3: Progressive crosswind with counterturn
            self.calculate_wind_angle(wind_vel_at_pos)
            if self.T-self.Tfirst < 0.1:
                self.beta = np.sign(self.beta)*np.radians(10)
            elif self.T-self.Tfirst < 0.3: #if 0.1<t-Tfirst<0.3
                self.beta = np.sign(self.beta)*np.radians(65)
            else: # if 0.3<t-Tfirst
                self.beta = np.sign(self.beta)*np.radians(80)
            self.u = -self.speed*np.cos(self.beta+self.wind_angle)
            self.v = self.speed*np.sin(self.beta+self.wind_angle)
        
        
        if self.nav_type == 'alex':
            if not self.last_dt_odor and self.odor: #the navigator just enters a plume
                self.new_stopper = self.Stopper(self.T)
                self.last_dt_odor = True
            if self.odor:
                time_in_plume = self.new_stopper.measure(self.T)
                self.lamda = time_in_plume
                self.duration = time_in_plume* self.alex_factor
            else:
                self.last_dt_odor= False
            self.go_upwind(wind_vel_at_pos)
            """
            self.last_dt_odor lets us the process of entering a plume
            a new stopper is started on in the event of entering a new plume
            note - in alex nav mode, the navigator can exit a plume and enter
            a new one without existing while still staying in navigation.
            for that reason, there needs to be a tracking of the odor in the last step
            """
            
              
        
        #after nav has been activated, the navigator cannot return to waiting mode
        #if it loses odor, it will start casting
        self.turned_on = True
        self.searching = False

    def cast(self,wind_vel_at_pos):
        if self.state != 'cast' :
            #if this is the beginging of a new casting phase
            self.change_direction()
            
        if self.cast_type == 0:
            self.u=0
            self.v=0
            
        if self.cast_type == 1:
            self.calculate_wind_angle(wind_vel_at_pos)
            self.u = -self.speed*np.cos(self.gamma+self.wind_angle)
            self.v = self.speed*np.sin(self.gamma+self.wind_angle)

        if self.cast_type == 2:
            #define different betas for different casting patterns
            self.cast2(wind_vel_at_pos)

        if self.cast_type == 3:
            if self.state != 'cast':
                #start timer
                self.timer = self.Timer(self.T,self.duration)
                self.searching = True
                self.duration = self.base_duration
            elif not self.timer.is_running(self.T):
                self.change_direction()
                self.timer = self.Timer(self.T,self.duration)
                self.duration *= 1.5
            self.calculate_wind_angle(wind_vel_at_pos)
            self.u = -self.speed*np.cos(self.gamma+self.wind_angle)
            self.v = self.speed*np.sin(self.gamma+self.wind_angle)
            
        if self.cast_type == 4:
            #same as cast_type 2, only gamma and duration change while flying
            self.update_gamma()
            self.update_duration()
            self.cast2(wind_vel_at_pos)

        if self.cast_type == 'carde1':
            carde1(self,wind_vel_at_pos)
            
        if self.cast_type == 'carde2':
            carde2(self,wind_vel_at_pos)

    def wait(self,wind_vel_at_pos):
        if self.wait_type == 1:
            self.u=0
            self.v=0

        if self.wait_type == 2:
            #coin toss between choosing to move left or right
            #wind angle, constant ground speed
            #traverse at 90 degrees to wind angle, no turns                 
            self.calculate_wind_angle(wind_vel_at_pos)
            self.u = -self.speed*np.cos(self.gamma+self.wind_angle)
            self.v = self.speed*np.sin(self.gamma+self.wind_angle)

        if self.wait_type == 'crw': #correlated random walk
            crw(self,wind_vel_at_pos)
    
                                     
    def update(self,conc_array,wind_vel_at_pos,dt):
        if self.T == 0: #because we want to start by casting
            self.smell_timer = self.Timer(self.T,dt)#start timer just not to bug out things later
            self.Tfirst = 0
        if self.is_smelling(conc_array):
            self.navigate(wind_vel_at_pos)
            self.state = 'nav' 
        elif self.turned_on:
            self.cast(wind_vel_at_pos)
            self.state = 'cast'
        else:
            self.wait(wind_vel_at_pos)
            self.state = 'wait'
        self.x += self.u*dt
        self.y += self.v*dt
        self.T += dt
        
    def moth_array(self, conc_array, wind_vel_at_pos):
        #draw moth position on matrix
        moth_array=np.zeros((500,1000))
        for i in range(10):
            for j in range(10):
                moth_array[int(self.x)-i][int(self.y)-j]=3e4
        if self.is_smelling(conc_array):
            for i in range(6):
                for j in range(6):
                    moth_array[int(self.x)-i-2][int(self.y)-j-2]=0
        #project moth unto same matrix as the concetration
        return conc_array + moth_array

