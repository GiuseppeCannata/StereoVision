from tkinter import *

def funz(messaggio):
    root = Tk()
    root.configure(bg="white")
    root.title("Avviso!")
    messaggio = Label(root, text=messaggio, bg="white")
    messaggio.grid(row=1, column=0, padx=10, pady=10)