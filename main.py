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





#%%

width, height, order_num_int = getGeometryInputs_hard_coded()

mesh_coords = createMesh(width, height)

visualize_mesh(mesh_coords)