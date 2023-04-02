from tkinter import *
from tkinter import scrolledtext
from tkinter import ttk
from easynmt import EasyNMT
from PIL import Image, ImageTk
from tkinter import messagebox

import random
import threading
import ClassNetwork
import Loading_class
import tkinter as tk
import Style_Class


class App_Main_Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NeuralNetwork 4.1.0")
        self.geometry("800x600+400+80")
        self["background"]="#c1c5d6"
        self.triger_trans = True
        self.load_image()
        self.interface()
        self.models = None
        Style_Class.Style()
        self.option_add('*TCombobox*Listbox.selectBackground', '#c1c5d6')
        self.option_add('*TCombobox*Listbox.selectForeground', '#101118')

    def load_image(self):
        pathToImage = "image\\copy.png"
        im = Image.open(pathToImage)
        im = im.resize((20, 20), Image.LANCZOS)
        self.ph = ImageTk.PhotoImage(im)

        pathToImage_del = "image\\bin.png"
        im_del = Image.open(pathToImage_del)
        im_del = im_del.resize((20, 20), Image.LANCZOS)
        self.ph_del = ImageTk.PhotoImage(im_del)

        pathToImage_trans_ru = "image\\ru.png"
        im_trans_ru = Image.open(pathToImage_trans_ru)
        im_trans_ru = im_trans_ru.resize((20, 20), Image.LANCZOS)
        self.ph_trans_ru = ImageTk.PhotoImage(im_trans_ru)

        pathToImage_trans_en = "image\\en.png"
        im_trans_en = Image.open(pathToImage_trans_en)
        im_trans_en = im_trans_en.resize((20, 20), Image.LANCZOS)
        self.ph_trans_en = ImageTk.PhotoImage(im_trans_en)

    def interface(self):
        Frame = ttk.Frame(self, style="frame_style.TFrame")
        Path_name = ttk.Label(Frame, text="Выберите книгу", font="Times 18")
        Count_char_name = ttk.Label(Frame, text="количество символов", font="Times 11", foreground="black")
        book = ["Гарри Поттер", "Шерлок Холмс"]
        self.book_var = StringVar(value=book[0])
        Path = ttk.Combobox(Frame, width=120, textvariable=self.book_var, style="combobox_style.TCombobox", values=book, state="readonly")

        self.btn_var = ttk.Button(Frame, text="Пересгенерировать", style="button_style.TButton", state="disabled", command=self.updated)
        btn_del = ttk.Button(Frame, image=self.ph_del, style="button_style.TButton", command=self.del_text)
        btn_copy = ttk.Button(Frame, image=self.ph, style="button_style.TButton", command=self.copy_buffer)
        btn_generated = ttk.Button(Frame, width=20, style="button_style.TButton", text="Сгенерировать текст",#height=2
                                  command=self.generated_text)
        self.btn_translate_ru = ttk.Button(Frame, style="button_style.TButton", image=self.ph_trans_ru, command=self.translate)
        self.scrolltext = tk.scrolledtext.ScrolledText(Frame, width=80, wrap="word",font="Georgia 10")

        variant_char = ["100", "150", "200", "300"]
        self.char_var = StringVar(value=variant_char[1])
        count_chars = ttk.Combobox(Frame, textvariable=self.char_var, style="combobox_style.TCombobox", values=variant_char, state="readonly")
        frame_btn = ttk.Frame(Frame, height=40, style="frame_style.TFrame")

        Path_name.grid(column=1, row=0, columnspan=3)
        Path.grid(column=1, row=1, columnspan=3)
        frame_btn.grid(column=2, columnspan=3, row=2)
        self.scrolltext.grid(column=1, row=3, columnspan=3)
        btn_generated.grid(column=1, row=4, columnspan=3, padx=5, pady=5)
        self.btn_var.grid(column=3, row=4, sticky="NE", padx=5, pady=5)
        Frame.pack()

        Count_char_name.place(x=0, y=480)
        count_chars.place(x=0, y=505)

        btn_copy.place(x=670, y=57)
        self.btn_translate_ru.place(x=635, y=57)
        btn_del.place(x=705, y=57)

    def clear_text(self, text):
        clear = text.split()
        result = " ".join(set(clear))
        return result

    def updated(self):
        long = self.lengh_text
        text = self.scrolltext.get("1.0", tk.END)
        if self.triger_trans:
            if text == "" or len(text) < 2 or text.isspace():
                self.btn_var.config(state="disabled")
            elif text != "":
                new_text = ""
                timer = '.' + str(long)
                load = Loading_class.Loading_form(self, float(timer))
                threading.Thread(target=load.Animation()).start()
                for i in range(0, long + 1):
                    new_text += text[i]
                self.scrolltext.delete("1.0", tk.END)
                self.scrolltext.insert(INSERT, self.clear_text(new_text+' '))
                self.scrolltext.insert(INSERT, self.clear_text(self.neyr.Set_text(random.uniform(1.2, 1.4))))
                load.closing()


    def del_text(self):
        self.scrolltext.delete("1.0", tk.END)
        self.btn_var.config(state="disabled")

    def copy_buffer(self):
        self.scrolltext.clipboard_clear()
        self.scrolltext.clipboard_append(self.scrolltext.get("1.0", tk.END))

    def generated_text(self):
        selection = self.book_var.get()
        save_model = ""
        text_save = ""
        if selection == "Гарри Поттер":
            save_model = "C:\\Users\\Dantalyan\\Desktop\\Future\\appNeyronetwork\\model_weights_HP.hdf5"
            text_save = "C:\\Users\\Dantalyan\\Desktop\\Future\\appNeyronetwork\\HP.txt"
        elif selection == "Шерлок Холмс":
            save_model = "C:\\Users\\Dantalyan\\Desktop\\Future\\appNeyronetwork\\model_weights_saved_Sherlock.hdf5"
            text_save = "C:\\Users\\Dantalyan\\Desktop\\Future\\appNeyronetwork\\sherlock.txt"
        self.lengh_text = len(self.scrolltext.get("1.0", tk.END))
        chars_g = self.char_var.get()
        timer = '.'+chars_g
        load = Loading_class.Loading_form(self, float(timer))
        textcontinue = self.scrolltext.get("1.0", tk.END)
        threading.Thread(target=load.Animation()).start()
        if not self.triger_trans:
            self.btn_var.config(state="normal")
            if textcontinue == "" or textcontinue.isspace():
                self.scrolltext.delete("1.0", tk.END)
            self.neyr = ClassNetwork.Neyron(int(chars_g), save_model, "", text_save)
            self.neyr.Load_Model()
            self.scrolltext.insert(tk.END,
                              self.models.translate(self.clear_text(self.neyr.Set_text(random.uniform(1.2, 1.4))), target_lang="ru"))
        elif self.triger_trans:
            self.btn_var.config(state="disabled")
            if textcontinue == "" or textcontinue.isspace():
                self.scrolltext.delete("1.0", tk.END)
            self.neyr = ClassNetwork.Neyron(int(chars_g), save_model, self.clear_text(textcontinue), text_save)
            self.neyr.Load_Model()
            self.scrolltext.insert(tk.END, self.clear_text(self.neyr.Set_text(random.uniform(1.2, 1.4))))
        load.closing()

    def translate(self):
        mes = messagebox.askyesno("Warning",
                                  "Предупреждение данный модуль все еще не стабилен вы уверены что хотите его использовать?",
                                  parent=self, icon='warning')
        if mes:
            self.models = EasyNMT('opus-mt', max_length=1000000)
            text = self.scrolltext.get("1.0", tk.END)
            if self.triger_trans:
                if text != "" or len(text) > 2 or not text.isspace():
                    self.triger_trans = False
                    self.btn_translate_ru.config(image=self.ph_trans_en)
                    hh = ' ' + self.scrolltext.get("1.0", tk.END)
                    load = Loading_class.Loading_form(self, float(.100))
                    threading.Thread(target=load.Animation()).start()
                    self.scrolltext.delete("1.0", tk.END)
                    self.scrolltext.insert(tk.END, self.models.translate(self.clear_text(hh), target_lang='ru'))
                    load.closing()
                elif text == "" or len(text) < 2 or text.isspace():
                    self.triger_trans = False
            elif not self.triger_trans:
                self.triger_trans = True
                self.btn_translate_ru.config(image=self.ph_trans_ru)


if __name__ == "__main__":
    App = App_Main_Window()
    App.mainloop()

