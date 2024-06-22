from sklearn.neighbors import BallTree
import numpy as np
import math

# Inputs: start-coordinate of the line
#         end-coordinate of the line
#         coordinates of the mesh
# Output: The line represented as coordinates of the mesh
def getLineCoordinates(start, end, mesh_coords):

    # the higher this is the more points on the line get queried
    # this could in some cases result to more points beeing 'chosen', 
    # thus more accurate result of the line 
    AMOUNT_OF_POINTS_ON_LINE = 10

    x = np.linspace(start[0], end[0], AMOUNT_OF_POINTS_ON_LINE)
    y = np.linspace(start[1], end[1], AMOUNT_OF_POINTS_ON_LINE)
    coords = np.column_stack((x, y))
    
    # Initialization of BallTree
    balltree = BallTree(mesh_coords)

    # gets the index of the nearest neightbors to the array "points"
    # k = 1 means only closest point gets returned
    # return_distance = False means we do not want the function to return the distance
    index = balltree.query(coords, k = 1, return_distance = False)

    # convert coords to tuples
    mesh_coords = [tuple(coord) for coord in mesh_coords]

    # put the line-coordinates in one list
    values = np.zeros([len(index)], dtype=tuple)
    
    j = 0
    for i in index:
        values[j] = mesh_coords[i[0]]
        j+=1

    # get rid of duplicates
    values = list(set(values))

    return values


# Generates the value of the given function and the given coordinates
# The Function needs to have the variables x and y in curved brackets
# Inputs: coordinates of the line
#         function which should be evaluated
# Output: Values of the Function at the Coordinates
def getLineValues(line_coords, function):

    values = []

    for (x, y) in line_coords:
        values = np.append(values, evaluate_function(function, x, y))

    return values


# calculates the value of the function at the position (x, y)
# Inputs: Function-Expression
#         Value for x
#         Value for y
# Output: Value of the Function
def evaluate_function(function, x, y):
    if(function.isnumeric()):
        return int(function)
    try:
        result = eval(function.format(x=x, y=y), {'__builtins__': None}, {'sin': math.sin, 'cos': math.cos, 'tan': math.tan, 'pi': math.pi, 'e': math.e, 'sqrt': math.sqrt})
        return result

    except Exception as e:
        print("Error evaluating function:", e)
        return None
