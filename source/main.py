# %%
import numpy as np
import csv
import time

from input_handling import *
from mesh_generation import *
from finite_element import *
from finite_element_procedure import *
from line import *
from exportRes import *

import argparse
from ast import literal_eval

# %%

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

def create_line_coords_and_values(mesh_coords, line_start, line_end, amount_of_line_points, line_value, line_bool):
    '''Creates the Coordinates and their respective Values for the Line'''

    # get the coordinates of the Line
    line_coords = []
    line_coords = getLineCoordinates(line_start, line_end, mesh_coords, amount_of_line_points, line_bool)

    line_values = []
    if line_coords:  # checks if list is not empty
        line_values = getLineValues(line_coords, line_value)            # old line_value_function

    return line_coords, line_values


def stiffness_matrix(mesh_coords, array_size, mat_tensor, order_num_int, boundary_conditions, width, height, amount_of_nodes_per_axis, line_coords, line_values):

    rho = 1  # TODO what does Rho do... despite beeing value in calculation

    K = np.zeros([array_size, array_size])

    rhs = np.zeros(array_size)
    K, rhs = assembling_algorithm(finite_elements, 4, K, rhs, mat_tensor, order_num_int, rho)
    K, rhs = bc.apply_boundary_conditions(K, rhs, boundary_conditions, bc.get_boundary_nodes(mesh_coords,width,height), width, height, amount_of_nodes_per_axis)
    K, rhs = apply_line_values(K, rhs, mesh_coords, line_coords, line_values)

    u = np.linalg.solve(K, rhs)

    return K, u


def node_connectivity_matrix(amount_of_nodes_per_axis):
    # Node Connectivity Matrix
    global_node_numbers_list = []
    for j in range(0, amount_of_nodes_per_axis - 1):
        for i in range(0, amount_of_nodes_per_axis - 1):
            arr = np.array([amount_of_nodes_per_axis *(j+1) + i, amount_of_nodes_per_axis*(j+1) + (i+1), amount_of_nodes_per_axis *(j) + i, amount_of_nodes_per_axis *(j) + (i+1)])
            global_node_numbers_list.append(arr)

    global_node_numbers_array = np.array(global_node_numbers_list)

    return global_node_numbers_array


def write_files(finite_elements, array_size, result_vector, mesh_coords, node_connectivity_matrix, out_file_name):
    '''Writes results to different files'''

    out_file_name = 'results/' + out_file_name      # Create File in results-Folder

    # Export Writer
    export_writer = EXPORT( 4,                          # Nodes per Element
                            len(finite_elements),       # Amount of Elements
                            array_size,                 # Amount of Nodes
                            2,                          # Dimension (2D)
                            result_vector,              # Result Vector                 # TODO old u
                            mesh_coords,                # Node Coordinates              # old mesh_coords
                            node_connectivity_matrix,   # Node Connectivity Matrix      # old global_node_numbers_array
                            1)                          # Degree of Freedom per Node                          

    export_writer.writeResults(out_file_name)


    # Write values to a .csv file for the CI-CD System
    filename = out_file_name + '.csv'

    file = open(filename, 'w', newline='')

    fields = ['coordinates', 'value']
    writer = csv.DictWriter(file, fieldnames=fields, delimiter=';')
    writer.writeheader()

    for i, _ in enumerate(result_vector):
        writer.writerow({'coordinates': mesh_coords[i], 'value': result_vector[i]})                     # old mesh_coords, result_vector


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Input values for the Finite-Element-Method Simulation")  # TODO formatter_class=argparse.ArgumentDefaultsHelpFormatter

    req_args = parser.add_argument_group('Base Parameters')
    opt_args = parser.add_argument_group('Optional Parameters')

    # Output File Name
    req_args.add_argument('--name',           type=str,   help="Name of the output-files",            default='results')

    # Basic Inputs
    req_args.add_argument('--width',          type=int,   help="Width of the Domain",                 default=100)
    req_args.add_argument('--height',         type=int,   help="Height of the Domain",                default=100)
    req_args.add_argument('--order_num_int',  type=int,   help="Order of the Numerical Integration",  default=3)      
    req_args.add_argument('--nodes_per_axis', type=int,   help="Amount of Nodes per Axis",            default=10)
    req_args.add_argument('--mat_tensor',     type=parse_matrix,            help="Material Tensor",                     default=[[1, 0], [0, 1]])

    # Boundary Conditions
    req_args.add_argument('--left_bound',     type=parse_boundary_condition,   help="Condition of the Left boundary",      default="[100, 'Dirichlet']")   # TODO good way to do it ?
    req_args.add_argument('--top_bound',      type=parse_boundary_condition,   help="Condition of the Top boundary",       default="[0, 'Neumann']")
    req_args.add_argument('--right_bound',    type=parse_boundary_condition,   help="Condition of the Right boundary",     default="[0, 'Dirichlet']")
    req_args.add_argument('--bottom_bound',   type=parse_boundary_condition,   help="Condition of the Botton boundary",    default="[0, 'Neumann']")
    
    # Line Inputs
    opt_args.add_argument('--line_start',   type=parse_coordinates,              help="X- and Y-Value of the Startpoint of the Line", required=False)
    opt_args.add_argument('--line_end',     type=parse_coordinates,              help="X- and Y-Value of the Endpoint of the Line", required=False)
    opt_args.add_argument('--line_value',   type=str,     help="Value or Function to describe the Values of the Line. (X/Y-Coordinates need to be in {}-brackets)", required=False)
    opt_args.add_argument('--line_points',  type=int,     help="Amount of Points for the Line", required=False, default=10)

    args = parser.parse_args()

    line_bool = True
    if (args.line_start and args.line_end and args.line_value) != None:  # check if Line-arguments were given
         line_bool = False

    start_time = time.time()

    # creates the mesh with all the nodes
    mesh_coords = createMesh(args.width, 
                             args.height, 
                             args.nodes_per_axis)

    # gets amount of coordinate pairs
    array_size = mesh_coords.shape[0]
    
    # Get Coordinates and their respective Values of the Line
    line_coords, line_values = create_line_coords_and_values(mesh_coords, 
                                                             args.line_start, 
                                                             args.line_end, 
                                                             args.line_points, 
                                                             args.line_value, 
                                                             line_bool)

    # creates the array containing the node-equations
    NE_array = get_node_equation_array(array_size, mesh_coords, line_coords)

    # creates the finite elements of the domain
    finite_elements = element_generation(args.nodes_per_axis, 
                                         args.height, 
                                         args.width, 
                                         args.nodes_per_axis)       #args.nodes_per_axis is in here twice

    bc_array = [
        bc.BoundaryCondition(args.left_bound[0], args.left_bound[1]),
        bc.BoundaryCondition(args.top_bound[0], args.top_bound[1]),
        bc.BoundaryCondition(args.right_bound[0], args.right_bound[1]),
        bc.BoundaryCondition(args.bottom_bound[0], args.bottom_bound[1])]


    stiff_mat, result_vect = stiffness_matrix(mesh_coords, 
                                              array_size, 
                                              args.mat_tensor, 
                                              args.order_num_int, 
                                              bc_array, 
                                              args.width, 
                                              args.height, 
                                              args.nodes_per_axis, 
                                              line_coords, 
                                              line_values)

    node_connect_mat = node_connectivity_matrix(args.nodes_per_axis)

    write_files(finite_elements, 
                array_size, 
                result_vect, 
                mesh_coords, 
                node_connect_mat,
                args.name)

    end_time = time.time()

    print(f"Elapsed Time: {end_time - start_time} seconds.")
