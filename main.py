#%%
import matplotlib.pyplot as plt
import numpy as np
import csv

from input_handling import *
from mesh_generation import *
from finite_element import *
from finite_element_procedure import *
from line import *
from boundary_condition import *

#%%

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
boundary_conditions = [[Type.Dirichlet.value, 1],[Type.Dirichlet.value, 2],[Type.Dirichlet.value, 3],[Type.Dirichlet.value, 4],[Type.Dirichlet.value, 5]]


#%%

width, height, order_num_int = getGeometryInputs_hard_coded()

line_start, line_end, line_value_function = getLineInputs_hard_coded()

# creates the mesh with all the nodes
mesh_coords = createMesh(width, height)

# get the coordinates of the Line
line_coords = getLineCoordinates(line_start, line_end, mesh_coords)
# TODO: if for this line_coords, so that it is choosable to have a line or not

line_values = getLineValues(line_coords, "{x}+{y}")

# gets amount of coordinate pairs
array_size = mesh_coords.shape[0]

# creates the array containing the node-equations
NE_array = get_node_equation_array(array_size, mesh_coords, line_coords)

# creates the finite elements of the domain
finite_elements = element_generation(NE_array, NODE_AMOUNT_PER_AXIS, height, width, boundary_conditions)
# System-matrix K
K = np.zeros([array_size, array_size])

boundary_nodes = get_boundary_nodes(mesh_coords,width,height)




# apply_boundary_conditions()
mat_tensor = np.array([[1, 1], [1, 1]])
order = 4
rho = 1
rhs = np.zeros(array_size)
K, rhs = assembling_algorithm2(finite_elements, 4, K, rhs, mat_tensor, order, rho)

#Resize the Arrays to the size we need them by cutting away the 0 entries
K = K[:array_size-line_values.size - 36, :array_size-line_values.size -36]
rhs = rhs[:array_size-line_values.size -36]

values = np.zeros([array_size])

#K,values = apply_boundary_conditions(K,values, boundary_conditions, boundary_nodes,width,height)




# Testing
visualize_mesh(mesh_coords, line_coords)
np.linalg.solve(K,rhs)
#print(NE_array)

# print('--------------------------------------')

# for i in range((NODE_AMOUNT_PER_AXIS - 1)**2):
#    print(finite_elements[i].get_global_element_number(), finite_elements[i].get_global_node_numbers())

# print(EQ(finite_elements, 3, 39))
# print(EQ(finite_elements, 4, 63))

# print("-------------------")
# print(boundary_nodes)




# Write values to a .csv file
filename = 'program_output.csv'

file = open(filename, 'w', newline='')

fields = ['coordinates', 'value']
writer = csv.DictWriter(file, fieldnames=fields, delimiter=';')
writer.writeheader()

for i, value in enumerate(values):
        writer.writerow({'coordinates': mesh_coords[i], 'value': values[i]})

# %%
