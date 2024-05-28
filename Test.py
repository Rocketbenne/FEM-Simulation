import tkinter as tk
from tkinter import font

# Create the main application window
root = tk.Tk()
root.title("Simple Tkinter App")

# Create a custom font
custom_font = font.Font(family="Helvetica", size=32, weight="bold")

# Create a label widget
label1 = tk.Label(root, text="Inputs", font=custom_font)
label1.grid(row=0, column=1, padx=100, pady=20)

# Define the number of rows and columns for the grid of entry widgets
rows = 3
columns = 3

#Creating Arrays used afterwards to store the data
entrys = []
inputs = []

# Create entry widgets and place them in a grid
for i in range(1,rows+1):
    for j in range(columns-1):
        if(j == 1):
            entry = tk.Entry(root)
            entry.grid(row=i, column=j, padx=5, pady=5)
            entrys.append(entry)

# Define a function to update the label with the entry text
def save_input():
    for entry in entrys:
        inputs.append(entry.get())
    print(inputs)


# Create a button widget that calls the update_label function when clicked
button = tk.Button(root, text="Save Inputs", command=save_input)
button.grid(row=6, column=1, padx=5, pady=20)

# Start the Tkinter event loop
root.mainloop()
