#%%
import numpy as np
import time as time
from scipy.sparse import coo_matrix
from sklearn.neighbors import BallTree
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches  # used to show the bounding box in the matplotlib plot

from input_handling import *
from mesh_generation import *

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
# Knotengleichungsarray
def get_node_equation_array(array_size, mesh_coords):

    globale_gleichungsnummer = np.zeros(array_size, dtype=int)

    min_x = np.min(mesh_coords[:, 0])
    max_x = np.max(mesh_coords[:, 0])
    min_y = np.min(mesh_coords[:, 1])
    max_y = np.max(mesh_coords[:, 1])

    i, j = 0, 1  # i for indexing and j for value of globale gleichungsnummer
    for (x, y) in mesh_coords:
        #print(x, y)
        if(x != min_x and x != max_x and y != min_y and y != max_y):
            globale_gleichungsnummer[i] = j
            j += 1
        i += 1

    # converts mesh_coords to tuples, tuples can be indexed using tuple[0] and tuple[1]
    mesh_coords_tuples = [tuple(coord) for coord in mesh_coords]

    return dict(zip(mesh_coords_tuples, globale_gleichungsnummer))   



#%%

width, height, order_num_int = getGeometryInputs_hard_coded()

mesh_coords = createMesh(width, height)

visualize_mesh(mesh_coords)

array_size = mesh_coords.shape[0]  # gets amount of coordinate pairs

NE_array = get_node_equation_array(array_size, mesh_coords)

#print(NE_array)
