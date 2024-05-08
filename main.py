#%%
import numpy as np
import time as time
from scipy.sparse import coo_matrix
from sklearn.neighbors import BallTree
import sys
import matplotlib.pyplot as plt

#%%

'''
Numbering of Fem_Knots and Elements as shown in VO

Global Knot and Equation Numbers
From left bottom to left top, then next column to the right
Local Knot Numbers starting from bottom right in a counter-clockwise rotation

    3---------6---------9
    | 4     3 | 4     3 |
    |    2    |    4    |
    | 1     2 | 1     2 |
    2---------5---------8
    | 4     3 | 4     3 |
    |    1    |    3    |
    | 1     2 | 1     2 |
    1---------4---------7

'''


class FEM_Knot:
    def __init__(self, pos_x, pos_y, global_knot_number, global_equation_number):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.global_knot_number = global_knot_number
        self.global_equation_number = global_equation_number

# Global knot numbers should be inputed in the order of the local knot numbers
class FEM_Element:
    def __init__(self, global_element_number, global_knot_numbers, value, derivation_value):
        self.global_element_number = global_element_number
        self.global_knot_numbers = global_knot_numbers
        self.value = value
        self.derivation_value = derivation_value



#%%
# First we let the user "input" be done throught putting numbers in the variables
# Later on we might do it throught the cmd or a pop-up-window

def getGeometryInputs():
    length, width, number_of_net_points, order_num_int = 100, 20, 30, 1

    return length, width, number_of_net_points, order_num_int

def createQuadNet(length, width, number_of_net_points):

    FEM_knots = np.array(number_of_net_points, FEM_Knot)  #creates an array of FEM-Knots

    return FEM_knots


#%%

length, width, number_of_net_points, order_num_int = getGeometryInputs()
QUAD_net = createQuadNet(length, width, number_of_net_points)

