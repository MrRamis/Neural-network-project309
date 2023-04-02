import random
from tkinter import *
import tkinter.ttk as ttk
import time, threading
from asyncio import sleep
from tqdm import asyncio
import Style_Class

class Loading_form:
    def __init__(self, main_form, timer):
        self.main_form = main_form
        self.tk = Toplevel(main_form, bg="#E0D3E0")
        self.tk.title("Loading")
        self.timer = timer
        self.tk.transient(main_form)
        self.tk.grab_set()
        self.tk.geometry("400x200+600+200")
        self.tk.attributes("-topmost", True)
        self.Frame_form = Frame(self.tk, bg="#E0D3E0")
        self.Label_form = Label(self.Frame_form, bg="#E0D3E0", text="Идет загрузка ожидайте", font="Times 12")
        self.Frame_form.pack()
        self.Label_form.pack(pady=10, padx=10)
        Style_Class.Style()

    def Animation(self):
        s = ttk.Style()
        s.theme_use('default')
        s.configure("red.Horizontal.TProgressbar", background='black',)
        self.progress_bar = ttk.Progressbar(self.Frame_form, length=300, style="red.Horizontal.TProgressbar", orient="horizontal", mode="determinate")
        self.progress_bar.pack()

        threading.Thread(target=self.progress()).start()

    def closing(self):
        self.tk.update()
        delen = random.randint(1, 3)
        mode = 16 - self.stop / delen
        for i in range(delen):
            Style_Class.Style()
            self.tk.update()
            self.progress_bar['value'] += mode
            time.sleep(self.timer)
        self.tk.destroy()

    def progress(self):
        self.stop = random.randint(13, 16)
        for i in range(self.stop):
            Style_Class.Style()
            self.tk.update()
            self.progress_bar['value'] += i
            time.sleep(self.timer*4)

