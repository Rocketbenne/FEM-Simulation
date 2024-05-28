import tkinter as tk

# Create the main application window
root = tk.Tk()
root.title("Simple Tkinter App")

# Create a label widget
label = tk.Label(root, text="Hello, Tkinter!")
label.pack(pady=10)

# Create an entry widget
entry = tk.Entry(root)
entry.pack(pady=10)

# Define a function to update the label with the entry text
def save_text():
    text = entry.get()
    label.config(text=text)


# Create a button widget that calls the update_label function when clicked
button = tk.Button(root, text="Update Label", command=save_text)
button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
