#%%
import numpy as np
import time as time
from scipy.sparse import coo_matrix
from sklearn.neighbors import BallTree
import csv

from input_handling import *
from mesh_generation import *
from finite_element import *
from finite_element_procedure import *

#%%

'''
Numbering of Fem_Knots and Elements 

Global Node and Equation Numbers
From left top to right top, then next row to the right ( as one reads )
Local Node Numbers starting from bottom right in a counter-clockwise rotation

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





#%%

width, height, order_num_int = getGeometryInputs_hard_coded()

# creates the mesh with all the nodes
mesh_coords = createMesh(width, height)
print(mesh_coords)
# gets amount of coordinate pairs
array_size = mesh_coords.shape[0]

# creates the array containing the node-equations
NE_array = get_node_equation_array(array_size, mesh_coords)

# creates the finite elements of the domain
finite_elements = element_generation(NE_array, NODE_AMOUNT_PER_AXIS)

# System-matrix K
K = np.zeros([array_size, array_size])

assembling_algorithm(finite_elements, 4, K)


# Testing
#visualize_mesh(mesh_coords)

#print(NE_array)

#print('--------------------------------------')

#for i in range((NODE_AMOUNT_PER_AXIS - 1)**2):
#    print(finite_elements[i].get_global_element_number(), finite_elements[i].get_global_node_numbers())

#print(EQ(finite_elements, 3, 39))
#print(EQ(finite_elements, 4, 63))

# array containing the solutions in each node
values = np.zeros([array_size])

# Write values to a .csv file
filename = 'program_output.csv'

file = open(filename, 'w', newline='')

fields = ['coordinates', 'value']
writer = csv.DictWriter(file, fieldnames=fields, delimiter=';')
writer.writeheader()

for i, value in enumerate(values):
        writer.writerow({'coordinates': mesh_coords[i], 'value': values[i]})
