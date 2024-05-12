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

    Outest Layer: Global Knot Number
    Second Layer: Local Knot Number
    Number in the Middle: Global Element Number

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

# used for testing the program, just wirte the values in here
def getGeometryInputs_hard_coded():
    width, height, number_of_net_points, order_num_int = 90, 20, 30, 1

    return width, height, number_of_net_points, order_num_int

# for finished version, lets user input values and error-checks them
def getGeometryInputs():
    width, height, number_of_net_points, order_num_int = 0, 0, 0, 0

    print("Input the Width: ")
    width = getNumberFromUser()
    print("Input the Height: ")
    height = getNumberFromUser()
    print("Input the Number of Net-Points: ")
    number_of_net_points = getNumberFromUser()
    print("Input the Order of the Numerical Integration: ")
    order_num_int = getNumberFromUser()

    return width, height, number_of_net_points, order_num_int

# get a number from the user throught the console and makes error checks
def getNumberFromUser():
    while(1):
        number = input()
        if(number.isnumeric()):  # checks if value is numeric
            if(int(number) > 0):  # checks if numeric value is greater than 0
                return int(number)
        print("\nPlease enter a Number greater than 0.\n")

# creates all instances of FEM-Knots and FEM-Elements
def createQuadNet(width, height, number_of_net_points):

    FEM_knots = np.empty(number_of_net_points, FEM_Knot)  #creates an array of FEM-Knots
    
    y_amount = int(width / number_of_net_points)  # amount of knots in y-direction
    x_amount = int(number_of_net_points/y_amount)

    # PRODUCES DIVISION BY ZERO ERROR IF WIDTH = NUMBER_OF_NET_POINTS
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
            FEM_knots[global_knot_number - 1] = knot  # -1 because variable is 1 at start
            global_knot_number += 1

    # TODO: Test with weird numers, (things that make uneven amounts etc)
    # TODO: Maybe change inputs of amount of knots to 2 Inputs, one in x and one in y
    
    # Test Output to Check if Knots are correctly placed 
    #for x in FEM_knots: 
    #    if(isinstance(x, FEM_Knot)):
    #        print("X " + str(x.pos_x) + "  Y " + str(x.pos_y))


    FEM_Elements = []  # List of FEM Elements so that .append() works

    # create each fem element and add to FEM_Elements


    FEM_Elements = np.array(FEM_Elements)  # Converts List to Numpy Array

    return FEM_knots, FEM_Elements


#%%

width, height, number_of_net_points, order_num_int = getGeometryInputs_hard_coded()
QUAD_net = createQuadNet(width, height, number_of_net_points)

