
'''
Functions for making knots, returning a set of points.
'''

import numpy as np

from pyknot2.make import knot

def trefoil(slip_length=30):

    data = knot.trefoil() * 5

    return np.vstack((data[:-2], data[-slip_length:-2][::-1] + 1.5))

    
