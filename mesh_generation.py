import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches  # used to show the bounding box in the matplotlib plot

#%%
NODE_AMOUNT_PER_AXIS = 10  # meaning in x and in y direction respectively

# Creates the nodes of the mesh
# Inputs: width and height of the domain
# Output: coordinates of the nodes
def createMesh(width, height):

    x_coords = np.zeros(NODE_AMOUNT_PER_AXIS**2, dtype=float)
    y_coords = np.zeros(NODE_AMOUNT_PER_AXIS**2, dtype=float)

    x_offset = width / (NODE_AMOUNT_PER_AXIS - 1)
    y_offset = height / (NODE_AMOUNT_PER_AXIS - 1)

    for i in range(NODE_AMOUNT_PER_AXIS):
        for j in range(NODE_AMOUNT_PER_AXIS):
            index = i * NODE_AMOUNT_PER_AXIS + j
            x_coords[index] = j * x_offset
            y_coords[index] = i * y_offset

    y_coords = y_coords[::-1]

    mesh_coords = np.column_stack((x_coords, y_coords))

    return mesh_coords

# visualizes the nodes of the mesh in a matplotlib-plot
# Input: coordinates of the nodes
def visualize_mesh(mesh_coords, line_coords):

    # Draws each point on the plot
    plt.scatter(mesh_coords[:, 0], mesh_coords[:, 1])

    # Draws the points of the line in red
    x_coords = [point[0] for point in line_coords]
    y_coords = [point[1] for point in line_coords]
    plt.scatter(x_coords, y_coords, color = 'r', label='Line')

    # Corner coordinate and Size of rectangle
    left, bottom = np.min(mesh_coords[:, 0]), np.min(mesh_coords[:, 1])
    width, height = np.max(mesh_coords[:, 0]) - np.min(mesh_coords[:, 0]), np.max(mesh_coords[:, 1]) - np.min(mesh_coords[:, 1])

    # Create a rectangle
    rect = patches.Rectangle((left, bottom), width, height, linewidth=1, edgecolor='r', facecolor='none')

    # Add the rectangle to the plot
    plt.gca().add_patch(rect)
       
    #plt.legend()   
    plt.show()
    return 0

