#%%
import numpy as np
import csv

from input_handling import *
from mesh_generation import *
from finite_element import *
from finite_element_procedure import *
from line import *
from exportRes import *

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

#%%

order = 4
rho = 1

width, height, order_num_int = getGeometryInputs_hard_coded()

#line_start, line_end, line_value_function = getLineInputs(width, height)

#mat_tensor = getMaterialTensor()

#boundary_conditions_ = getBCInputs()

"""boundary_conditions = [[boundary_conditions_[0][0],boundary_conditions_[0][1]],
[boundary_conditions_[1][0],boundary_conditions_[1][1]],[boundary_conditions_[2][0],boundary_conditions_[2][1]],
[boundary_conditions_[3][0],boundary_conditions_[3][1]],[Type.Dirichlet.value, 0]]"""



# creates the mesh with all the nodes
mesh_coords = createMesh(width, height)

# gets amount of coordinate pairs
array_size = mesh_coords.shape[0]

# get the coordinates of the Line
line_coords = []
line_coords = getLineCoordinates(line_start, line_end, mesh_coords)

line_values = []
if line_coords:  # checks if list is not empty
    line_values = getLineValues(line_coords, line_value_function)


# creates the array containing the node-equations
NE_array = get_node_equation_array(array_size, mesh_coords, line_coords)

# creates the finite elements of the domain
finite_elements = element_generation(NE_array, NODE_AMOUNT_PER_AXIS, height, width, boundary_conditions)
# System-matrix K

K = np.zeros([array_size, array_size])

rhs = np.zeros(array_size)
K, rhs = assembling_algorithm(finite_elements, 4, K, rhs, mat_tensor, order, rho)



with open('matrix.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(K)

#Resize the Arrays to the size we need them by cutting away the 0 entries
K = K[:array_size - len(line_values) - 36, :array_size - len(line_values) - 36]
rhs = rhs[:array_size - len(line_values) - 36]

u = np.linalg.solve(K, rhs)

# Add togheter the calculated values of the Nodes with Node-Equation-Numbers with the Boundaries
counter = 0
out = []
for i in range(9):
    out.append(boundary_conditions[0][1])
for i in range(8):
     out.append(boundary_conditions[1][1])
     out.append(boundary_conditions[3][1])
     for j in range(8):
        out.append(u[counter]) 
        counter += 1
out.append(boundary_conditions[1][1])
out.append(boundary_conditions[3][1])
for i in range(9):
    out.append(boundary_conditions[2][1])

out = np.array(out)


# Node Connectivity Matrix
global_node_numbers_list = []
for j in range(0, 9):
     for i in range(0, 9):
          arr = np.array([NODE_AMOUNT_PER_AXIS *(j+1) + i, NODE_AMOUNT_PER_AXIS*(j+1) + (i+1), NODE_AMOUNT_PER_AXIS *(j) + i, NODE_AMOUNT_PER_AXIS *(j) + (i+1)])
          global_node_numbers_list.append(arr)
        
global_node_numbers_array = np.array(global_node_numbers_list)

# Export Writer
export_writer = EXPORT(4,                       # Nodes per Element
                       len(finite_elements),    # Amount of Elements
                       array_size,              # Amount of Nodes
                       2,                       # Dimension (2D)
                       out,                     # Result Vector
                       mesh_coords,             # Node Coordinates
                       global_node_numbers_array, # Node Connectivity Matrix
                       1)                       # Degree of Freedom per Node

export_writer.writeResults()


# Write values to a .csv file for the CI-CD System
filename = 'program_output.csv'

file = open(filename, 'w', newline='')

fields = ['coordinates', 'value']
writer = csv.DictWriter(file, fieldnames=fields, delimiter=';')
writer.writeheader()

for i, value in enumerate(out):
        writer.writerow({'coordinates': mesh_coords[i], 'value': out[i]})

# %%
