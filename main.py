import customtkinter as ctk
from ui.app import csv_maker

if __name__ == "__main__":
    root = ctk.CTk()
    app = csv_maker(root=root)
    root.mainloop()