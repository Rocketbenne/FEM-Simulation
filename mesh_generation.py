import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches  # used to show the bounding box in the matplotlib plot

#%%
NODE_AMOUNT_PER_AXIS = 10  # meaning in x and in y direction respectively

# Creates the nodes of the mesh
# Inputs: width and height of the domain
# Output: coordinates of the nodes
def createMesh(width, height):

    x_coords = np.zeros(NODE_AMOUNT_PER_AXIS, dtype=float)
    y_coords = np.zeros(NODE_AMOUNT_PER_AXIS, dtype=float)

    x_offset = width / (NODE_AMOUNT_PER_AXIS - 1)
    y_offset = height / (NODE_AMOUNT_PER_AXIS - 1)

    for i in range(NODE_AMOUNT_PER_AXIS):
        x_coords[i] = i * x_offset
        y_coords[i] = i * y_offset

    y_coords = y_coords[::-1]  # reverses the array
    
    x_coords = np.repeat(x_coords, NODE_AMOUNT_PER_AXIS)
    y_coords = np.tile(y_coords, NODE_AMOUNT_PER_AXIS)

    mesh_coords = np.column_stack((x_coords, y_coords))

    return mesh_coords

# visualizes the nodes of the mesh in a matplotlib-plot
# Input: coordinates of the nodes
def visualize_mesh(mesh_coords):

    # Draws each point on the plot
    plt.scatter(mesh_coords[:, 0], mesh_coords[:, 1])

    # Corner coordinate and Size of rectangle
    left, bottom = np.min(mesh_coords[:, 0]), np.min(mesh_coords[:, 1])
    width, height = np.max(mesh_coords[:, 0]) - np.min(mesh_coords[:, 0]), np.max(mesh_coords[:, 1]) - np.min(mesh_coords[:, 1])

    # Create a rectangle
    rect = patches.Rectangle((left, bottom), width, height, linewidth=1, edgecolor='r', facecolor='none')

    # Add the rectangle to the plot
    plt.gca().add_patch(rect)
       
    plt.show()
    return 0
