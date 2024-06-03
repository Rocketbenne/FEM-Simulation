#%%
# First we let the user "input" be done throught putting numbers in the variables
# Later on we might do it throught the cmd or a pop-up-window

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
        print("\nPlease enter a Number greater than 0.\n")
