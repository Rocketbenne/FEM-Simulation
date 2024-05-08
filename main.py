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
    width, height, number_of_net_points, order_num_int = 90, 20, 30, 1

    return width, height, number_of_net_points, order_num_int

def createQuadNet(width, height, number_of_net_points):

    FEM_knots = np.array(number_of_net_points, FEM_Knot)  #creates an array of FEM-Knots
    y_amount = width / number_of_net_points  # amount of knots in y-direction
    x_amount = (number_of_net_points/y_amount)
    y_offset = height / (y_amount - 1)  # -1 because first knot is on height y = 0
    x_offset = width / (x_amount - 1)
    global_knot_number = 1
    global_equation_number = 1
    for i in range(x_amount):
        for j in range(y_amount):
            if(i != 0 & i != x_amount & j != 0 & j != y_amount):
                knot = FEM_Knot(i * x_offset, j * y_offset, global_knot_number, global_equation_number)
                global_equation_number += 1
            else:
                knot = FEM_Knot(i * x_offset, j * y_offset, global_knot_number, 0)
            global_knot_number += 1
            FEM_knots[global_knot_number] = knot


    FEM_Elements = []  # List of FEM Elements so that .append() works

    # create each fem element and add to FEM_Elements


    FEM_Elements = np.array(FEM_Elements)  # Converts List to Numpy Array

    return FEM_knots, FEM_Elements


#%%

width, height, number_of_net_points, order_num_int = getGeometryInputs()
QUAD_net = createQuadNet(width, height, number_of_net_points)

