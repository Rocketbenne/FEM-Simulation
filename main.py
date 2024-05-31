#%%
import numpy as np
import time as time
from scipy.sparse import coo_matrix
from sklearn.neighbors import BallTree
import sys

from input_handling import *
from mesh_generation import *
from finite_element import *

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
# Knotengleichungsarray / Node-Equation-Array
# Inputs: amount of nodes in the domain
#         coordinates of the domain 
# Output: Array containing node-equation-numbers
def get_node_equation_array(array_size, mesh_coords):

    node_equation_array = np.zeros(array_size, dtype=int)

    min_x = np.min(mesh_coords[:, 0])
    max_x = np.max(mesh_coords[:, 0])
    min_y = np.min(mesh_coords[:, 1])
    max_y = np.max(mesh_coords[:, 1])

    i, j = 0, 1  # i for indexing and j for value of globale gleichungsnummer
    for (x, y) in mesh_coords:
        #print(x, y)
        if(x != min_x and x != max_x and y != min_y and y != max_y):
            node_equation_array[i] = j
            j += 1
        i += 1

    # converts mesh_coords to tuples, tuples can be indexed using tuple[0] and tuple[1]
    #mesh_coords_tuples = [tuple(coord) for coord in mesh_coords]

    #TODO: unsure if dict is good to use here, maybe tuple would be better
    #return dict(zip(mesh_coords_tuples, node_equation_array))  

    # just returns node_equation_array atm
    return node_equation_array

# Gleichungsarray / Equation-Array
# Inputs: array containing the finite elements of the domain
#         local node number [1 -4]
#         element number
# Output: global equation number
def EQ(finite_elements, local_number, element_number):
    return finite_elements[element_number - 1].get_global_node_numbers()[local_number - 1]


#%%

width, height, order_num_int = getGeometryInputs_hard_coded()

# creates the mesh with all the nodes
mesh_coords = createMesh(width, height)

# gets amount of coordinate pairs
array_size = mesh_coords.shape[0]  

# creates the array containing the node-equations
NE_array = get_node_equation_array(array_size, mesh_coords)

# creates the finite elements of the domain
finite_elements = element_generation(NE_array, NODE_AMOUNT)


# Testing
visualize_mesh(mesh_coords)

print(NE_array)

print('--------------------------------------')

for i in range((NODE_AMOUNT-1)**2):
    print(finite_elements[i].get_global_element_number(), finite_elements[i].get_global_node_numbers())

print(EQ(finite_elements, 3, 39))
print(EQ(finite_elements, 4, 63))

