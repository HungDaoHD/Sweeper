import tkinter as tk
from tkinter import ttk, messagebox
import traceback
import sys
import win32api
from class_Arceus import arceus


class login:

    def __init__(self, win, prgConn, strVer):
        self.prgConn = prgConn
        self.ver = strVer
        self.winLogin = win

        self.frLogin = ttk.Labelframe(self.winLogin, name='frLogin', text='LOGIN', relief=tk.SOLID, width=100, height=100)
        self.frLogin.place(relx=0.5, rely=0.3, anchor='center') # relwidth=0.5, relheight=0.5

        self.isLogin = tk.BooleanVar()
        self.isLogin.set(False)

        swpLoginSupportLbl = ttk.Label(self.frLogin,
        text='For more further support, please contact Mr.Hung Dao \nat hung.dao@ipsos.com or 090 737 8682')
        loginNameLbl = ttk.Label(self.frLogin, text='Username')
        loginPassLbl = ttk.Label(self.frLogin, text='Password')
        self.varLoginName = tk.StringVar()
        self.varLoginPass = tk.StringVar()
        self.loginName = ttk.Entry(self.frLogin, textvariable=self.varLoginName)
        self.loginPass = ttk.Entry(self.frLogin, show='*', textvariable=self.varLoginPass)
        self.newPassLbl1 = ttk.Label(self.frLogin, text='New password')
        self.newPassLbl2 = ttk.Label(self.frLogin, text='Confirm password')
        self.newPass1 = ttk.Entry(self.frLogin, show='*')
        self.newPass2 = ttk.Entry(self.frLogin, show='*')

        self.varIsChangePass = tk.BooleanVar()
        self.cbxChangePass = ttk.Checkbutton(self.frLogin, text='Change password', command=self.loginChangePass,
                                              variable=self.varIsChangePass, onvalue=True, offvalue=False)
        self.btnLoginSubmit = ttk.Button(self.frLogin, text='Submit', command=self.loginSubmit)
        self.btnLoginCancel = ttk.Button(self.frLogin, text='Cancel', command=self.loginCancel)

        swpLoginSupportLbl.grid(row=0, column=0, sticky='ew', columnspan=3, padx=5, pady=3)
        loginNameLbl.grid(row=1, column=0, padx=5, pady=3)
        loginPassLbl.grid(row=2, column=0, padx=5, pady=3)
        self.loginName.grid(row=1, column=1, sticky='ew', columnspan=2, padx=5, pady=3)
        self.loginPass.grid(row=2, column=1, sticky='ew', columnspan=2, padx=5, pady=3)
        self.newPassLbl1.grid(row=3, column=0, padx=5, pady=3)
        self.newPassLbl2.grid(row=4, column=0, padx=5, pady=3)
        self.newPass1.grid(row=3, column=1, sticky='ew', columnspan=2, padx=5, pady=3)
        self.newPass2.grid(row=4, column=1, sticky='ew', columnspan=2, padx=5, pady=3)
        self.cbxChangePass.grid(row=5, column=0, sticky='w', padx=5, pady=3)
        self.btnLoginSubmit.grid(row=5, column=1, sticky='e', padx=5, pady=3)
        self.btnLoginCancel.grid(row=5, column=2, sticky='w', padx=5, pady=3)
        self.frLogin.grid_columnconfigure(1, weight=1)

        self.newPassLbl1.grid_forget()
        self.newPassLbl2.grid_forget()
        self.newPass1.grid_forget()
        self.newPass2.grid_forget()

        if win32api.GetUserName() == 'Hung.Dao' and win32api.GetComputerName() == 'APVNHCM20170':
            self.loginName.insert(0, win32api.GetUserName().lower())
            self.loginPass.insert(0, 'Galaxy\'sHero1996')

        self.winLogin.bind('<Return>', self.loginSubmit)
        self.winLogin.protocol("WM_DELETE_WINDOW", self.loginCancel)

        self.loginName.focus()


    def loginCancel(self, event=None):
        self.winLogin.destroy()
        sys.exit()


    def loginChangePass(self, event=None):
        if self.varIsChangePass.get():
            self.newPassLbl1.grid(row=3, column=0, padx=5, pady=3)
            self.newPassLbl2.grid(row=4, column=0, padx=5, pady=3)
            self.newPass1.grid(row=3, column=1, sticky='ew', columnspan=2, padx=5, pady=3)
            self.newPass2.grid(row=4, column=1, sticky='ew', columnspan=2, padx=5, pady=3)
        else:
            self.newPass1.delete(0, 'end')
            self.newPass2.delete(0, 'end')
            self.newPassLbl1.grid_forget()
            self.newPassLbl2.grid_forget()
            self.newPass1.grid_forget()
            self.newPass2.grid_forget()


    def loginSubmit(self, event=None):
        if self.varIsChangePass.get():
            self.submitForChangePass()
        else:
            self.submitForLogin()


    def submitForLogin(self):
        try:
            self.isLogin.set(False)
            self.loginName.configure(state='disabled')
            self.loginPass.configure(state='disabled')
            self.cbxChangePass.configure(state='disabled')
            self.btnLoginSubmit.configure(state='disabled')
            self.btnLoginCancel.configure(state='disabled')
            self.winLogin.after(1, self.winLogin.update())

            isValidLogin, isValidStt, isValidVer = False, False, False

            if self.loginName.get() and self.loginPass.get():
                isValidLogin, isValidStt = self.prgConn.tryLogin(self.loginName.get(), self.loginPass.get())
                isValidVer = self.prgConn.checkVersion(self.ver)
                if isValidLogin and isValidVer and isValidStt:
                    self.isLogin.set(True)
                    self.frLogin.destroy()
                    self.winLogin.unbind('<Return>')
                    arceus(self.winLogin, self.prgConn, self.ver, self.varLoginName.get(), self.varLoginPass.get())
                else:
                    if not isValidLogin:
                        messagebox.showerror('Login Error', 'Please check your username or password.')
                    if isValidLogin and not isValidStt:
                        messagebox.showerror('Login Error', 'Your account is already active.')
                    if not isValidVer:
                        self.prgConn.tryLogin(self.loginName.get(), self.loginPass.get(), isLogin=False)
                        messagebox.showerror('Out of date version', 'Please download the newer version.')

                    self.winLogin.focus()
            else:
                messagebox.showerror('Input missing', 'Please input username and password.')
                self.winLogin.focus()
            try:
                self.loginName.configure(state='enable')
                self.loginPass.configure(state='enable')
                self.cbxChangePass.configure(state='enable')
                self.btnLoginSubmit.configure(state='enable')
                self.btnLoginCancel.configure(state='enable')
                if not (isValidLogin and isValidVer):
                    self.loginPass.delete(0, 'end')
                    self.loginPass.focus()
            except Exception:
                pass
        except Exception:
            messagebox.showerror('Error', traceback.format_exc())


    def submitForChangePass(self, event=None):
        try:
            self.loginName.configure(state='disabled')
            self.loginPass.configure(state='disabled')
            self.newPass1.configure(state='disabled')
            self.newPass2.configure(state='disabled')
            self.cbxChangePass.configure(state='disabled')
            self.btnLoginSubmit.configure(state='disabled')
            self.btnLoginCancel.configure(state='disabled')
            self.winLogin.after(1, self.winLogin.update())

            isNewPassValid = True
            if not self.loginName.get() or not self.loginPass.get():
                isNewPassValid = False
                messagebox.showerror('Input missing', 'Please input user name and current password.')
            if not self.newPass1.get() or not self.newPass2.get():
                isNewPassValid = False
                messagebox.showerror('Input missing', 'Please input your new password.')
            if self.newPass1.get() != self.newPass2.get():
                isNewPassValid = False
                messagebox.showerror('Input error', 'New password and confirm password must be the same.')

            if isNewPassValid:
                isValidPassChange, strValidPassChange = self.prgConn.tryChangePass(self.loginName.get(), self.loginPass.get(), self.newPass1.get())
                if isValidPassChange:
                    self.varIsChangePass.set(False)
                    self.loginChangePass()
                    messagebox.showinfo('Changing completed', strValidPassChange)
                else:
                    messagebox.showerror('Changing error', strValidPassChange)

            try:
                self.loginName.configure(state='enable')
                self.loginPass.configure(state='enable')
                self.newPass1.configure(state='enable')
                self.newPass2.configure(state='enable')
                self.cbxChangePass.configure(state='enable')
                self.btnLoginSubmit.configure(state='enable')
                self.btnLoginCancel.configure(state='enable')
                self.loginPass.delete(0, 'end')
                self.newPass1.delete(0, 'end')
                self.newPass2.delete(0, 'end')
            except Exception:
                pass
        except Exception:
            messagebox.showerror('Error', traceback.format_exc())