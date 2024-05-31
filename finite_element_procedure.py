import numpy as np

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

