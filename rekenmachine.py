# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk


class Rekenmachine(tk.Frame):
    """Deze class bouwt een Rekenmachine. Het venster wordt geïnitialiseerd."""
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        # Zorg ervoor dat de widgets goed over de ruimte worden verdeeld:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def createWidgets(self):
        # Maak het scherm waarin het uiteindelijke resultaat wordt getoond
        # en het invoerscherm
        
        self.invoer = tk.StringVar()
        self.uitvoer = tk.StringVar()
        self.operator = ''
        
        self.uitvoerscherm = ttk.Label(self, textvariable=self.uitvoer)
        self.uitvoerscherm.grid(column=0, row=1, columnspan=2, sticky="W")
        self.invoerscherm = ttk.Label(self, textvariable=self.invoer)
        self.invoerscherm.grid(column=2, row=1, columnspan=1, sticky="E")

        # maak toetsen om het programma te besturen
        # ttk.Button(self, text='Stop', command=quit).grid(row=0, column=3)
        ttk.Button(self, text='Wis', command=self.wissen).grid(row=1, column=3)

        # maak alle rekentoetsen
        self.symbolen = [[7,8,9,'/'],[4,5,6,'x'],[1,2,3,'-'],['.',0,'+','=']]
        self.toetsen = [['' for y in range(4)] for x in range(4)]
        for x in range(4):
            for y in range(4):
                toets = self.symbolen[x][y]
                self.toetsen[x][y] = Rekentoets(self, toets=toets, x=x, y=y)
    
    def Calc(self, toets):
        # Voer de getallen in en bereken de sommen
        # Er wordt tot op zekere hoogte rekening gehouden met 
        # float <> int maar deze rekenmachine is nog niet 100 % betrouwebaar

        invoer = self.invoer.get()
        uitvoer = self.uitvoer.get()
        functies = {'+': fPlus, '-': fMin, 'x': fKeer, '/': fDeel}
        
        if type(toets) == int:
            invoer += str(toets)
        elif toets == '.':
            if '.' not in invoer:
                if invoer == '':
                    invoer = '0.'
                else:
                    invoer += '.'
                self.toetsen[3][0]["state"] = "disabled"
        else:
            # als de invoer niet leeg is, doe dan een berekening,
            # of zet in ieder geval de invoer in het uitvoerveld
            if invoer != '':
                if self.operator in functies:
                    uitvoer = functies[self.operator](invoer, uitvoer)
                else:
                    uitvoer = invoer
                # zet het resultaat in de uitvoer, maak de invoer leeg 
                # zet de punt weer op actief
                self.uitvoer.set(str(uitvoer).strip('0').strip('.'))
                invoer = ''
                self.toetsen[3][0]["state"] = "normal"
            self.operator = toets

        self.invoer.set(invoer)

    def wissen(self):
        if self.invoer.get() == '':
            self.uitvoer.set('')
        else:
            self.invoer.set('')


class Rekentoets(tk.Button):
    """Deze class bouwt een toets en geeft deze een functie mee."""
    
    def __init__(self, master=None, *args, toets, x, y):
        ttk.Button.__init__(self, master)
        self["text"] = toets
        self["command"] = lambda: self.master.Calc(toets)
        self.grid(row=(x+2), column=y, sticky="WENS")
        self.toets = toets


def fPlus(invoer, uitvoer):
    try:
        return int(uitvoer) + int(invoer)
    except:
        return float(uitvoer) + float(invoer)

def fMin(invoer, uitvoer):
    try:
        return int(uitvoer) - int(invoer)
    except:
        return float(uitvoer) - float(invoer)

def fKeer(invoer, uitvoer):
    try:
        return int(uitvoer) * int(invoer)
    except:
        return float(uitvoer) * float(invoer)

def fDeel(invoer, uitvoer):
    try:
        return float(uitvoer) / float(invoer)
    except:
        return 'Dit kan niet: {}/{}'.format(uitvoer, invoer)   

def tCalc(Event):
    # print(Event)
    toetssym = {'*': 'x', '\r': '='}
    symbolen = [str(rm.symbolen[x][y]) for x in range(4) for y in range(4)]

    if Event.char in toetssym:
        rm.Calc(toetssym[Event.char])
    elif Event.char in symbolen:
        try:
            rm.Calc(int(Event.char))
        except:
            rm.Calc(Event.char)
    elif Event.keysym == "Delete":
        rm.wissen()
    elif Event.keysym == "BackSpace":
        invoer = rm.invoer.get()
        if invoer != '':
            if invoer[-1] == '.':
                rm.toetsen[3][0]["state"] = "normal"
            rm.invoer.set(invoer[:-1])
    else:
        # print(Event)
        pass

if __name__ == '__main__':
    rm = Rekenmachine()
    rm.master.title('Rekenmachine')
    rm.master.wm_iconbitmap('icoon.ico')
    rm.master.bind('<Escape>', quit)
    rm.master.bind('<KeyPress>', tCalc)

    rm.mainloop()
