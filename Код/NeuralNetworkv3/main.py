from tkinter import *
from tkinter import scrolledtext
from tkinter import ttk
import ClassNetwork
import tkinter

save_model = "C:\\Users\\Dantalyan\\Desktop\\Future\\appNeyronetwork\\model_weights_HP.hdf5"
text_save = "C:\\Users\\Dantalyan\\Desktop\\Future\\appNeyronetwork\\HP.txt"


def Clear_Text(text):
    clear = text.split()
    result = " ".join(clear)
    return result


def Generated_Text():
    selection = Path.get()
    chars_g = count_chars.get()
    textcontinue = scrolltext.get("1.0", tkinter.END)
    neyr = ClassNetwork.Neyron(int(chars_g), save_model, Clear_Text(textcontinue), text_save)
    scrolltext.insert(INSERT, neyr.Set_text())


Main_window = Tk()
Main_window.geometry("800x700+400+80")

Frame = Frame(Main_window)
Path_name = Label(Frame, text="Выберите книгу", font="Times 18")
book = ["Гарри Поттер", "Шерлок Холмс"]
book_var = StringVar(value=book[0])
Path = ttk.Combobox(Frame, width=110, textvariable=book_var, values=book, state="readonly")
btn_generated = Button(Frame, width=20, height=2, text="Сгенерировать текст", font="Times 12", command=Generated_Text)
scrolltext = scrolledtext.ScrolledText(Frame)
variant_char = ["100", "150", "200", "300"]
char_var = StringVar(value=variant_char[1])
count_chars = ttk.Combobox(Frame, textvariable=char_var, values=variant_char, state="readonly")


Frame.pack()
Path_name.pack()
Path.pack()
btn_generated.pack(pady=10, padx=10)
scrolltext.pack()
count_chars.pack()
Main_window.mainloop()






