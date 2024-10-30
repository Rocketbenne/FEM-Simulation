import numpy as np
import boundary_condition as bc

'''
Numbering of Fem_Knots and Elements

Global Node and Equation Numbers
From left top to right top, then next row to the right ( as one reads )
Local Node Numbers starting from bottom left in a counter-clockwise rotation

    1---------2---------3
    | 4     3 | 4     3 |
    |    1    |    2    |
    | 1     2 | 1     2 |
    4---------5---------6
    | 4     3 | 4     3 |
    |    3    |    4    |
    | 1     2 | 1     2 |
    7---------8---------9

    Outest Layer: Global Node Number
    Second Layer: Local Node Number
    Number in the Middle: Global Element Number

'''


class FEM_Element:
    def __init__(self, global_element_number, global_node_numbers, global_cords, boundaries=None):
        self.global_element_number = global_element_number
        self.global_node_numbers = global_node_numbers
        self.global_cords = global_cords
        self.boundaries = boundaries

    def get_global_node_numbers(self):
        return self.global_node_numbers

    def get_global_element_number(self):
        return self.global_element_number

    def get_global_coords(self):
        return self.global_cords

    def get_boundaries(self):
        return self.boundaries


# Generation of the finite elements in the domain
# Inputs: Array containing the the node equation numbers
#         amount of nodes per axis
# Output: Array containing the finite Elements
def element_generation(dimension, height, width, amount_of_nodes_per_axis):
    elements = np.empty((dimension - 1) ** 2, dtype=FEM_Element)

    delta_x = width / (dimension - 1)
    delta_y = height / (dimension - 1)

    element_number = 1
    for y in range(dimension - 1):
        for x in range(dimension - 1):
            
            node_numbers = np.array([[bc.find_global_node_nr([x*delta_x,height - (y+1)*delta_y],width,height, amount_of_nodes_per_axis)],
                                     [bc.find_global_node_nr([(x+1)*delta_x,height - (y+1)*delta_y],width,height, amount_of_nodes_per_axis)],
                                     [bc.find_global_node_nr([(x+1)*delta_x,height - y*delta_y],width,height, amount_of_nodes_per_axis)],
                                     [bc.find_global_node_nr([x*delta_x,height - y*delta_y],width,height, amount_of_nodes_per_axis)]])

            global_coords = np.array([[delta_x * ((element_number - 1) % (dimension - 1)), height - y * delta_y - delta_y],
                                    [delta_x * ((element_number - 1) % (dimension - 1)) + delta_x, height - y * delta_y - delta_y],
                                    [delta_x * ((element_number - 1) % (dimension - 1)) + delta_x, height - y * delta_y],
                                      [delta_x * ((element_number - 1) % (dimension - 1)), height - y * delta_y]])
            

            elements[element_number - 1] = FEM_Element(element_number, node_numbers, global_coords)
            element_number += 1

    return elements

