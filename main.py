#%%
import numpy as np
import time as time
from scipy.sparse import coo_matrix
from sklearn.neighbors import BallTree
import sys

from input_handling import *
from mesh_generation import *
from finite_element import *
from finite_element_procedure import *

#%%

'''
Numbering of Fem_Knots and Elements 

Global Knot and Equation Numbers
From left top to right top, then next row to the right ( as one reads )
Local Knot Numbers starting from bottom right in a counter-clockwise rotation

    1---------2---------3
    | 4     3 | 4     3 |
    |    1    |    2    |
    | 1     2 | 1     2 |
    4---------5---------6
    | 4     3 | 4     3 |
    |    3    |    4    |
    | 1     2 | 1     2 |
    7---------8---------9

    Outest Layer: Global Knot Number
    Second Layer: Local Knot Number
    Number in the Middle: Global Element Number

'''





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

assembling_algorithm(finite_elements, array_size)


# Testing
visualize_mesh(mesh_coords)

print(NE_array)

print('--------------------------------------')

for i in range((NODE_AMOUNT-1)**2):
    print(finite_elements[i].get_global_element_number(), finite_elements[i].get_global_node_numbers())

print(EQ(finite_elements, 3, 39))
print(EQ(finite_elements, 4, 63))

