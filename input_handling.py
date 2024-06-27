#%%
# First we let the user "input" be done throught putting numbers in the variables
# Later on we might do it throught the cmd or a pop-up-window
import numpy as np


# used for testing the program, just wirte the values in here
def getGeometryInputs_hard_coded():
    width, height, order_num_int = 90, 180, 1

    return width, height, order_num_int

# for finished version, lets user input values and error-checks them
def getGeometryInputs():
    width, height, order_num_int = 0, 0, 0

    print("Input the Width: ")
    width = getNumberFromUser()
    print("Input the Height: ")
    height = getNumberFromUser()
    print("Input the Order of the Numerical Integration: ")
    order_num_int = getNumberFromUser()

    return width, height, order_num_int

# get a number from the user throught the console and makes error checks
def getNumberFromUser():
    while(1):
        number = input()
        if(number.isnumeric()):  # checks if value is numeric
            if(int(number) > 0):  # checks if numeric value is greater than 0
                return int(number)
        print("Please enter a Number greater than 0.\n")

# get a number in a specific range from the user throught the console and makes error checks
def getNumberFromUserInRange(range):
    while(1):
        number = input()
        if(number.isnumeric()):  # checks if value is numeric
            if(int(number) > 0):  # checks if numeric value is greater than 0 and less than thr given range
                if(int(number) <= range):
                    return int(number)
        print("Please enter a Number greater than 0 and less than " + str(range) + ".\n")

def getNumberFromUserInRangeWithZero(range):
    while(1):
        number = input()
        if(number.isnumeric()):  # checks if value is numeric
            if(int(number) >= 0):  # checks if numeric value is greater|equal  0 and less than thr given range
                if(int(number) <= range):
                    return int(number)
        print("Please enter a Number greater than 0 and less than " + str(range) + ".\n")

def getNumberFromUserWithAll():
    while(1):
        number = input()
        if(number.isnumeric()):  # checks if value is numeric
            return int(number)
        print("Please enter a Number.\n")

# user input for line with given value
def getLineInputs(width, height):
    start, end, value_function = 0, 0, ""

    print("X-Coordinate of the Start-Point of the Line: ")
    x_start = getNumberFromUserInRange(width)
    print("Y-Coordinate of the Start-Point of the Line: ")
    y_start = getNumberFromUserInRange(height)
    print("X-Coordinate of the End-Point of the Line: ")
    x_end = getNumberFromUserInRange(width)
    print("Y-Coordinate of the End-Point of the Line: ")
    y_end = getNumberFromUserInRange(height)
    print("Input the value of the Line: ")
    value_function = input()

    start = (x_start, x_end)
    end = (y_start, y_end)

    return start, end, value_function


def getMaterialTensor():
    print("First value of the material Tensor: ")
    value1 = getNumberFromUser()
    print("Second value of the material Tensor: ")
    value2 = getNumberFromUser()
    print("Third value of the material Tensor: ")
    value3 = getNumberFromUser()
    print("Fourth value of the material Tensor: ")
    value4 = getNumberFromUser()
    return np.array([[value1, value2],[value3, value4]])

def getLineInputs_hard_coded():
    start = (50, 180)
    end = (50, 0)
    value_function = "0"

    #start = (10, 160)
    #end = (57, 100)
    #value_function = "{x}+{y}"

    return start, end, value_function

def getBCInputs():
    top_side = getBCInput("top")
    right_side = getBCInput("right")
    bottom_side = getBCInput("bottom")
    left_side = getBCInput("left")
    return top_side, right_side, bottom_side, left_side

def getBCInput(side):
    bc = [0,0]
    print(f"Input the {side} boundary type  0=Dirichlet 1=Neumann: ")
    bc[0] = getNumberFromUserInRangeWithZero(1)
    print(f"Input the {side} boundary value: ")
    bc[1] = getNumberFromUserWithAll()
    return bc

