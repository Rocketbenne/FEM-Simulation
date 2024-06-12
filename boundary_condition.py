#Class for boundary conditions containing value and type of bc(Dirilecht or Neumann)
import numpy as np
class BoundaryCondition:
    def __init__(self,value,bc_type):
        self.value = value
        self.bc_type = bc_type 

#Extracts the boundary nodes and returns them as 2D Array where row is for left,top,right,bottom
# and the col is another array with the corresponding nodes
# Of each side left side is the corner from inside perspective
''''
    left:    Node    Node    Node    Node ..... 
    top:    Node    Node    Node    Node ....
    right:  Node    ...
    bottom: Node    ...
'''
def get_boundary_nodes(mesh_coords,width,height):
    x_values = mesh_coords[:, 0]  # Extract all x-coordinates
    y_values = mesh_coords[:, 1]  # Extract all y-coordinates

    left_nodes = mesh_coords[(x_values == 0)  & (y_values != height), :]  
    right_nodes = mesh_coords[(x_values == width) & (y_values != 0), :]  
    top_nodes = mesh_coords[(x_values != width) & (y_values == height), :]  
    bottom_nodes = mesh_coords[(x_values != 0) & (y_values == 0), :]  
    
    boundary_nodes = (left_nodes,top_nodes,right_nodes,bottom_nodes)
    return np.array(boundary_nodes)

def apply_boundary_conditions(system_matrix,boundary_conditions,boundary_nodes):
    raise NotImplementedError