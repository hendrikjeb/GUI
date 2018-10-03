import tkinter as tk
from tkinter import ttk

class Rekentoets(tk.Button):
    """docstring for Rekentoets"""
    def __init__(self, master=None, *args, toetsen, x, y):
        ttk.Button.__init__(self, master, text=toetsen[x][y], command=self.Calc)
        self.grid(row=(x+2), column=y, sticky="WENS")
        self.toets = toetsen[x][y]

    def Calc(self):
        if type(self.toets) == int:
            nieuwe_waarde = "{}{}".format(self.master.input.get(), self.toets)
            self.master.input.set(nieuwe_waarde)
        elif self.toets == '.':
            pass
        else:
            pass
        self.master.scherm.focus()
        self.master.scherm.icursor(tk.END)

class Rekenmachine(tk.Frame):
    """docstring for Rekenmachine"""
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def createWidgets(self):
        self.input = tk.StringVar()
        self.output = tk.StringVar()
        
        self.resultaat = ttk.Label(self, textvariable=self.output)
        self.resultaat.grid(column=0, row=0, columnspan=3, sticky="WENS")
        self.scherm = ttk.Entry(self, textvariable=self.input)
        self.scherm.grid(column=0, row=1, columnspan=3, sticky="WENS")
        self.scherm.focus()
        ttk.Button(self, text='Stop', command=quit).grid(row=0, column=3)
        ttk.Button(self, text='Wis').grid(row=1, column=3)

        self.createButtons()

    def createButtons(self):
        toetsen = [[7,8,9,'/'],[4,5,6,'x'],[1,2,3,'-'],['.',0,'+','=']]
        for x in range(4):
            for y in range(4):
                Rekentoets(self, toetsen=toetsen, x=x, y=y)

rm = Rekenmachine()
rm.master.title('Rekenmachine')
rm.master.wm_iconbitmap('icoon.ico')
rm.master.bind('<Escape>', quit)
rm.mainloop()
