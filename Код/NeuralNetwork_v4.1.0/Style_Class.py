from tkinter import ttk


class Style(ttk.Style):
    def __init__(self):
        super().__init__()
        button_style = ttk.Style()
        button_style.theme_use("clam")
        button_style.configure("button_style.TButton", background="#787fa0", foreground="#101118", focuscolor='none')
        button_style.map('button_style.TButton', background=[('active', '#ebecf0')])

        frame_style = ttk.Style()
        frame_style.configure("frame_style.TFrame", background="#c1c5d6")

        combobox_style = ttk.Style()
        combobox_style.configure("combobox_style.TCombobox", foreground="#101118")


        self.configure(".", font="Georgia", foreground="#101118", background="#c1c5d6")


