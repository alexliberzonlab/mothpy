from __future__ import division

__authors__ = 'Noam Benelli'
from simulation import moth_simulation
from kalman import kalman_filter 
from moth_graphics import plot


num_it = 1#number of iteration
diff_dict = moth_simulation(num_it)
kalman_dict = kalman_filter(diff_dict)
plot(kalman_dict,num_it)


