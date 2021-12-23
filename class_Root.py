from class_Porygon import porygon
import helpinghand as hp
import tkinter as tk
from tkinter import messagebox
from class_Login import login


class root:

    def __init__(self, strVer):
        self.ver = strVer
        self.winRoot = tk.Tk()
        self.winRoot.title(f'Sweeper {self.ver}')
        self.winRoot.iconphoto(False, tk.PhotoImage(file='Icon\Sweeper.png'))
        self.winRoot.state('zoomed')
        self.winRoot.minsize(600, 300)

        if hp.internetConnection():
            self.prgConn = porygon()
            winLogin = login(self.winRoot, self.prgConn, strVer)
        else:
            messagebox.showerror('Internet connection errors', 'Please check your internet connection.')

        self.winRoot.mainloop()