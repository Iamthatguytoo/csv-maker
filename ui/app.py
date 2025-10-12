import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print("Starting the CSV Maker app...")
import pandas as pd
import tkinter as tk
from csv_utils.loader import load_csv_with_fallback
from csv_utils.saver import save_data_as_csv
from widgets.scrollable_area import create_scrollable_area
from tkinter import messagebox, filedialog, simpledialog
import os
PAD_X = 5

class csv_maker:
    
    def __init__(self, root):
        
        self.root = root
        self.main_frame, self.canvas, self.scrollable_frame = create_scrollable_area(self.root)
        self.root.title("CSV Maker")
        self.entries = []
        self.data = []
        self.columns = []
        self.headers = []
        self.top_controls_frame = tk.Frame(self.root)
        self.top_controls_frame.grid(row=0, column=0, columnspan=2, pady=10)
        self.root.grid_rowconfigure(0, weight=0)  
        self.root.grid_rowconfigure(1, weight=1)  
        self.root.grid_rowconfigure(100, weight=1)  
        self.root.grid_columnconfigure(0, weight=1)  
        self.root.grid_columnconfigure(1, weight=1)
        self.search_var = tk.StringVar()


        self.root.geometry("800x600")

        self.setup_initial_inputs()

    def new_csv(self): 
         self.entries = []
         self.data = []
         self.columns = []
         self.headers = []
         self.setup_initial_inputs()

    def reset_csv(self):
        for row in self.entries:
            for entry in row:
                entry.delete(0, tk.END)
        messagebox.showinfo("Success", "All data cleared")

    def load_csv(self):
        
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*"), ("Excel files", "*.xlsx *.xls")], 
            title="Load CSV",
        )

        if not file_path:
            return
        
        ext = os.path.splitext(file_path)[1].lower()

        try:
            if ext in [".xlsx", ".xls"]:
                df = pd.read_excel(file_path)
            else:
                df = load_csv_with_fallback(file_path)  
        except Exception as e:
            messagebox.showerror("Error", f"Could not load file:\n{e}")
            return
        self.num_rows = len(df)
        self.num_cols = len(df.columns)
        self.columns = list(df.columns)

        self.main_frame, self.canvas, self.scrollable_frame = create_scrollable_area(self.root)
        self.entries = []
        self.headers = []

        for c, col_name in enumerate(self.columns):
            header_label = tk.Label(self.scrollable_frame, text=col_name,font=('Arial', 10, 'bold'))
            header_label.grid(row=0, column=c, padx=5, pady=5)
            self.scrollable_frame.grid_columnconfigure(c, weight=1)
            self.headers.append(header_label)

        for r in range(self.num_rows):
            row_entries = []
            for c in range(self.num_cols):
                 entry = tk.Entry(self.scrollable_frame)
                 entry.insert(0, str(df.iloc[r, c]))
                 entry.grid(row=r + 1, column=c, padx=5, pady=2, sticky='ew')
                 row_entries.append(entry)
            self.entries.append(row_entries)

        self.create_button_frame()

        messagebox.showinfo("Success", f"Loaded {os.path.basename(file_path)}")

    def setup_initial_inputs(self):
       
        for widget in self.root.winfo_children():
            grid_info = widget.grid_info()
            if grid_info and int(grid_info.get("row", 0)) >= 1:
                widget.destroy()
                
        self.input_frame = tk.Frame(self.root)
        self.input_frame.grid(row=1, column=0, columnspan=4, sticky='nw', pady=(10, 0))

        tk.Label(self.input_frame, text="Number of columns").grid(row=0, column=0, padx=(0, 2), pady=5, sticky='w')
        self.col_entry = tk.Entry(self.input_frame, width=10)
        self.col_entry.grid(row=0, column=1, padx=(0, 10), pady=5)

        tk.Label(self.input_frame, text="Number of rows").grid(row=0, column=2, padx=(0, 2), pady=5, sticky='w')
        self.row_entry = tk.Entry(self.input_frame, width=10)
        self.row_entry.grid(row=0, column=3, padx=(0, 10), pady=5)


        self.top_controls_frame.grid_columnconfigure(0, weight=1)
        self.top_controls_frame.grid_columnconfigure(1, weight=1)
        self.top_controls_frame.grid_columnconfigure(2, weight=1)

        tk.Button(self.top_controls_frame, text="Create Table", command=self.create_table).grid(row=0, column=0, padx=5, sticky="ew")
        tk.Button(self.top_controls_frame, text="New Project", command=self.new_csv).grid(row=0, column=1, padx=5, sticky="ew")
        tk.Button(self.top_controls_frame, text="Load Existing Table", command=self.load_csv).grid(row=0, column=2, padx=5, sticky="ew")

    def add_rows(self):
        row_index = len(self.entries)
        row_entries = []

        for c in range(self.num_cols):
            entry = tk.Entry(self.scrollable_frame)
            entry.grid(row=row_index + 1, column=c, padx=5, pady=2, sticky='ew')
            row_entries.append(entry)

        self.entries.append(row_entries)
        self.num_rows += 1

    def remove_rows(self):
        if self.num_rows <= 0:
            messagebox.showwarning("Error", "No rows to remove")
            return
        
        for entry in self.entries[-1]:
            entry.destroy()

        self.entries.pop()
        self.num_rows -= 1

    def add_columns(self):
        column_name = simpledialog.askstring("Add Column", "Enter Column name:")

        if not column_name or column_name.strip() == "":
            messagebox.showwarning("Warning", "Column name should not be empty")
            return
        
        column_name = column_name.strip()
        self.columns.append(column_name)
        self.num_cols += 1

        for row_index, row_entries in enumerate(self.entries):
            entry = tk.Entry(self.scrollable_frame)
            entry.grid(row=row_index + 1, column=self.num_cols - 1, padx=5, pady=2, sticky='ew')
            row_entries.append(entry)

        header_label = tk.Label(self.scrollable_frame, text=column_name, font=('Arial', 10, 'bold'))
        header_label.grid(row=0, column=self.num_cols - 1, padx=5, pady=5)
        self.scrollable_frame.grid_columnconfigure(self.num_cols - 1, weight=1)
        self.headers.append(header_label)

    def remove_columns(self):
        if self.num_cols <= 1:
            messagebox.showwarning("Warning","No remaining columns")
            return
        
        for row_entries in self.entries:
            row_entries[-1].destroy()
            row_entries.pop()

        if self.headers:
            self.headers[-1].destroy()
            self.headers.pop()

        
        self.num_cols -= 1

    def filter_rows(self):

         search_term = self.search_var.get().lower()
    
         if not search_term:
            
            for r, row in enumerate(self.entries):
                for c, entry in enumerate(row):
                    entry.grid()
            return
        
       
         for r, row in enumerate(self.entries):
             row_has_match = False
             for entry in row:
                 if search_term in entry.get().lower():
                     row_has_match = True
                     break
            
            
             for entry in row:
                 if row_has_match:
                    entry.grid()
                 else:
                    entry.grid_remove()  

    def create_button_frame(self):

        search_frame = tk.Frame(self.root)
        search_frame.grid(row=99, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        tk.Label(search_frame, text="Search in CSV:").pack(side=tk.LEFT, padx=5)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind("<KeyRelease>", lambda e: self.filter_rows())
            
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=101, column=0, columnspan=2, pady=5)

        tk.Button(button_frame, text="Reset CSV", command=self.reset_csv, width=15).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="Add Row", command=self.add_rows, width=15).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="Remove Row", command=self.remove_rows, width=15).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="Add Column", command=self.add_columns, width=15).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="Remove Column", command=self.remove_columns, width=15).pack(side=tk.LEFT, padx=2)

        tk.Button(self.root, text="Save as CSV", command=self.save_as_csv).grid(row=103, column=0, columnspan=2, pady=10)


    def create_table(self):
        try:
            self.num_cols = int(self.col_entry.get())
            self.num_rows = int(self.row_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers.")
            return

        
        for widget in self.root.winfo_children():
            grid_info = widget.grid_info()
            if grid_info and int(grid_info.get("row", 0)) >= 2:
                widget.destroy()

        
        self.column_names_frame = tk.Frame(self.root)
        self.column_names_frame.grid(row=2, column=0, columnspan=3, sticky="nw", pady=(0, 0))
        self.column_names_frame.grid_columnconfigure(0, weight=0)  
        self.column_names_frame.grid_columnconfigure(1, weight=1)  

        self.column_name_entries = []
        for i in range(self.num_cols):
            tk.Label(self.column_names_frame, text=f"Column {i+1} Name:").grid(row=i, column=0, padx=5, pady=2, sticky="w")
            entry = tk.Entry(self.column_names_frame)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky="ew")
            self.column_name_entries.append(entry)

        tk.Button(self.column_names_frame, text="Next", command=self.build_data_form).grid(row=self.num_cols, column=0, columnspan=2, pady=10)

    def build_data_form(self):

        
        
        self.columns = [e.get().strip() for e in self.column_name_entries]
        if any(not name for name in self.columns):
            messagebox.showerror("Invalid Input", "Please enter all column names.")
            return
        
        try:
            self.num_rows = int(self.row_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of rows.")
            return

        self.num_cols = len(self.columns)

       
        for widget in self.root.grid_slaves():
            if int(widget.grid_info()["row"]) >= 3 + self.num_cols:
                widget.destroy()
        
        self.main_frame, self.canvas, self.scrollable_frame = create_scrollable_area(self.root)

        

        self.entries = []
        self.headers = []
 
        for c, col_name in enumerate(self.columns):
            header_label = tk.Label(self.scrollable_frame, text=col_name, font=('Arial', 10, 'bold'))
            header_label.grid(row=0, column=c, padx=5, pady=5)
            self.scrollable_frame.grid_columnconfigure(c, weight=1)
            self.headers.append(header_label)

        for r in range(self.num_rows):
            row_entries = []
            for c in range(self.num_cols):
                entry = tk.Entry(self.scrollable_frame)
                entry.grid(row=r + 1, column=c, padx=5, pady=2, sticky='ew')
                row_entries.append(entry)
            self.entries.append(row_entries)

        self.create_button_frame()

        self.root.update_idletasks()
        self.root.geometry(f"{self.root.winfo_reqwidth()}x{self.root.winfo_reqheight()}")

    
    def save_as_csv(self):
        data = []
        for row in self.entries:
            row_data = [entry.get() for entry in row]
            data.append(row_data)

        if any(len(row) != len(self.columns) for row in data):
          messagebox.showerror("Error", "Mismatch between data columns and column headers.")
          return
        
        save_data_as_csv(data, self.columns)