import tkinter as tk
def create_scrollable_area(root):
        
    main_frame = tk.Frame(root)
    main_frame.grid(row=100, column=0, columnspan=999, sticky="nsew")

    root.grid_rowconfigure(100, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    canvas = tk.Canvas(main_frame)
    v_scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    h_scrollbar = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=canvas.xview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=v_scrollbar.set,
                     xscrollcommand=h_scrollbar.set)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    return main_frame, canvas, scrollable_frame