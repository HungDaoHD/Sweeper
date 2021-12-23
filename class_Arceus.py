import tkinter as tk
from tkinter import ttk, messagebox
from class_Sweeper import sweeper
from class_MLV import mlv


class arceus:

    def __init__(self, win, prgConn, strVer, userName, password):
        self.prgConn = prgConn
        self.ver = strVer
        self.winArceus = win
        self.loginName = userName
        self.loginPass = password

        # ICON
        self.iconsArceus = {
            'Sweeper': tk.PhotoImage(file='Icon\Features\Checklist.png'),
            'MLV': tk.PhotoImage(file='Icon\Features\MLV.png'),
            'BVC': tk.PhotoImage(file='Icon\Features\BVC.png'),
            'CPT': tk.PhotoImage(file='Icon\Features\CPT.png'),
        }

        self.frArceus = ttk.Labelframe(self.winArceus, name='frArceus', text='FEATURES')
        self.frArceus.place(relx=0.5, rely=0.3, anchor='center')

        self.btnSweeper = ttk.Button(self.frArceus, text='Checklist', command=self.displaySweeper, image=self.iconsArceus['Sweeper'], compound='left')
        self.btnMLV = ttk.Button(self.frArceus, text='MLV', command=self.displayMLV, image=self.iconsArceus['MLV'], compound='left')
        self.btnBVC = ttk.Button(self.frArceus, text='BVC', command=self.displayBVC, image=self.iconsArceus['BVC'], compound='left', state='disabled')
        self.btnCPT = ttk.Button(self.frArceus, text='CPT', command=self.displayCPT, image=self.iconsArceus['CPT'], compound='left', state='disabled')

        self.btnSweeper.grid(row=0, column=0, sticky='we')
        self.btnMLV.grid(row=0, column=1, sticky='we')
        self.btnBVC.grid(row=0, column=2, sticky='we')
        self.btnCPT.grid(row=0, column=3, sticky='we')
        self.frArceus.grid_columnconfigure(0, weight=1)
        self.frArceus.grid_columnconfigure(1, weight=1)
        self.frArceus.grid_columnconfigure(2, weight=1)
        self.frArceus.grid_columnconfigure(3, weight=1)

        self.winArceus.protocol("WM_DELETE_WINDOW", self.quitConfirmation)


    def quitConfirmation(self, event=None):
        if messagebox.askyesno('Confirmation', 'Are you sure you want to quit?'):
            self.winArceus.iconify()
            isValidAcc, isValidStt = self.prgConn.tryLogin(self.loginName, self.loginPass, isLogin=False)
            if isValidAcc and isValidStt:
                self.winArceus.quit()
            else:
                self.winArceus.deiconify()
                messagebox.showerror('Quiting error', 'Please check your internet connection.')


    def displaySweeper(self):
        self.frArceus.destroy()
        sweeper(self.winArceus, self.prgConn, self.ver, self.loginName, self.loginPass, arceus)


    def displayMLV(self):
        self.frArceus.destroy()
        mlv(self.winArceus, self.prgConn, self.ver, self.loginName, self.loginPass, arceus)


    @staticmethod
    def displayBVC():
        messagebox.showinfo('BVC', 'Coming soon.')


    @staticmethod
    def displayCPT():
        messagebox.showinfo('CPT', 'Coming soon.')