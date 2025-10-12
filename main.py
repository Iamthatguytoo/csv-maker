import tkinter as tk
from ui.app import csv_maker

if __name__ == "__main__":
    root = tk.Tk()
    app = csv_maker(root)
    root.mainloop()