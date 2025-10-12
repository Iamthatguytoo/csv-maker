import pandas as pd
import os
from tkinter import messagebox, filedialog

def save_data_as_csv(data, columns):
    empty_cells = sum(1 for row in data for cell in row if not cell or cell.strip() == "")
    
    if empty_cells > 0:
        
        response = messagebox.askyesno(
            "Warning",
            f"Found {empty_cells} empty cells. Continue saving?"
        )
        if not response:
            return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        initialdir=os.path.expanduser("~"),
        title="Save CSV as",
    )

    if not file_path:
        return

    df = pd.DataFrame(data, columns=columns)
    df.to_csv(file_path, index=False)

    try:
        os.startfile(file_path)
    except AttributeError:
        pass

    messagebox.showinfo("Success", f"Data saved to {os.path.basename(file_path)}")

   