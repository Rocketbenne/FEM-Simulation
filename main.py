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
boundary_conditions = [[Type.Dirichlet.value, 0],[Type.Dirichlet.value, 10],[Type.Dirichlet.value, 0],[Type.Dirichlet.value, -10],[Type.Dirichlet.value, 0]]


#%%

width, height, order_num_int = getGeometryInputs_hard_coded()

line_start, line_end, line_value_function = getLineInputs_hard_coded()

# creates the mesh with all the nodes
mesh_coords = createMesh(width, height)

# gets amount of coordinate pairs
array_size = mesh_coords.shape[0]

# get the coordinates of the Line
line_coords = []
#line_coords = getLineCoordinates(line_start, line_end, mesh_coords)
# TODO: if for this line_coords, so that it is choosable to have a line or not

if line_coords:  # checks if list is not empty
    line_values = getLineValues(line_coords, line_value_function)


# creates the array containing the node-equations
NE_array = get_node_equation_array(array_size, mesh_coords, line_coords)

# creates the finite elements of the domain
finite_elements = element_generation(NE_array, NODE_AMOUNT_PER_AXIS, height, width, boundary_conditions)
# System-matrix K
K = np.zeros([array_size, array_size])

boundary_nodes = get_boundary_nodes(mesh_coords,width,height)

#for element in finite_elements:
#     print(element.get_global_element_number())
#     print(element.get_global_node_numbers())
#     print(element.get_boundaries())
     #print(element.get_global_coords())



# apply_boundary_conditions()
mat_tensor = np.array([[1, 1], [1, 1]])
order = 4
rho = 1
rhs = np.zeros(array_size)
K, rhs = assembling_algorithm2(finite_elements, 4, K, rhs, mat_tensor, order, rho)
#rhs = np.zeros(array_size)

#Resize the Arrays to the size we need them by cutting away the 0 entries

with open('matrix.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(K)

#K = K[:array_size-line_values.size - 36, :array_size-line_values.size -36]
#rhs = rhs[:array_size-line_values.size -36]
K = K[:array_size - 36, :array_size - 36]
rhs = rhs[:array_size - 36]


values = np.zeros([array_size])


u = np.linalg.solve(K, rhs)


#global_node_numbers_list = []
#for element in finite_elements:

    #new_order = np.array([element.get_global_node_numbers()[3], element.get_global_node_numbers()[2], element.get_global_node_numbers()[0], element.get_global_node_numbers()[1]])
#    new_order = np.array([element.get_global_coords()[2], element.get_global_coords()[3], element.get_global_coords()[0], element.get_global_coords()[1]])
#    global_node_numbers_list.append(new_order)
    #print(element.get_global_node_numbers())
    #print(new_order)
    #print("--")
#global_node_numbers_array = np.array(global_node_numbers_list)
#print(global_node_numbers_array)

# versuach: fa jeden element die 4 knotennummern ungeben, wobei die knoten fa 0 bis 100 gian
global_node_numbers_list = []
for j in range(0, 9):
     for i in range(0, 9):
          arr = np.array([NODE_AMOUNT_PER_AXIS *(j+1) + i, NODE_AMOUNT_PER_AXIS*(j+1) + (i+1), NODE_AMOUNT_PER_AXIS *(j) + i, NODE_AMOUNT_PER_AXIS *(j) + (i+1)])
          global_node_numbers_list.append(arr)
        
global_node_numbers_array = np.array(global_node_numbers_list)



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


export_writer = EXPORT(4,                       # Nodes per Element
                       len(finite_elements),    # Amount of Elements
                       array_size,              # Amount of Nodes
                       2,                       # Dimension (2D)
                       out,                     # Result Vector
                       mesh_coords,             # Node Coordinates
                       global_node_numbers_array, # global knot number of each element
                       1)                       # Degree of Freedom per Node

export_writer.writeResults()

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

for i, value in enumerate(u):
        writer.writerow({'coordinates': mesh_coords[i], 'value': u<[i]})

# %%
