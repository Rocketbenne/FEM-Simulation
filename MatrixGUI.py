import tkinter as tk


class MatrixGUI:
    def __init__(self, root, rows, columns,start_rows, start_columns, lable_names: list[str] = None):
        self.root = root
        self.rows = rows
        self.columns = columns
        self.start_rows = start_rows
        self.start_columns = start_columns
        self.lable_names = lable_names
        if(self.lable_names == None):
            self.entries = []
            self._create_widgets()
        else:
            self.labels = []
            self._create_labels(self.lable_names)

    def _create_widgets(self):
        for i in range(self.start_rows,self.start_rows + self.rows):
            row_entries = []
            for j in range(self.start_columns, self.start_columns + self.columns):
                entry = tk.Entry(self.root, width=10)
                entry.grid(row=i, column=j)
                row_entries.append(entry)
            self.entries.append(row_entries)

    def get_matrix(self):
        matrix = []
        for row in self.entries:
            row_values = []
            for entry in row:
                row_values.append(entry.get())
            matrix.append(row_values)
        return matrix

    def _create_labels(self, label_names):
        for i in range(self.start_rows,self.start_rows + self.rows):
            row_lables = []
            for j in range(self.start_columns, self.start_columns + self.columns):
                label = tk.Label(self.root,text=self.lable_names[i-self.start_rows], width=15)
                label.grid(row=i, column=j)
                row_lables.append(label)
            self.labels.append(row_lables)


    def set_matrix(self, matrix):
        for i in range(self.rows):
            for j in range(self.columns):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, matrix[i][j])



