import cv2
import time
from tkinter import * 


import Messaggio as messaggio
import Preview as prev
import ScattaFoto as scatta
import GestioneLaser as laser
import Misura as mis


def Preview ():
    messaggio.funz("Premere q per arrestare")
    prev.funz()


def Scatta():
    imgLeft , imgRight = scatta.funz()
    #salvataggio immagini
    #d --> day , B --> mese , y --> anno , H --> ore , M --> minuti , S --> secondi 
    cv2.imwrite('../img/Left_'+time.strftime("%d_%B_%y:%H:%M:%S"), imgLeft)
    cv2.imwrite('../img/Right_'+time.strftime("%d_%B_%y:%H:%M:%S"), imgRight)
    messaggio.funz("Immagini salvate")


def Accendi():
    laser.funz(1)

def Spegni():
    laser.funz(0)

def Misura():
    mis.funz()

#AVVIO INTERFACCIA
root = Tk() #finestra principale
root.title("Misuratore di distanza")
root.configure(bg="gray")
#grandezze finestra fissate
root.minsize(width=500,height=200)
root.maxsize(width=500,height=200)

#BOTTONI INTERFACCIA
preview = Button(root, text="Preview", command=Preview, bg="white")
cattura = Button(root, text="Scatta", command=Scatta, bg="white")
accendilaser = Button (root, text = "Accendi laser", command =Accendi, bg = "white")
spegnilaser = Button (root, text = "Spegni laser", command =Spegni, bg = "white")
calcola = Button(root, text="Misura", command=Misura, bg="white")

#POSIZIONI BOTTONI NELLA GRIGLIA
cattura.grid(row=15, column=7, columnspan=2, padx=100, pady=10)
preview.grid(row=15, column=14, columnspan=2, padx=10, pady=10)
accendilaser.grid(row=16, column=7, columnspan=2, padx=100, pady=10)
spegnilaser.grid(row=16, column=14, columnspan=2, padx=10, pady=10)
calcola.grid(row=17, column=7, columnspan=2, padx=100, pady=10)

root.mainloop()
# when everything done,release the capture
