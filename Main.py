import tkinter as tk
import numpy as np
from tkinter import font
import MatrixGUI

# Create the main application window
root = tk.Tk()
root.title("Simple Tkinter App")

# Create a custom font
custom_font = font.Font(family="Helvetica", size=32, weight="bold")
custom_font2 = font.Font(family="Helvetica", size=16, weight="bold")

# Create a label widget
label1 = tk.Label(root, text="Inputs", font=custom_font)
label1.grid(row=0, column=1)

# Creating Arrays used afterwards to store the data
entrys = []
inputs = []
lable_names = ["Material Tensor", "Material Tensor", "length", "width", " " , " "]

# Create the Grid
matrix_tensor = MatrixGUI.MatrixGUI(root,2,2,1,1)
matrix_entry = MatrixGUI.MatrixGUI(root,5,1,3,1)
matrix_label = MatrixGUI.MatrixGUI(root,5,1,1,0,lable_names)
# Define a function to update the label with the entry text
def save_input():
    for entry in matrix_entry.get_matrix():
        inputs.append(entry)
    for tensor in matrix_tensor.get_matrix():
        inputs.append(tensor)
    print(inputs)
    button.destroy()

def print_matrix():
    matrix = matrix_entry.get_matrix()
    print(matrix)


# Create a button widget that calls the update_label function when clicked
button = tk.Button(root, text="Save Inputs", command=save_input)
button.grid(row=matrix_entry.rows+matrix_entry.start_rows, column=1)

# Start the Tkinter event loop
root.mainloop()
