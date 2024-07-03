
# We set:
#   - Dirichlet Boundary conditions on the left with value 0
#   - Dirichlet Boundary conditions on the right with value 9
#   - Upper and lower bounds have values [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]: f(x) = x
#   - No line in the domain

# Result should be a linear function from left to right with increasing temperature

# In the csv-file we write:
#   - the coordinates of each node
#   - the calculated value for each node
#   - nodes and values are beeing traversed from top left to bottom right 
#     as one reads

import numpy as np
import csv
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mesh_generation import *

mesh = createMesh(9, 9, 10)

values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
values = np.tile(values, 10)

# Write values to a .csv file
filename = 'tests/reference.csv'

file = open(filename, 'w', newline='')

fields = ['coordinates', 'value']
writer = csv.DictWriter(file, fieldnames=fields, delimiter=';')
writer.writeheader()

for i, value in enumerate(values):
        writer.writerow({'coordinates': mesh[i], 'value': values[i]})
