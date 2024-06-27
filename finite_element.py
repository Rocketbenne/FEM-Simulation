import numpy as np

class FEM_Element:
    def __init__(self, global_element_number, global_node_numbers, global_cords, boundaries = None):
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
def element_generation(node_equation_array, dimension, height, width, boundary_conditions = None):
    elements = np.empty((dimension - 1)**2, dtype=FEM_Element)

    delta_x = width / (dimension - 1)
    delta_y = height / (dimension - 1)

    element_number = 1
    for y in range(dimension - 1):
        for x in range(dimension - 1):
            node_numbers = np.array([node_equation_array[dimension * (y+1) + x], 
                                        node_equation_array[dimension * (y+1) + (x+1)], 
                                        node_equation_array[dimension * y + (x+1)], 
                                        node_equation_array[dimension * y + x]])

            global_coords = np.array([[delta_x*((element_number - 1) % (dimension-1)),height - y * delta_y],
                                     [delta_x*((element_number - 1) % (dimension-1)) + delta_x, height - y * delta_y],
                                     [delta_x*((element_number - 1) % (dimension-1)), height - y * delta_y - delta_y],
                                     [delta_x*((element_number - 1) % (dimension-1)) + delta_x, height - y * delta_y - delta_y]])
            
            '''
            # Anordnung Globale Koordinaten
            0  -----  1
               |   |
            2  -----  3

            # Anordnung Node-Numbers
            3  -----  2
               |   |
            0  -----  1
            '''

            boundaries = np.zeros([4, 2])
            for i in range(4):
                if node_numbers[i] == 0:
                    if i == 0:  # Umrechnung Anordnung Node-Numbers --> Anordnung Globale Koordinaten
                        i = 2
                    elif i == 1:
                        i = 3
                    elif i == 2:
                        i = 1
                    elif i == 3:
                        i = 0
                    #The corner values are set by the left or right boundary conditon from the recatangle
                    if global_coords[i][0] == 0 and global_coords[i][1] == 0:  # edge cases
                        boundaries[i] = boundary_conditions[3]
                    elif global_coords[i][0] == width and global_coords[i][1] == 0:
                        boundaries[i] = boundary_conditions[2]
                    elif global_coords[i][0] == width and global_coords[i][1] == height:
                        boundaries[i] = boundary_conditions[1]
                    elif global_coords[i][0] == 0 and global_coords[i][1] == height:
                        boundaries[i] = boundary_conditions[0]
                    
                    elif global_coords[i][0] == 0:  # sides
                        boundaries[i] = [boundary_conditions[3][0], boundary_conditions[3][1]]
                    elif global_coords[i][0] == width:
                        boundaries[i] = [boundary_conditions[1][0], boundary_conditions[1][1]]
                    elif global_coords[i][1] == 0:
                        boundaries[i] = [boundary_conditions[2][0], boundary_conditions[2][1]]
                    elif global_coords[i][1] == height:
                        boundaries[i] = [boundary_conditions[0][0], boundary_conditions[0][1]]
                    else:
                        boundaries[i] = [boundary_conditions[4][0], boundary_conditions[4][1]]
            elements[element_number - 1] = FEM_Element(element_number, node_numbers, global_coords, boundaries)
            element_number += 1

    return elements

