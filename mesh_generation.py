import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches  # used to show the bounding box in the matplotlib plot



#%%
# Create the Net/Mesh with all it's nodes
# Returns coodinates of the nodes

def createMesh(width, height):

    node_amount = 10  # meaning in x and in y direction respectively

    x_coords = np.zeros(node_amount, dtype=float)
    y_coords = np.zeros(node_amount, dtype=float)

    x_offset = width / (node_amount - 1)
    y_offset = height / (node_amount - 1)

    for i in range(node_amount):
        x_coords[i] = i * x_offset
        y_coords[i] = i * y_offset
    
    x_coords = np.repeat(x_coords, node_amount)
    y_coords = np.tile(y_coords, node_amount)

    mesh_coords = np.column_stack((x_coords, y_coords))

    return mesh_coords

def visualize_mesh(mesh_coords):

    # Draws each point on the plot
    plt.scatter(mesh_coords[:, 0], mesh_coords[:, 1])

    # Edges and Size of rectangle
    left, bottom = np.min(mesh_coords[:, 0]), np.min(mesh_coords[:, 1])
    width, height = np.max(mesh_coords[:, 0]) - np.min(mesh_coords[:, 0]), np.max(mesh_coords[:, 1]) - np.min(mesh_coords[:, 1])

    # Create a rectangle
    rect = patches.Rectangle((left, bottom), width, height, linewidth=1, edgecolor='r', facecolor='none')

    # Add the rectangle to the plot
    plt.gca().add_patch(rect)
       
    plt.show()
    return 0