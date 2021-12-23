import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import os
import numpy as np
from class_Ditto import ditto
from class_Rotom import rotom
from class_Hurricane import hurricane
import traceback
from uuid import uuid4
import re
import time



class sweeper:

    def __init__(self, win, prgConn, strVer, loginName, loginPass, classArceus):
        self.swpWin = win

        # UserName & Password
        self.loginName = loginName
        self.loginPass = loginPass
        self.classArceus = classArceus

        # Version
        self.ver = strVer

        # Data objects
        self.rtm = rotom(None, None, [])
        self.dto = None
        self.hrc = hurricane(None, None, {})
        self.prgConn = prgConn

        # Init
        self.strTitle = f'Sweeper {self.ver}'
        self.swpWin.title(self.strTitle)
        self.swpWin.iconphoto(False, tk.PhotoImage(file='Icon\Sweeper.png'))
        self.swpWin.state('zoomed')
        self.swpWin.minsize(1200, 600)

        # Save status
        self.isChecklistSave = True

        # metadata status
        self.isDataActive = False

        # About
        strAbout = f'Sweeper version {self.ver}'
        strAbout += '\n\nAuthor: Hung.Dao\nEmail: hung.dao@ipsos.com'
        strAbout += '\n\nDescription: \nSweeper is developed with the aim of helping users to reduce their time spent on checking data. The data can be immediately not only checked after a checklist is created but also delivered to CSG after FW Manager has confirmed it.'
        self.strAbout = strAbout

        # tkinter Style
        swpStyle = ttk.Style()
        swpStyle.configure('mystyle.Treeview.Heading', font=('Calibri', 11, 'bold'))

        # ICON
        self.swpIcons = {
            'open': tk.PhotoImage(file='Icon\Menubar\Open.png').subsample(5, 5),
            'load': tk.PhotoImage(file='Icon\Menubar\Load.png').subsample(5, 5),
            'save': tk.PhotoImage(file='Icon\Menubar\Save.png').subsample(5, 5),
            'quit': tk.PhotoImage(file='Icon\Menubar\Quit.png').subsample(6, 6),
            'run': tk.PhotoImage(file='Icon\Menubar\Run.png').subsample(6, 6),
            'features': tk.PhotoImage(file='Icon\Menubar\Features.png').subsample(5, 5),
            'errorlog': tk.PhotoImage(file='Icon\Menubar\ErrorLog.png').subsample(5, 5),
            'about': tk.PhotoImage(file='Icon\Menubar\About.png').subsample(1, 1),

            'database': tk.PhotoImage(file='Icon\MetadataType\database.png').subsample(5, 5),
            'cats': tk.PhotoImage(file='Icon\MetadataType\cats.png').subsample(5, 5),
            'datetime': tk.PhotoImage(file='Icon\MetadataType\datetime.png').subsample(5, 5),
            'double': tk.PhotoImage(file='Icon\MetadataType\double.png').subsample(5, 5),
            'grid': tk.PhotoImage(file='Icon\MetadataType\grid.png').subsample(5, 5),
            'long': tk.PhotoImage(file='Icon\MetadataType\long.png').subsample(5, 5),
            'text': tk.PhotoImage(file=r'Icon\MetadataType\text.png').subsample(5, 5),
            'unknown': tk.PhotoImage(file=r'Icon\MetadataType\unknown.png').subsample(5, 5),
            'childnode': tk.PhotoImage(file=r'Icon\MetadataType\childnode.png').subsample(5, 5),

            'newcats': tk.PhotoImage(file=r'Icon\MetadataType\newcats.png').subsample(5, 5),
            'newdatetime': tk.PhotoImage(file=r'Icon\MetadataType\newdatetime.png').subsample(5, 5),
            'newdouble': tk.PhotoImage(file=r'Icon\MetadataType\newdouble.png').subsample(5, 5),
            'newgrid': tk.PhotoImage(file=r'Icon\MetadataType\newgrid.png').subsample(5, 5),
            'newlong': tk.PhotoImage(file=r'Icon\MetadataType\newlong.png').subsample(5, 5),
            'newtext': tk.PhotoImage(file=r'Icon\MetadataType\newtext.png').subsample(5, 5),
            'newunknown': tk.PhotoImage(file=r'Icon\MetadataType\newunknown.png').subsample(5, 5),
            'newchildnode': tk.PhotoImage(file=r'Icon\MetadataType\newchildnode.png').subsample(5, 5),

            'btnclear': tk.PhotoImage(file=r'Icon\Button\Clear.png').subsample(3, 3),
            'btnsubmit': tk.PhotoImage(file=r'Icon\Button\Submit.png').subsample(3, 3),
            'btnupdate': tk.PhotoImage(file=r'Icon\Button\Update.png').subsample(3, 3),

            'checklistCheck': tk.PhotoImage(file=r'Icon\Checklist\Check.png').subsample(5, 5),
            'checklistCreate': tk.PhotoImage(file=r'Icon\Checklist\Create.png').subsample(5, 5),

            'btnmoveup': tk.PhotoImage(file=r'Icon\Button\MoveUp.png').subsample(5, 5),
            'btnmovedown': tk.PhotoImage(file=r'Icon\Button\MoveDown.png').subsample(5, 5),
            'btndelete': tk.PhotoImage(file=r'Icon\Button\Delete.png').subsample(5, 5),
            'btnduplicate': tk.PhotoImage(file=r'Icon\Button\Duplicate.png').subsample(5, 5),

        }

        # MENU BAR
        self.swpWin.option_add('*tearOff', False)
        self.swpMenuBar = tk.Menu(self.swpWin, name='!menu')
        self.swpWin.config(menu=self.swpMenuBar)

        self.swpMenu = {
            'File': tk.Menu(self.swpMenuBar),
            'View': tk.Menu(self.swpMenuBar),
            'Run': tk.Menu(self.swpMenuBar),
            'Help': tk.Menu(self.swpMenuBar),
        }

        # MENU BAR - CREATE ITEMS
        self.swpMenuBar.add_cascade(menu=self.swpMenu['File'], label='File')
        self.swpMenuBar.add_cascade(menu=self.swpMenu['View'], label='View')
        self.swpMenuBar.add_cascade(menu=self.swpMenu['Run'], label='Run')
        self.swpMenuBar.add_cascade(menu=self.swpMenu['Help'], label='Help')

        # MENU BAR - ADD COMMAND
        self.swpMenu['File'].add_command(label='Open metadata', command=self.openMetadataFile)
        self.swpMenu['File'].add_separator()
        self.swpMenu['File'].add_command(label='Save checklist', command=self.saveChecklistToCsv)
        self.swpMenu['File'].add_command(label='Load checklist', command=self.loadChecklistFromCsv)
        self.swpMenu['File'].add_separator()
        self.swpMenu['File'].add_command(label='Features', command=self.backToArceus)
        self.swpMenu['File'].add_separator()
        self.swpMenu['File'].add_command(label='Quit', command=self.quitConfirmation)
        self.swpMenu['Run'].add_command(label='Run checklist', command=self.runChecklist)
        self.swpMenu['Help'].add_command(label='About', command=lambda: messagebox.showinfo('About', self.strAbout))
        self.swpIsErrLogActive = tk.BooleanVar()
        self.swpMenu['View'].add_checkbutton(label='Error log', variable=self.swpIsErrLogActive, command=self.errLogCallback)

        # MENU BAR - CONFIGURE
        self.swpMenu['File'].entryconfig('Open metadata', accelerator='Ctrl + O', image=self.swpIcons['open'], compound='left')
        self.swpMenu['File'].entryconfig('Save checklist', accelerator='Ctrl + S', image=self.swpIcons['save'], compound='left', state='disabled')
        self.swpMenu['File'].entryconfig('Load checklist', accelerator='Ctrl + L', image=self.swpIcons['load'], compound='left', state='disabled')
        self.swpMenu['File'].entryconfig('Features', image=self.swpIcons['features'], compound='left')
        self.swpMenu['File'].entryconfig('Quit', accelerator='Alt + Q', image=self.swpIcons['quit'], compound='left')
        self.swpMenu['View'].entryconfig('Error log', image=self.swpIcons['errorlog'], compound='left')
        self.swpMenu['Run'].entryconfig('Run checklist', accelerator='F5', image=self.swpIcons['run'], compound='left', state='disabled')
        self.swpMenu['Help'].entryconfig('About', image=self.swpIcons['about'], compound='left')


        #PANELS
        self.swpPanels = {
            'master': ttk.PanedWindow(self.swpWin, orient=tk.HORIZONTAL, name='!panedwindow'),
            'status': ttk.PanedWindow(self.swpWin, orient=tk.VERTICAL, name='!panedwindow2')
        }

        # PANELS - PACK
        self.swpPanels['master'].pack(fill='both', expand=True, side='top')
        self.swpPanels['status'].pack(fill='x', expand=True, side='left')

        self.swpFrames = {
            'metadata': ttk.Frame(self.swpPanels['master']),
            'material': ttk.Frame(self.swpPanels['master'], relief=tk.FLAT),
            'checklist': ttk.Frame(self.swpPanels['master'], relief=tk.FLAT),
            'status': ttk.Frame(self.swpPanels['status']),
        }

        self.swpMaterialFrames = {
            'question': ttk.Frame(self.swpFrames['material'], relief=tk.FLAT),
            'condition': ttk.Frame(self.swpFrames['material'], relief=tk.FLAT),
            'navigation': ttk.Frame(self.swpFrames['material'], relief=tk.FLAT),
        }

        # PANEL MASTER - ADD FRAMES
        self.swpPanels['master'].add(self.swpFrames['metadata'], weight=1)
        self.swpPanels['master'].add(self.swpFrames['material'], weight=2)
        self.swpPanels['master'].add(self.swpFrames['checklist'], weight=2)

        # PANEL MASTER - FRAMES MATERIAL - PACK FRAMES
        self.swpMaterialFrames['question'].grid(row=0, column=0, sticky='snew')
        self.swpMaterialFrames['navigation'].grid(row=0, column=1, sticky='snew')
        self.swpMaterialFrames['condition'].grid(row=1, column=0, columnspan=2, sticky='snew')
        self.swpFrames['material'].grid_columnconfigure(0, weight=10)
        self.swpFrames['material'].grid_columnconfigure(1, weight=1)
        self.swpFrames['material'].grid_rowconfigure(0, weight=1)
        self.swpFrames['material'].grid_rowconfigure(1, weight=10)

        # PANEL MASTER - FRAME METADATA - TREEVIEW
        self.swpTrvData = ttk.Treeview(self.swpFrames['metadata'], style='mystyle.Treeview')
        self.swpTrvData.pack(side='left', fill='both', expand=True)
        self.swpTrvData.column('#0', width=100)
        self.swpTrvData.heading('#0', text=f'Welcome, {self.loginName}')

        # PANEL MASTER - FRAME METADATA - TREEVIEW MENU
        self.swpTrvDataMenu = tk.Menu(self.swpTrvData, tearoff=0)
        self.swpTrvDataMenuItems = {
            'Check': tk.Menu(self.swpTrvDataMenu),
            'Create': tk.Menu(self.swpTrvDataMenu),
        }
        self.swpTrvDataMenu.add_cascade(menu=self.swpTrvDataMenuItems['Check'], label='Checking methods')
        self.swpTrvDataMenu.add_separator()
        self.swpTrvDataMenu.add_cascade(menu=self.swpTrvDataMenuItems['Create'], label='Creating methods')
        self.swpTrvDataMenuSel = tk.StringVar()
        for mth in self.hrc.method:
            self.swpTrvDataMenuItems['Check'].add_radiobutton(label=mth, variable=self.swpTrvDataMenuSel, command=self.trvDataMenuSelected)
        for mth in self.rtm.method:
            self.swpTrvDataMenuItems['Create'].add_radiobutton(label=mth, variable=self.swpTrvDataMenuSel, command=self.trvDataMenuSelected)

        # PANEL MASTER - FRAME METADATA - SCROLLBAR
        swpScrollbarData = ttk.Scrollbar(self.swpFrames['metadata'], orient=tk.VERTICAL, command=self.swpTrvData.yview)
        swpScrollbarData.pack(side='right', fill='y')
        self.swpTrvData.config(yscrollcommand=swpScrollbarData.set)

        # PANEL MASTER - FRAME MATERIAL - FRAME QUESTION - QUESTION LABEL
        self.swpCheckQreLbl = ttk.Label(self.swpMaterialFrames['question'], text='Question:')
        self.swpCheckQreLbl.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        # PANEL MASTER - FRAME MATERIAL - FRAME QUESTION - QUESTION ENTRY
        self.swpCheckQreEntryVal = tk.StringVar()
        self.swpCheckQreEntry = ttk.Entry(self.swpMaterialFrames['question'], textvariable=self.swpCheckQreEntryVal)
        self.swpCheckQreEntry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        # PANEL MASTER - FRAME MATERIAL - FRAME QUESTION - QUESTION CHECKBOX
        self.swpCheckQreCbxVal = tk.BooleanVar()
        self.swpCheckQreCbx = ttk.Checkbutton(self.swpMaterialFrames['question'], text='Disabled:',
                                              variable=self.swpCheckQreCbxVal, onvalue=True, offvalue=False,
                                              command=self.swpCheckQreCbxChange)
        self.swpCheckQreCbx.grid(row=1, column=0, padx=10, pady=0, sticky='w')

        # PANEL MASTER - FRAME MATERIAL - FRAME QUESTION - QUESTION COMBOBOX
        self.swpCheckQreMethodCbbVal = tk.StringVar()
        self.swpCheckQreMethodCbb = ttk.Combobox(self.swpMaterialFrames['question'], textvariable=self.swpCheckQreMethodCbbVal)
        self.swpCheckQreMethodCbb.grid(row=1, column=1, padx=10, pady=0, sticky='ew')

        self.swpMaterialFrames['question'].columnconfigure(1, weight=1)
        self.disableChildsOfFrame(self.swpMaterialFrames['question'], 'disabled')

        # FRAME MATERIAL - FRAME CONDITION - NOTEBOOK
        self.swpCondNotebook = ttk.Notebook(self.swpMaterialFrames['condition'])
        self.swpCondNotebook.pack(fill='both', expand=True)

        self.swpCondNotebookTabs = dict()
        lstMethods = self.hrc.method + self.rtm.method
        for mth in lstMethods:
            self.swpCondNotebookTabs[mth] = ttk.Frame(self.swpCondNotebook)
            self.swpCondNotebook.add(self.swpCondNotebookTabs[mth], text=mth)
            self.swpCondNotebook.tab(self.swpCondNotebookTabs[mth], state='hidden')

        self.swpCondNotebookTabItems = {
            'askedall': ttk.Label(self.swpCondNotebookTabs['askedall'], text='This method have no condition.'),
            'yearsubtract': {
                'label': ttk.Label(self.swpCondNotebookTabs['yearsubtract'], text='Year of birth question: '),
                'qreCond': ttk.Entry(self.swpCondNotebookTabs['yearsubtract']),
            },
            'catfromnum': {
                'label': ttk.Label(self.swpCondNotebookTabs['catfromnum'], text='Numeric question: '),
                'qreCond': ttk.Entry(self.swpCondNotebookTabs['catfromnum']),
                'instruction': ttk.Label(self.swpCondNotebookTabs['catfromnum'], justify='left',
                                        text='Instruction:\n1. {cat}=x to y\n2. {cat}=over x\n3. {cat}=under x'),
                'itemCond1': ttk.Entry(self.swpCondNotebookTabs['catfromnum']),
                'itemCond2': ttk.Entry(self.swpCondNotebookTabs['catfromnum']),
                'itemCond3': ttk.Entry(self.swpCondNotebookTabs['catfromnum']),
                'itemCond4': ttk.Entry(self.swpCondNotebookTabs['catfromnum']),
                'itemCond5': ttk.Entry(self.swpCondNotebookTabs['catfromnum']),
                'itemCond6': ttk.Entry(self.swpCondNotebookTabs['catfromnum']),
                'itemCond7': ttk.Entry(self.swpCondNotebookTabs['catfromnum']),
                'itemCond8': ttk.Entry(self.swpCondNotebookTabs['catfromnum']),
                'itemCond9': ttk.Entry(self.swpCondNotebookTabs['catfromnum']),
                'itemCond10': ttk.Entry(self.swpCondNotebookTabs['catfromnum']),
            },
            'catfromcats': {
                'label': ttk.Label(self.swpCondNotebookTabs['catfromcats'], text='Categorical question: '),
                'qreCond': ttk.Entry(self.swpCondNotebookTabs['catfromcats']),
                'instruction': ttk.Label(self.swpCondNotebookTabs['catfromcats'], justify='left',
                                        text='Instruction:\n1. {_1}={_1,_2}\n2. {_2}={_3,_4}\n3. {_3}={_5}'),
                'itemCond1': ttk.Entry(self.swpCondNotebookTabs['catfromcats']),
                'itemCond2': ttk.Entry(self.swpCondNotebookTabs['catfromcats']),
                'itemCond3': ttk.Entry(self.swpCondNotebookTabs['catfromcats']),
                'itemCond4': ttk.Entry(self.swpCondNotebookTabs['catfromcats']),
                'itemCond5': ttk.Entry(self.swpCondNotebookTabs['catfromcats']),
                'itemCond6': ttk.Entry(self.swpCondNotebookTabs['catfromcats']),
                'itemCond7': ttk.Entry(self.swpCondNotebookTabs['catfromcats']),
                'itemCond8': ttk.Entry(self.swpCondNotebookTabs['catfromcats']),
                'itemCond9': ttk.Entry(self.swpCondNotebookTabs['catfromcats']),
                'itemCond10': ttk.Entry(self.swpCondNotebookTabs['catfromcats']),
            },
            'lsm2': tk.Label(self.swpCondNotebookTabs['lsm2'], text='This method have no condition.'),
            'sum': {
                'label1': ttk.Label(self.swpCondNotebookTabs['sum'], text='Numeric question 1: '),
                'label2': ttk.Label(self.swpCondNotebookTabs['sum'], text='Numeric question 2: '),
                'label3': ttk.Label(self.swpCondNotebookTabs['sum'], text='Numeric question 3: '),
                'label4': ttk.Label(self.swpCondNotebookTabs['sum'], text='Numeric question 4: '),
                'label5': ttk.Label(self.swpCondNotebookTabs['sum'], text='Numeric question 5: '),
                'label6': ttk.Label(self.swpCondNotebookTabs['sum'], text='Numeric question 6: '),
                'label7': ttk.Label(self.swpCondNotebookTabs['sum'], text='Numeric question 7: '),
                'label8': ttk.Label(self.swpCondNotebookTabs['sum'], text='Numeric question 8: '),
                'label9': ttk.Label(self.swpCondNotebookTabs['sum'], text='Numeric question 9: '),
                'label10': ttk.Label(self.swpCondNotebookTabs['sum'], text='Numeric question 10: '),

                'qreCond1': ttk.Entry(self.swpCondNotebookTabs['sum']),
                'qreCond2': ttk.Entry(self.swpCondNotebookTabs['sum']),
                'qreCond3': ttk.Entry(self.swpCondNotebookTabs['sum']),
                'qreCond4': ttk.Entry(self.swpCondNotebookTabs['sum']),
                'qreCond5': ttk.Entry(self.swpCondNotebookTabs['sum']),
                'qreCond6': ttk.Entry(self.swpCondNotebookTabs['sum']),
                'qreCond7': ttk.Entry(self.swpCondNotebookTabs['sum']),
                'qreCond8': ttk.Entry(self.swpCondNotebookTabs['sum']),
                'qreCond9': ttk.Entry(self.swpCondNotebookTabs['sum']),
                'qreCond10': ttk.Entry(self.swpCondNotebookTabs['sum']),
                'instruction': ttk.Label(self.swpCondNotebookTabs['sum'], justify='left',
                                        text='Instruction:\nQre = Qre1+Qre2+...+Qre10\nnum100 = Qre1+Qre2+...+Qre10'),
            },
            'allin': {
                'label1': ttk.Label(self.swpCondNotebookTabs['allin'], text='Question: '),
                'label2': ttk.Label(self.swpCondNotebookTabs['allin'], justify='left',
                                   text='Exclusive codes: \n(ex: {_99,_98})'),
                'qreCond': ttk.Entry(self.swpCondNotebookTabs['allin']),
                'exclusive': ttk.Entry(self.swpCondNotebookTabs['allin']),
            },
            'containsany': {
                'label': ttk.Label(self.swpCondNotebookTabs['containsany'], text='Question / Categories: '),
                'qreCond': ttk.Entry(self.swpCondNotebookTabs['containsany']),
            },
            'notequal': {
                'label': ttk.Label(self.swpCondNotebookTabs['notequal'], text='SA question: '),
                'qreCond': ttk.Entry(self.swpCondNotebookTabs['notequal']),
            },
            'equal': {
                'label': ttk.Label(self.swpCondNotebookTabs['equal'], text='SA question: '),
                'qreCond': ttk.Entry(self.swpCondNotebookTabs['equal']),
            },
            'when': {
                'label1': ttk.Label(self.swpCondNotebookTabs['when'], text='(..'),
                'label2': ttk.Label(self.swpCondNotebookTabs['when'], text='Question'),
                'label3': ttk.Label(self.swpCondNotebookTabs['when'], text=''),
                'label4': ttk.Label(self.swpCondNotebookTabs['when'], text='Values'),
                'label5': ttk.Label(self.swpCondNotebookTabs['when'], text='..)'),
                'label6': ttk.Label(self.swpCondNotebookTabs['when'], text='and/or'),

                'itemStm1': ttk.Label(self.swpCondNotebookTabs['when'], text='='),
                'itemStm2': ttk.Label(self.swpCondNotebookTabs['when'], text='='),
                'itemStm3': ttk.Label(self.swpCondNotebookTabs['when'], text='='),
                'itemStm4': ttk.Label(self.swpCondNotebookTabs['when'], text='='),
                'itemStm5': ttk.Label(self.swpCondNotebookTabs['when'], text='='),
                'itemStm6': ttk.Label(self.swpCondNotebookTabs['when'], text='='),
                'itemStm7': ttk.Label(self.swpCondNotebookTabs['when'], text='='),
                'itemStm8': ttk.Label(self.swpCondNotebookTabs['when'], text='='),
                'itemStm9': ttk.Label(self.swpCondNotebookTabs['when'], text='='),
                'itemStm10': ttk.Label(self.swpCondNotebookTabs['when'], text='='),

                'qreCond1': ttk.Entry(self.swpCondNotebookTabs['when']),
                'qreCond2': ttk.Entry(self.swpCondNotebookTabs['when']),
                'qreCond3': ttk.Entry(self.swpCondNotebookTabs['when']),
                'qreCond4': ttk.Entry(self.swpCondNotebookTabs['when']),
                'qreCond5': ttk.Entry(self.swpCondNotebookTabs['when']),
                'qreCond6': ttk.Entry(self.swpCondNotebookTabs['when']),
                'qreCond7': ttk.Entry(self.swpCondNotebookTabs['when']),
                'qreCond8': ttk.Entry(self.swpCondNotebookTabs['when']),
                'qreCond9': ttk.Entry(self.swpCondNotebookTabs['when']),
                'qreCond10': ttk.Entry(self.swpCondNotebookTabs['when']),

                'itemOpen1': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', '('], state='readonly', width=5),
                'itemVal1': ttk.Entry(self.swpCondNotebookTabs['when']),
                'itemClose1': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', ')'], state='readonly', width=5),
                'itemConj1': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', 'and', 'or'], state='readonly', width=5),

                'itemOpen2': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', '('], state='readonly', width=5),
                'itemVal2': ttk.Entry(self.swpCondNotebookTabs['when']),
                'itemClose2': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', ')'], state='readonly', width=5),
                'itemConj2': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', 'and', 'or'], state='readonly', width=5),

                'itemOpen3': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', '('], state='readonly', width=5),
                'itemVal3': ttk.Entry(self.swpCondNotebookTabs['when']),
                'itemClose3': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', ')'], state='readonly', width=5),
                'itemConj3': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', 'and', 'or'], state='readonly', width=5),

                'itemOpen4': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', '('], state='readonly', width=5),
                'itemVal4': ttk.Entry(self.swpCondNotebookTabs['when']),
                'itemClose4': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', ')'], state='readonly', width=5),
                'itemConj4': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', 'and', 'or'], state='readonly', width=5),

                'itemOpen5': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', '('], state='readonly', width=5),
                'itemVal5': ttk.Entry(self.swpCondNotebookTabs['when']),
                'itemClose5': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', ')'], state='readonly', width=5),
                'itemConj5': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', 'and', 'or'], state='readonly', width=5),

                'itemOpen6': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', '('], state='readonly', width=5),
                'itemVal6': ttk.Entry(self.swpCondNotebookTabs['when']),
                'itemClose6': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', ')'], state='readonly', width=5),
                'itemConj6': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', 'and', 'or'], state='readonly', width=5),

                'itemOpen7': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', '('], state='readonly', width=5),
                'itemVal7': ttk.Entry(self.swpCondNotebookTabs['when']),
                'itemClose7': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', ')'], state='readonly', width=5),
                'itemConj7': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', 'and', 'or'], state='readonly', width=5),

                'itemOpen8': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', '('], state='readonly', width=5),
                'itemVal8': ttk.Entry(self.swpCondNotebookTabs['when']),
                'itemClose8': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', ')'], state='readonly', width=5),
                'itemConj8': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', 'and', 'or'], state='readonly', width=5),

                'itemOpen9': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', '('], state='readonly', width=5),
                'itemVal9': ttk.Entry(self.swpCondNotebookTabs['when']),
                'itemClose9': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', ')'], state='readonly', width=5),
                'itemConj9': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', 'and', 'or'], state='readonly', width=5),

                'itemOpen10': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', '('], state='readonly', width=5),
                'itemVal10': ttk.Entry(self.swpCondNotebookTabs['when']),
                'itemClose10': ttk.Combobox(self.swpCondNotebookTabs['when'], values=['', ')'], state='readonly', width=5),
                'itemConj10': ttk.Label(self.swpCondNotebookTabs['when'], width=5),

                'instruction': ttk.Label(self.swpCondNotebookTabs['when'], justify='left',
                text='Instruction:\nValues can be input: "Null" or "~Null" or "{_cats}" or "~{_cats}"'),
            },
            'iterfilby': {
                'label': ttk.Label(self.swpCondNotebookTabs['iterfilby'], text='Filter question: '),
                'qreCond': ttk.Entry(self.swpCondNotebookTabs['iterfilby']),
                'instruction': ttk.Label(self.swpCondNotebookTabs['iterfilby'], justify='left',
                text='''Instruction:
                - Checking question must contain as least 1 of '[..]'(cuz only loop type can be filtered by iterations).
                - Checking question's level > condition question's level.
                - If condition question in loop then checking question must have same parent with it. 
                '''),
            },
            'logic': {
                'label1': ttk.Label(self.swpCondNotebookTabs['logic'], text='(..'),
                'label2': ttk.Label(self.swpCondNotebookTabs['logic'], text='Question'),
                'label3': ttk.Label(self.swpCondNotebookTabs['logic'], text=''),
                'label4': ttk.Label(self.swpCondNotebookTabs['logic'], text='Values'),
                'label5': ttk.Label(self.swpCondNotebookTabs['logic'], text='..)'),
                'label6': ttk.Label(self.swpCondNotebookTabs['logic'], text='and/or'),

                'itemStm0': ttk.Label(self.swpCondNotebookTabs['logic'], text='='),
                'itemStm1': ttk.Label(self.swpCondNotebookTabs['logic'], text='='),
                'itemStm2': ttk.Label(self.swpCondNotebookTabs['logic'], text='='),
                'itemStm3': ttk.Label(self.swpCondNotebookTabs['logic'], text='='),
                'itemStm4': ttk.Label(self.swpCondNotebookTabs['logic'], text='='),
                'itemStm5': ttk.Label(self.swpCondNotebookTabs['logic'], text='='),
                'itemStm6': ttk.Label(self.swpCondNotebookTabs['logic'], text='='),
                'itemStm7': ttk.Label(self.swpCondNotebookTabs['logic'], text='='),
                'itemStm8': ttk.Label(self.swpCondNotebookTabs['logic'], text='='),
                'itemStm9': ttk.Label(self.swpCondNotebookTabs['logic'], text='='),
                'itemStm10': ttk.Label(self.swpCondNotebookTabs['logic'], text='='),

                'qreCond0': ttk.Label(self.swpCondNotebookTabs['logic'], text='qre'),
                'qreCond1': ttk.Entry(self.swpCondNotebookTabs['logic']),
                'qreCond2': ttk.Entry(self.swpCondNotebookTabs['logic']),
                'qreCond3': ttk.Entry(self.swpCondNotebookTabs['logic']),
                'qreCond4': ttk.Entry(self.swpCondNotebookTabs['logic']),
                'qreCond5': ttk.Entry(self.swpCondNotebookTabs['logic']),
                'qreCond6': ttk.Entry(self.swpCondNotebookTabs['logic']),
                'qreCond7': ttk.Entry(self.swpCondNotebookTabs['logic']),
                'qreCond8': ttk.Entry(self.swpCondNotebookTabs['logic']),
                'qreCond9': ttk.Entry(self.swpCondNotebookTabs['logic']),
                'qreCond10': ttk.Entry(self.swpCondNotebookTabs['logic']),

                'itemOpen0': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', '('], state='readonly', width=5),
                'itemVal0': ttk.Entry(self.swpCondNotebookTabs['logic']),
                'itemClose0': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', ')'], state='readonly', width=5),
                'itemConj0': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', 'and', 'or'], state='readonly', width=5),

                'itemOpen1': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', '('], state='readonly', width=5),
                'itemVal1': ttk.Entry(self.swpCondNotebookTabs['logic']),
                'itemClose1': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', ')'], state='readonly', width=5),
                'itemConj1': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', 'and', 'or'], state='readonly', width=5),

                'itemOpen2': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', '('], state='readonly', width=5),
                'itemVal2': ttk.Entry(self.swpCondNotebookTabs['logic']),
                'itemClose2': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', ')'], state='readonly', width=5),
                'itemConj2': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', 'and', 'or'], state='readonly', width=5),

                'itemOpen3': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', '('], state='readonly', width=5),
                'itemVal3': ttk.Entry(self.swpCondNotebookTabs['logic']),
                'itemClose3': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', ')'], state='readonly', width=5),
                'itemConj3': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', 'and', 'or'], state='readonly', width=5),

                'itemOpen4': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', '('], state='readonly', width=5),
                'itemVal4': ttk.Entry(self.swpCondNotebookTabs['logic']),
                'itemClose4': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', ')'], state='readonly', width=5),
                'itemConj4': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', 'and', 'or'], state='readonly', width=5),

                'itemOpen5': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', '('], state='readonly', width=5),
                'itemVal5': ttk.Entry(self.swpCondNotebookTabs['logic']),
                'itemClose5': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', ')'], state='readonly', width=5),
                'itemConj5': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', 'and', 'or'], state='readonly', width=5),

                'itemOpen6': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', '('], state='readonly', width=5),
                'itemVal6': ttk.Entry(self.swpCondNotebookTabs['logic']),
                'itemClose6': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', ')'], state='readonly', width=5),
                'itemConj6': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', 'and', 'or'], state='readonly', width=5),

                'itemOpen7': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', '('], state='readonly', width=5),
                'itemVal7': ttk.Entry(self.swpCondNotebookTabs['logic']),
                'itemClose7': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', ')'], state='readonly', width=5),
                'itemConj7': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', 'and', 'or'], state='readonly', width=5),

                'itemOpen8': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', '('], state='readonly', width=5),
                'itemVal8': ttk.Entry(self.swpCondNotebookTabs['logic']),
                'itemClose8': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', ')'], state='readonly', width=5),
                'itemConj8': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', 'and', 'or'], state='readonly', width=5),

                'itemOpen9': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', '('], state='readonly', width=5),
                'itemVal9': ttk.Entry(self.swpCondNotebookTabs['logic']),
                'itemClose9': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', ')'], state='readonly', width=5),
                'itemConj9': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', 'and', 'or'], state='readonly', width=5),

                'itemOpen10': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', '('], state='readonly', width=5),
                'itemVal10': ttk.Entry(self.swpCondNotebookTabs['logic']),
                'itemClose10': ttk.Combobox(self.swpCondNotebookTabs['logic'], values=['', ')'], state='readonly', width=5),
                'itemConj10': ttk.Label(self.swpCondNotebookTabs['logic'], width=5),

                'instruction': ttk.Label(self.swpCondNotebookTabs['logic'], justify='left',
                text='Instruction:\nValues can be input: "Null" or "~Null" or "{_cats}" or "~{_cats}"'),
            },
            'merge': {
                'label1': ttk.Label(self.swpCondNotebookTabs['merge'], text='Categorical question 1: '),
                'label2': ttk.Label(self.swpCondNotebookTabs['merge'], text='Categorical question 2: '),
                'label3': ttk.Label(self.swpCondNotebookTabs['merge'], text='Categorical question 3: '),
                'label4': ttk.Label(self.swpCondNotebookTabs['merge'], text='Categorical question 4: '),
                'label5': ttk.Label(self.swpCondNotebookTabs['merge'], text='Categorical question 5: '),
                'label6': ttk.Label(self.swpCondNotebookTabs['merge'], text='Categorical question 6: '),
                'label7': ttk.Label(self.swpCondNotebookTabs['merge'], text='Categorical question 7: '),
                'label8': ttk.Label(self.swpCondNotebookTabs['merge'], text='Categorical question 8: '),
                'label9': ttk.Label(self.swpCondNotebookTabs['merge'], text='Categorical question 9: '),
                'label10': ttk.Label(self.swpCondNotebookTabs['merge'], text='Categorical question 10: '),
                'label11': ttk.Label(self.swpCondNotebookTabs['merge'], text='Exclusive categories: '),

                'qreCond1': ttk.Entry(self.swpCondNotebookTabs['merge']),
                'qreCond2': ttk.Entry(self.swpCondNotebookTabs['merge']),
                'qreCond3': ttk.Entry(self.swpCondNotebookTabs['merge']),
                'qreCond4': ttk.Entry(self.swpCondNotebookTabs['merge']),
                'qreCond5': ttk.Entry(self.swpCondNotebookTabs['merge']),
                'qreCond6': ttk.Entry(self.swpCondNotebookTabs['merge']),
                'qreCond7': ttk.Entry(self.swpCondNotebookTabs['merge']),
                'qreCond8': ttk.Entry(self.swpCondNotebookTabs['merge']),
                'qreCond9': ttk.Entry(self.swpCondNotebookTabs['merge']),
                'qreCond10': ttk.Entry(self.swpCondNotebookTabs['merge']),

                'exclusive': ttk.Entry(self.swpCondNotebookTabs['merge']),

                'instruction': ttk.Label(self.swpCondNotebookTabs['merge'], justify='left',
                                    text='Instruction:\nQre = (Qre1+Qre2+...+Qre10)-exclusive'
                                         '\nQre = (Qre1+{_1,_2,_3}+...+Qre10)-exclusive'),
            },
            'assign': {
                'label00': ttk.Label(self.swpCondNotebookTabs['assign'], text='From'),
                'label01': ttk.Label(self.swpCondNotebookTabs['assign'], text='Question 1:'),
                'label02': ttk.Label(self.swpCondNotebookTabs['assign'], text='Question 2:'),
                'label03': ttk.Label(self.swpCondNotebookTabs['assign'], text='Question 3:'),
                'label04': ttk.Label(self.swpCondNotebookTabs['assign'], text='Question 4:'),
                'label05': ttk.Label(self.swpCondNotebookTabs['assign'], text='Question 5:'),
                'label06': ttk.Label(self.swpCondNotebookTabs['assign'], justify='left',
                                     text='Exclusive codes: \n(ex: {_99,_98})'),
                'label10': ttk.Label(self.swpCondNotebookTabs['assign'], text='When'),
                'label11': ttk.Label(self.swpCondNotebookTabs['assign'], text='(..'),
                'label12': ttk.Label(self.swpCondNotebookTabs['assign'], text='Question'),
                'label13': ttk.Label(self.swpCondNotebookTabs['assign'], text=''),
                'label14': ttk.Label(self.swpCondNotebookTabs['assign'], text='Values'),
                'label15': ttk.Label(self.swpCondNotebookTabs['assign'], text='..)'),
                'label16': ttk.Label(self.swpCondNotebookTabs['assign'], text='and/or'),

                'instruction': ttk.Label(self.swpCondNotebookTabs['assign'], justify='left',
                text='Instruction:\nQre = Qre1+Qre2+...+Qre5 when (QreX is {_1} and QreY is {_2}) or QreZ not {_3}'),

                'itemStm1': ttk.Label(self.swpCondNotebookTabs['assign'], text='='),
                'itemStm2': ttk.Label(self.swpCondNotebookTabs['assign'], text='='),
                'itemStm3': ttk.Label(self.swpCondNotebookTabs['assign'], text='='),
                'itemStm4': ttk.Label(self.swpCondNotebookTabs['assign'], text='='),
                'itemStm5': ttk.Label(self.swpCondNotebookTabs['assign'], text='='),

                'qreCond1': ttk.Entry(self.swpCondNotebookTabs['assign']),
                'qreCond2': ttk.Entry(self.swpCondNotebookTabs['assign']),
                'qreCond3': ttk.Entry(self.swpCondNotebookTabs['assign']),
                'qreCond4': ttk.Entry(self.swpCondNotebookTabs['assign']),
                'qreCond5': ttk.Entry(self.swpCondNotebookTabs['assign']),

                'exclusive': ttk.Entry(self.swpCondNotebookTabs['assign']),

                'itemOpen1': ttk.Combobox(self.swpCondNotebookTabs['assign'], values=['', '('], state='readonly', width=5),
                'itemQre1': ttk.Entry(self.swpCondNotebookTabs['assign']),
                'itemVal1': ttk.Entry(self.swpCondNotebookTabs['assign']),
                'itemClose1': ttk.Combobox(self.swpCondNotebookTabs['assign'], values=['', ')'], state='readonly', width=5),
                'itemConj1': ttk.Combobox(self.swpCondNotebookTabs['assign'], values=['', 'and', 'or'], state='readonly', width=5),

                'itemOpen2': ttk.Combobox(self.swpCondNotebookTabs['assign'], values=['', '('], state='readonly', width=5),
                'itemQre2': ttk.Entry(self.swpCondNotebookTabs['assign']),
                'itemVal2': ttk.Entry(self.swpCondNotebookTabs['assign']),
                'itemClose2': ttk.Combobox(self.swpCondNotebookTabs['assign'], values=['', ')'], state='readonly', width=5),
                'itemConj2': ttk.Combobox(self.swpCondNotebookTabs['assign'], values=['', 'and', 'or'], state='readonly', width=5),

                'itemOpen3': ttk.Combobox(self.swpCondNotebookTabs['assign'], values=['', '('], state='readonly', width=5),
                'itemQre3': ttk.Entry(self.swpCondNotebookTabs['assign']),
                'itemVal3': ttk.Entry(self.swpCondNotebookTabs['assign']),
                'itemClose3': ttk.Combobox(self.swpCondNotebookTabs['assign'], values=['', ')'], state='readonly', width=5),
                'itemConj3': ttk.Combobox(self.swpCondNotebookTabs['assign'], values=['', 'and', 'or'], state='readonly', width=5),

                'itemOpen4': ttk.Combobox(self.swpCondNotebookTabs['assign'], values=['', '('], state='readonly', width=5),
                'itemQre4': ttk.Entry(self.swpCondNotebookTabs['assign']),
                'itemVal4': ttk.Entry(self.swpCondNotebookTabs['assign']),
                'itemClose4': ttk.Combobox(self.swpCondNotebookTabs['assign'], values=['', ')'], state='readonly', width=5),
                'itemConj4': ttk.Combobox(self.swpCondNotebookTabs['assign'], values=['', 'and', 'or'], state='readonly', width=5),

                'itemOpen5': ttk.Combobox(self.swpCondNotebookTabs['assign'], values=['', '('], state='readonly', width=5),
                'itemQre5': ttk.Entry(self.swpCondNotebookTabs['assign']),
                'itemVal5': ttk.Entry(self.swpCondNotebookTabs['assign']),
                'itemClose5': ttk.Combobox(self.swpCondNotebookTabs['assign'], values=['', ')'], state='readonly', width=5),
                'itemConj5': ttk.Label(self.swpCondNotebookTabs['assign'], width=5),

            },
            'count': {
                'label1': ttk.Label(self.swpCondNotebookTabs['count'], text='Categorical question: '),
                'label2': ttk.Label(self.swpCondNotebookTabs['count'], justify='left', text='Exclusive codes: \n(ex: {_99,_98})'),
                'qreCond': ttk.Entry(self.swpCondNotebookTabs['count']),
                'exclusive': ttk.Entry(self.swpCondNotebookTabs['count']),
            },
            'difference': {
                'label0': ttk.Label(self.swpCondNotebookTabs['difference'], text='Base question'),
                'label00': ttk.Label(self.swpCondNotebookTabs['difference'], text='Childs question'),
                'label1': ttk.Label(self.swpCondNotebookTabs['difference'], text='Categorical question 1: '),
                'label2': ttk.Label(self.swpCondNotebookTabs['difference'], text='Categorical question 2: '),
                'label3': ttk.Label(self.swpCondNotebookTabs['difference'], text='Categorical question 3: '),
                'label4': ttk.Label(self.swpCondNotebookTabs['difference'], text='Categorical question 4: '),
                'label5': ttk.Label(self.swpCondNotebookTabs['difference'], text='Categorical question 5: '),
                'label6': ttk.Label(self.swpCondNotebookTabs['difference'], text='Categorical question 6: '),
                'label7': ttk.Label(self.swpCondNotebookTabs['difference'], text='Categorical question 7: '),
                'label8': ttk.Label(self.swpCondNotebookTabs['difference'], text='Categorical question 8: '),
                'label9': ttk.Label(self.swpCondNotebookTabs['difference'], text='Categorical question 9: '),
                'label10': ttk.Label(self.swpCondNotebookTabs['difference'], text='Categorical question 10: '),

                'qreCond1': ttk.Entry(self.swpCondNotebookTabs['difference']),
                'qreCond2': ttk.Entry(self.swpCondNotebookTabs['difference']),
                'qreCond3': ttk.Entry(self.swpCondNotebookTabs['difference']),
                'qreCond4': ttk.Entry(self.swpCondNotebookTabs['difference']),
                'qreCond5': ttk.Entry(self.swpCondNotebookTabs['difference']),
                'qreCond6': ttk.Entry(self.swpCondNotebookTabs['difference']),
                'qreCond7': ttk.Entry(self.swpCondNotebookTabs['difference']),
                'qreCond8': ttk.Entry(self.swpCondNotebookTabs['difference']),
                'qreCond9': ttk.Entry(self.swpCondNotebookTabs['difference']),
                'qreCond10': ttk.Entry(self.swpCondNotebookTabs['difference']),

                'instruction': ttk.Label(self.swpCondNotebookTabs['difference'], justify='left',
                text='Instruction:\nQre1 = {_1,_2,_3,_4,_5,_6}\nQre2 = {_2,_3}\nQre3 = {_5}\n=>Qre = {_1,_4,_6}'),
            },
            'intersection': {
                'label0': ttk.Label(self.swpCondNotebookTabs['intersection'], text='Base question'),
                'label00': ttk.Label(self.swpCondNotebookTabs['intersection'], text='Childs question'),
                'label1': ttk.Label(self.swpCondNotebookTabs['intersection'], text='Categorical question 1: '),
                'label2': ttk.Label(self.swpCondNotebookTabs['intersection'], text='Categorical question 2: '),
                'label3': ttk.Label(self.swpCondNotebookTabs['intersection'], text='Categorical question 3: '),
                'label4': ttk.Label(self.swpCondNotebookTabs['intersection'], text='Categorical question 4: '),
                'label5': ttk.Label(self.swpCondNotebookTabs['intersection'], text='Categorical question 5: '),
                'label6': ttk.Label(self.swpCondNotebookTabs['intersection'], text='Categorical question 6: '),
                'label7': ttk.Label(self.swpCondNotebookTabs['intersection'], text='Categorical question 7: '),
                'label8': ttk.Label(self.swpCondNotebookTabs['intersection'], text='Categorical question 8: '),
                'label9': ttk.Label(self.swpCondNotebookTabs['intersection'], text='Categorical question 9: '),
                'label10': ttk.Label(self.swpCondNotebookTabs['intersection'], text='Categorical question 10: '),

                'qreCond1': ttk.Entry(self.swpCondNotebookTabs['intersection']),
                'qreCond2': ttk.Entry(self.swpCondNotebookTabs['intersection']),
                'qreCond3': ttk.Entry(self.swpCondNotebookTabs['intersection']),
                'qreCond4': ttk.Entry(self.swpCondNotebookTabs['intersection']),
                'qreCond5': ttk.Entry(self.swpCondNotebookTabs['intersection']),
                'qreCond6': ttk.Entry(self.swpCondNotebookTabs['intersection']),
                'qreCond7': ttk.Entry(self.swpCondNotebookTabs['intersection']),
                'qreCond8': ttk.Entry(self.swpCondNotebookTabs['intersection']),
                'qreCond9': ttk.Entry(self.swpCondNotebookTabs['intersection']),
                'qreCond10': ttk.Entry(self.swpCondNotebookTabs['intersection']),

                'instruction': ttk.Label(self.swpCondNotebookTabs['intersection'], justify='left',
                text='Instruction:\nQre1 = {_1,_2,_3,_4,_5,_6}\nQre2 = {_2,_5,_7}\nQre3 = {_5,_8}\n=>Qre = {_2,_5}'),
            },
            'getiters': {
                'label1': ttk.Label(self.swpCondNotebookTabs['getiters'], text='Grid question'),
                'label2': ttk.Label(self.swpCondNotebookTabs['getiters'], text='Get which'),

                'qreCond': ttk.Entry(self.swpCondNotebookTabs['getiters']),
                'itemVal': ttk.Combobox(self.swpCondNotebookTabs['getiters'],
                values=['all', '{_cats}', '~{_cats}', '{_num[><=]XXX}', '~{_num[><=]XXX}', 'Null', '~Null', 'min', 'max'],
                width=20),

                'instruction': ttk.Label(self.swpCondNotebookTabs['getiters'], justify='left',
                text='Instruction:\n\n1. GridQre = Grid[..]._Codes is categorical'
                '\n\n- Grid[{_1}]._Codes = {_1,_2}\n- Grid[{_2}]._Codes = Null\n- Grid[{_3}]._Codes = {_1,_3}'
                '\n- Grid[{_4}]._Codes = Null\n- Grid[{_5}]._Codes = {_2,_3}'
                '\n\n=> if Get which = all then NewQre = {_1,_2,_3,_4,_5}'
                '\n=> if Get which = {_1} then NewQre = {_1,_3}'
                '\n=> if Get which = ~{_1} then NewQre = {_2,_4,_5}'
                '\n=> if Get which = Null then NewQre = {_2,_4}'
                '\n=> if Get which = ~Null then NewQre = {_1,_3,_5}'
                '\n\n2. GridQre = Grid[..]._Codes is numeric'
                '\n\n- Grid[{_1}]._Codes = 15\n- Grid[{_2}]._Codes = 25\n- Grid[{_3}]._Codes = Null'
                '\n- Grid[{_4}]._Codes = Null\n- Grid[{_5}]._Codes = 35'
                '\n\n=> if Get which = all then NewQre = {_1,_2,_3,_4,_5}'
                '\n=> if Get which = {_num=25} then NewQre = {_2}'
                '\n=> if Get which = ~{_num=25} then NewQre = {_1,_3,_4,_5}'
                '\n=> if Get which = {_num>25} then NewQre = {_5}'
                '\n=> if Get which = {_num<25} then NewQre = {_1}'
                '\n=> if Get which = Null then NewQre = {_3,_4}'
                '\n=> if Get which = ~Null then NewQre = {_1,_2,_5}'
                '\n=> if Get which = min then NewQre = {_1}'
                '\n=> if Get which = max then NewQre = {_5}'),
            },
            'numcompared': {
                'label1': ttk.Label(self.swpCondNotebookTabs['numcompared'], text='Numeric question 1'),
                'label2': ttk.Label(self.swpCondNotebookTabs['numcompared'], text='Numeric question 2'),
                'qreCond1': ttk.Entry(self.swpCondNotebookTabs['numcompared']),
                'qreCond2': ttk.Entry(self.swpCondNotebookTabs['numcompared']),
                'instruction': ttk.Label(self.swpCondNotebookTabs['numcompared'], justify='left',
                text='Instruction:\n\n1. NumQre1 = NumQre2 => {_equal}\n2. NumQre1 > NumQre2 => {_over}\n'
                '3. NumQre1 < NumQre2 => {_under}\n4. NumQre1 = null or NumQre2 = null => {}\n'
                '5. NumQre1 and NumQre2 can be formated {_num123}')
            },
            'dropped': {
                'label00': ttk.Label(self.swpCondNotebookTabs['dropped'], text='From'),
                'label01': ttk.Label(self.swpCondNotebookTabs['dropped'], text='Question 1:'),
                'label02': ttk.Label(self.swpCondNotebookTabs['dropped'], text='Question 2:'),
                'label03': ttk.Label(self.swpCondNotebookTabs['dropped'], text='Question 3:'),
                'label04': ttk.Label(self.swpCondNotebookTabs['dropped'], text='Question 4:'),
                'label05': ttk.Label(self.swpCondNotebookTabs['dropped'], text='Question 5:'),
                'label06': ttk.Label(self.swpCondNotebookTabs['dropped'], justify='left',
                                     text='Exclusive codes: \n(ex: {_99,_98})'),
                'label10': ttk.Label(self.swpCondNotebookTabs['dropped'], text='When'),
                'label11': ttk.Label(self.swpCondNotebookTabs['dropped'], text='(..'),
                'label12': ttk.Label(self.swpCondNotebookTabs['dropped'], text='Question'),
                'label13': ttk.Label(self.swpCondNotebookTabs['dropped'], text=''),
                'label14': ttk.Label(self.swpCondNotebookTabs['dropped'], text='Values'),
                'label15': ttk.Label(self.swpCondNotebookTabs['dropped'], text='..)'),
                'label16': ttk.Label(self.swpCondNotebookTabs['dropped'], text='and/or'),

                'instruction': ttk.Label(self.swpCondNotebookTabs['dropped'], justify='left',
                                         text='Instruction:\nQre = -Qre1-Qre2-...-Qre5 when (QreX is {_1} and QreY is {_2}) or QreZ not {_3}'),

                'itemStm1': ttk.Label(self.swpCondNotebookTabs['dropped'], text='='),
                'itemStm2': ttk.Label(self.swpCondNotebookTabs['dropped'], text='='),
                'itemStm3': ttk.Label(self.swpCondNotebookTabs['dropped'], text='='),
                'itemStm4': ttk.Label(self.swpCondNotebookTabs['dropped'], text='='),
                'itemStm5': ttk.Label(self.swpCondNotebookTabs['dropped'], text='='),

                'qreCond1': ttk.Entry(self.swpCondNotebookTabs['dropped']),
                'qreCond2': ttk.Entry(self.swpCondNotebookTabs['dropped']),
                'qreCond3': ttk.Entry(self.swpCondNotebookTabs['dropped']),
                'qreCond4': ttk.Entry(self.swpCondNotebookTabs['dropped']),
                'qreCond5': ttk.Entry(self.swpCondNotebookTabs['dropped']),

                'exclusive': ttk.Entry(self.swpCondNotebookTabs['dropped']),

                'itemOpen1': ttk.Combobox(self.swpCondNotebookTabs['dropped'], values=['', '('], state='readonly',
                                          width=5),
                'itemQre1': ttk.Entry(self.swpCondNotebookTabs['dropped']),
                'itemVal1': ttk.Entry(self.swpCondNotebookTabs['dropped']),
                'itemClose1': ttk.Combobox(self.swpCondNotebookTabs['dropped'], values=['', ')'], state='readonly',
                                           width=5),
                'itemConj1': ttk.Combobox(self.swpCondNotebookTabs['dropped'], values=['', 'and', 'or'],
                                          state='readonly', width=5),

                'itemOpen2': ttk.Combobox(self.swpCondNotebookTabs['dropped'], values=['', '('], state='readonly',
                                          width=5),
                'itemQre2': ttk.Entry(self.swpCondNotebookTabs['dropped']),
                'itemVal2': ttk.Entry(self.swpCondNotebookTabs['dropped']),
                'itemClose2': ttk.Combobox(self.swpCondNotebookTabs['dropped'], values=['', ')'], state='readonly',
                                           width=5),
                'itemConj2': ttk.Combobox(self.swpCondNotebookTabs['dropped'], values=['', 'and', 'or'],
                                          state='readonly', width=5),

                'itemOpen3': ttk.Combobox(self.swpCondNotebookTabs['dropped'], values=['', '('], state='readonly',
                                          width=5),
                'itemQre3': ttk.Entry(self.swpCondNotebookTabs['dropped']),
                'itemVal3': ttk.Entry(self.swpCondNotebookTabs['dropped']),
                'itemClose3': ttk.Combobox(self.swpCondNotebookTabs['dropped'], values=['', ')'], state='readonly',
                                           width=5),
                'itemConj3': ttk.Combobox(self.swpCondNotebookTabs['dropped'], values=['', 'and', 'or'],
                                          state='readonly', width=5),

                'itemOpen4': ttk.Combobox(self.swpCondNotebookTabs['dropped'], values=['', '('], state='readonly',
                                          width=5),
                'itemQre4': ttk.Entry(self.swpCondNotebookTabs['dropped']),
                'itemVal4': ttk.Entry(self.swpCondNotebookTabs['dropped']),
                'itemClose4': ttk.Combobox(self.swpCondNotebookTabs['dropped'], values=['', ')'], state='readonly',
                                           width=5),
                'itemConj4': ttk.Combobox(self.swpCondNotebookTabs['dropped'], values=['', 'and', 'or'],
                                          state='readonly', width=5),

                'itemOpen5': ttk.Combobox(self.swpCondNotebookTabs['dropped'], values=['', '('], state='readonly',
                                          width=5),
                'itemQre5': ttk.Entry(self.swpCondNotebookTabs['dropped']),
                'itemVal5': ttk.Entry(self.swpCondNotebookTabs['dropped']),
                'itemClose5': ttk.Combobox(self.swpCondNotebookTabs['dropped'], values=['', ')'], state='readonly',
                                           width=5),
                'itemConj5': ttk.Label(self.swpCondNotebookTabs['dropped'], width=5),
            },
            'getminnumber': {
                'label1': ttk.Label(self.swpCondNotebookTabs['getminnumber'], text='Numeric question 1'),
                'label2': ttk.Label(self.swpCondNotebookTabs['getminnumber'], text='Numeric question 2'),
                'label3': ttk.Label(self.swpCondNotebookTabs['getminnumber'], text='Numeric question 3'),
                'label4': ttk.Label(self.swpCondNotebookTabs['getminnumber'], text='Numeric question 4'),
                'label5': ttk.Label(self.swpCondNotebookTabs['getminnumber'], text='Numeric question 5'),
                'label6': ttk.Label(self.swpCondNotebookTabs['getminnumber'], text='Numeric question 6'),
                'label7': ttk.Label(self.swpCondNotebookTabs['getminnumber'], text='Numeric question 7'),
                'label8': ttk.Label(self.swpCondNotebookTabs['getminnumber'], text='Numeric question 8'),
                'label9': ttk.Label(self.swpCondNotebookTabs['getminnumber'], text='Numeric question 9'),
                'label10': ttk.Label(self.swpCondNotebookTabs['getminnumber'], text='Numeric question 10'),
                'qreCond1': ttk.Entry(self.swpCondNotebookTabs['getminnumber']),
                'qreCond2': ttk.Entry(self.swpCondNotebookTabs['getminnumber']),
                'qreCond3': ttk.Entry(self.swpCondNotebookTabs['getminnumber']),
                'qreCond4': ttk.Entry(self.swpCondNotebookTabs['getminnumber']),
                'qreCond5': ttk.Entry(self.swpCondNotebookTabs['getminnumber']),
                'qreCond6': ttk.Entry(self.swpCondNotebookTabs['getminnumber']),
                'qreCond7': ttk.Entry(self.swpCondNotebookTabs['getminnumber']),
                'qreCond8': ttk.Entry(self.swpCondNotebookTabs['getminnumber']),
                'qreCond9': ttk.Entry(self.swpCondNotebookTabs['getminnumber']),
                'qreCond10': ttk.Entry(self.swpCondNotebookTabs['getminnumber']),
                'instruction': ttk.Label(self.swpCondNotebookTabs['getminnumber'], justify='left',
                text='Instruction:\n\nGet the minimum value of the questions(numeric type)')
            },
            'getmaxnumber': {
                'label1': ttk.Label(self.swpCondNotebookTabs['getmaxnumber'], text='Numeric question 1'),
                'label2': ttk.Label(self.swpCondNotebookTabs['getmaxnumber'], text='Numeric question 2'),
                'label3': ttk.Label(self.swpCondNotebookTabs['getmaxnumber'], text='Numeric question 3'),
                'label4': ttk.Label(self.swpCondNotebookTabs['getmaxnumber'], text='Numeric question 4'),
                'label5': ttk.Label(self.swpCondNotebookTabs['getmaxnumber'], text='Numeric question 5'),
                'label6': ttk.Label(self.swpCondNotebookTabs['getmaxnumber'], text='Numeric question 6'),
                'label7': ttk.Label(self.swpCondNotebookTabs['getmaxnumber'], text='Numeric question 7'),
                'label8': ttk.Label(self.swpCondNotebookTabs['getmaxnumber'], text='Numeric question 8'),
                'label9': ttk.Label(self.swpCondNotebookTabs['getmaxnumber'], text='Numeric question 9'),
                'label10': ttk.Label(self.swpCondNotebookTabs['getmaxnumber'], text='Numeric question 10'),
                'qreCond1': ttk.Entry(self.swpCondNotebookTabs['getmaxnumber']),
                'qreCond2': ttk.Entry(self.swpCondNotebookTabs['getmaxnumber']),
                'qreCond3': ttk.Entry(self.swpCondNotebookTabs['getmaxnumber']),
                'qreCond4': ttk.Entry(self.swpCondNotebookTabs['getmaxnumber']),
                'qreCond5': ttk.Entry(self.swpCondNotebookTabs['getmaxnumber']),
                'qreCond6': ttk.Entry(self.swpCondNotebookTabs['getmaxnumber']),
                'qreCond7': ttk.Entry(self.swpCondNotebookTabs['getmaxnumber']),
                'qreCond8': ttk.Entry(self.swpCondNotebookTabs['getmaxnumber']),
                'qreCond9': ttk.Entry(self.swpCondNotebookTabs['getmaxnumber']),
                'qreCond10': ttk.Entry(self.swpCondNotebookTabs['getmaxnumber']),
                'instruction': ttk.Label(self.swpCondNotebookTabs['getmaxnumber'], justify='left',
                text='Instruction:\n\nGet the maximum value of the questions(numeric type)')
            },
            'getvaluesbyiters': {
                'label1': ttk.Label(self.swpCondNotebookTabs['getvaluesbyiters'], text='Iterations'),
                'label2': ttk.Label(self.swpCondNotebookTabs['getvaluesbyiters'], text='Categorical grid'),
                'qreCond1': ttk.Entry(self.swpCondNotebookTabs['getvaluesbyiters']),
                'qreCond2': ttk.Entry(self.swpCondNotebookTabs['getvaluesbyiters']),
                'instruction': ttk.Label(self.swpCondNotebookTabs['getvaluesbyiters'], justify='left',
                text='''Instruction:
                - Iterations: can be input categories or categorical question
                - Grid categorical: only input Categorical grid with format Grid[..]._Qre
                - Return values are categorical
                - EX:
                  + Iterations = {_1,_2} and Categorical grid = _Q1[..]._Q1_Codes
                  + Return union(_Q1[{_1}]._Q1_Codes, _Q1[{_2}]._Q1_Codes).unique()''')
            },
            'getsum': {
                'label1': ttk.Label(self.swpCondNotebookTabs['getsum'], text='Categorical question 1: '),
                'label2': ttk.Label(self.swpCondNotebookTabs['getsum'], text='Categorical question 2: '),
                'label3': ttk.Label(self.swpCondNotebookTabs['getsum'], text='Categorical question 3: '),
                'label4': ttk.Label(self.swpCondNotebookTabs['getsum'], text='Categorical question 4: '),
                'label5': ttk.Label(self.swpCondNotebookTabs['getsum'], text='Categorical question 5: '),
                'label6': ttk.Label(self.swpCondNotebookTabs['getsum'], text='Categorical question 6: '),
                'label7': ttk.Label(self.swpCondNotebookTabs['getsum'], text='Categorical question 7: '),
                'label8': ttk.Label(self.swpCondNotebookTabs['getsum'], text='Categorical question 8: '),
                'label9': ttk.Label(self.swpCondNotebookTabs['getsum'], text='Categorical question 9: '),
                'label10': ttk.Label(self.swpCondNotebookTabs['getsum'], text='Categorical question 10: '),

                'qreCond1': ttk.Entry(self.swpCondNotebookTabs['getsum'], name='!getSumQreCond1'),
                'qreCond2': ttk.Entry(self.swpCondNotebookTabs['getsum'], name='!getSumQreCond2'),
                'qreCond3': ttk.Entry(self.swpCondNotebookTabs['getsum'], name='!getSumQreCond3'),
                'qreCond4': ttk.Entry(self.swpCondNotebookTabs['getsum'], name='!getSumQreCond4'),
                'qreCond5': ttk.Entry(self.swpCondNotebookTabs['getsum'], name='!getSumQreCond5'),
                'qreCond6': ttk.Entry(self.swpCondNotebookTabs['getsum'], name='!getSumQreCond6'),
                'qreCond7': ttk.Entry(self.swpCondNotebookTabs['getsum'], name='!getSumQreCond7'),
                'qreCond8': ttk.Entry(self.swpCondNotebookTabs['getsum'], name='!getSumQreCond8'),
                'qreCond9': ttk.Entry(self.swpCondNotebookTabs['getsum'], name='!getSumQreCond9'),
                'qreCond10': ttk.Entry(self.swpCondNotebookTabs['getsum'], name='!getSumQreCond10'),

                'instruction': ttk.Label(self.swpCondNotebookTabs['getsum'], justify='left',
                                         text='Instruction:\nQre = sum(Qre1+Qre2+...+Qre10)'
                                              '\nQre = sum(Qre1+{_num123}+...+Qre10)'),
            },
        }

        self.swpCondNotebookTabItems['askedall'].pack(padx=5, pady=5)

        self.swpCondNotebookTabItems['yearsubtract']['label'].pack(side='left', anchor='nw', padx=5, pady=5)
        self.swpCondNotebookTabItems['yearsubtract']['qreCond'].pack(fill='x', padx=5, pady=5)

        self.swpCondNotebookTabItems['catfromnum']['label'].grid(row=0, column=0, padx=5, pady=5)
        self.swpCondNotebookTabItems['catfromnum']['qreCond'].grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.swpCondNotebookTabItems['catfromnum']['instruction'].grid(row=1, column=0, rowspan=10, padx=5, pady=5)
        for i in np.arange(len(self.swpCondNotebookTabItems['catfromnum'])-3):
            self.swpCondNotebookTabItems['catfromnum']['itemCond{}'.format(i+1)].grid(row=i+2, column=1, padx=5, pady=5, sticky='ew')
        self.swpCondNotebookTabs['catfromnum'].grid_columnconfigure(1, weight=1)

        self.swpCondNotebookTabItems['catfromcats']['label'].grid(row=0, column=0, padx=5, pady=5)
        self.swpCondNotebookTabItems['catfromcats']['qreCond'].grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.swpCondNotebookTabItems['catfromcats']['instruction'].grid(row=1, column=0, rowspan=10, padx=5, pady=5)
        for i in np.arange(len(self.swpCondNotebookTabItems['catfromcats']) - 3):
            self.swpCondNotebookTabItems['catfromcats']['itemCond{}'.format(i + 1)].grid(row=i + 2, column=1, padx=5, pady=5, sticky='ew')
        self.swpCondNotebookTabs['catfromcats'].grid_columnconfigure(1, weight=1)

        self.swpCondNotebookTabItems['lsm2'].pack(padx=5, pady=5)

        for i in np.arange(1, 11):
            self.swpCondNotebookTabItems['sum']['label{}'.format(i)].grid(row=i, column=0, padx=5, pady=5)
            self.swpCondNotebookTabItems['sum']['qreCond{}'.format(i)].grid(row=i, column=1, padx=5, pady=5, sticky='ew')
        self.swpCondNotebookTabItems['sum']['instruction'].grid(row=11, column=0, columnspan=2, padx=5, pady=5, sticky='w')
        self.swpCondNotebookTabs['sum'].grid_columnconfigure(1, weight=1)

        self.swpCondNotebookTabItems['allin']['label1'].grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.swpCondNotebookTabItems['allin']['qreCond'].grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.swpCondNotebookTabItems['allin']['label2'].grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.swpCondNotebookTabItems['allin']['exclusive'].grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.swpCondNotebookTabs['allin'].grid_columnconfigure(1, weight=1)

        self.swpCondNotebookTabItems['containsany']['label'].pack(side='left', anchor='nw', padx=5, pady=5)
        self.swpCondNotebookTabItems['containsany']['qreCond'].pack(fill='x', padx=5, pady=5)

        self.swpCondNotebookTabItems['notequal']['label'].pack(side='left', anchor='nw', padx=5, pady=5)
        self.swpCondNotebookTabItems['notequal']['qreCond'].pack(fill='x', padx=5, pady=5)

        self.swpCondNotebookTabItems['equal']['label'].pack(side='left', anchor='nw', padx=5, pady=5)
        self.swpCondNotebookTabItems['equal']['qreCond'].pack(fill='x', padx=5, pady=5)

        for i in np.arange(6):
            self.swpCondNotebookTabItems['when']['label{}'.format(i+1)].grid(row=0, column=i, padx=5, pady=5)
        for i in np.arange(10):
            self.swpCondNotebookTabItems['when']['itemOpen{}'.format(i+1)].grid(row=i+1, column=0, padx=5, pady=5)
            self.swpCondNotebookTabItems['when']['qreCond{}'.format(i+1)].grid(row=i+1, column=1, padx=5, pady=5, sticky='ew')
            self.swpCondNotebookTabItems['when']['itemStm{}'.format(i+1)].grid(row=i+1, column=2, padx=5, pady=5)
            self.swpCondNotebookTabItems['when']['itemVal{}'.format(i+1)].grid(row=i+1, column=3, padx=5, pady=5, sticky='ew')
            self.swpCondNotebookTabItems['when']['itemClose{}'.format(i+1)].grid(row=i+1, column=4, padx=5, pady=5)
            self.swpCondNotebookTabItems['when']['itemConj{}'.format(i+1)].grid(row=i+1, column=5, padx=5, pady=5)
        self.swpCondNotebookTabItems['when']['instruction'].grid(row=11, column=0, columnspan=2, padx=5, pady=5, sticky='w')
        self.swpCondNotebookTabs['when'].grid_columnconfigure(1, weight=3)
        self.swpCondNotebookTabs['when'].grid_columnconfigure(3, weight=1)

        self.swpCondNotebookTabItems['iterfilby']['label'].pack(side='left', anchor='nw', padx=5, pady=5)
        self.swpCondNotebookTabItems['iterfilby']['qreCond'].pack(fill='x', padx=5, pady=5)
        self.swpCondNotebookTabItems['iterfilby']['instruction'].pack(anchor='nw', padx=5, pady=5)

        for i in np.arange(6):
            self.swpCondNotebookTabItems['logic']['label{}'.format(i+1)].grid(row=0, column=i, padx=5, pady=5)
        for i in np.arange(11):
            self.swpCondNotebookTabItems['logic']['itemOpen{}'.format(i)].grid(row=i+1, column=0, padx=5, pady=5)
            self.swpCondNotebookTabItems['logic']['qreCond{}'.format(i)].grid(row=i+1, column=1, padx=5, pady=5, sticky='ew')
            self.swpCondNotebookTabItems['logic']['itemStm{}'.format(i)].grid(row=i+1, column=2, padx=5, pady=5)
            self.swpCondNotebookTabItems['logic']['itemVal{}'.format(i)].grid(row=i+1, column=3, padx=5, pady=5, sticky='ew')
            self.swpCondNotebookTabItems['logic']['itemClose{}'.format(i)].grid(row=i+1, column=4, padx=5, pady=5)
            self.swpCondNotebookTabItems['logic']['itemConj{}'.format(i)].grid(row=i+1, column=5, padx=5, pady=5)
        self.swpCondNotebookTabItems['logic']['instruction'].grid(row=12, column=0, columnspan=2, padx=5, pady=5, sticky='w')
        self.swpCondNotebookTabs['logic'].grid_columnconfigure(1, weight=3)
        self.swpCondNotebookTabs['logic'].grid_columnconfigure(3, weight=1)

        for i in np.arange(1, 11):
            self.swpCondNotebookTabItems['merge']['label{}'.format(i)].grid(row=i, column=0, padx=5, pady=5)
            self.swpCondNotebookTabItems['merge']['qreCond{}'.format(i)].grid(row=i, column=1, padx=5, pady=5, sticky='ew')
        self.swpCondNotebookTabItems['merge']['label11'].grid(row=11, column=0, padx=5, pady=5)
        self.swpCondNotebookTabItems['merge']['exclusive'].grid(row=11, column=1, padx=5, pady=5, sticky='ew')
        self.swpCondNotebookTabItems['merge']['instruction'].grid(row=12, column=0, columnspan=2, padx=5, pady=5, sticky='w')
        self.swpCondNotebookTabs['merge'].grid_columnconfigure(1, weight=1)

        self.swpCondNotebookTabItems['assign']['label00'].grid(row=0, column=0, padx=5, pady=5, columnspan=6)
        for i in np.arange(5):
            self.swpCondNotebookTabItems['assign']['label0{}'.format(i+1)].grid(row=i+1, column=0, padx=5, pady=5)
            self.swpCondNotebookTabItems['assign']['qreCond{}'.format(i+1)].grid(row=i+1, column=1, padx=5, pady=5, sticky='ew', columnspan=5)
        self.swpCondNotebookTabItems['assign']['label06'].grid(row=6, column=0, padx=5, pady=5)
        self.swpCondNotebookTabItems['assign']['exclusive'].grid(row=6, column=1, padx=5, pady=5, sticky='ew', columnspan=5)
        self.swpCondNotebookTabItems['assign']['label10'].grid(row=7, column=0, padx=5, pady=5, columnspan=6)
        for i in np.arange(6):
            self.swpCondNotebookTabItems['assign']['label1{}'.format(i+1)].grid(row=8, column=i, padx=5, pady=5)
        for i in np.arange(1, 6):
            self.swpCondNotebookTabItems['assign']['itemOpen{}'.format(i)].grid(row=i+8, column=0, padx=5, pady=5)
            self.swpCondNotebookTabItems['assign']['itemQre{}'.format(i)].grid(row=i+8, column=1, padx=5, pady=5, sticky='ew')
            self.swpCondNotebookTabItems['assign']['itemStm{}'.format(i)].grid(row=i+8, column=2, padx=5, pady=5)
            self.swpCondNotebookTabItems['assign']['itemVal{}'.format(i)].grid(row=i+8, column=3, padx=5, pady=5, sticky='ew')
            self.swpCondNotebookTabItems['assign']['itemClose{}'.format(i)].grid(row=i+8, column=4, padx=5, pady=5)
            self.swpCondNotebookTabItems['assign']['itemConj{}'.format(i)].grid(row=i+8, column=5, padx=5, pady=5)
        self.swpCondNotebookTabItems['assign']['instruction'].grid(row=14, column=0, padx=5, pady=5, columnspan=6, sticky='w')
        self.swpCondNotebookTabs['assign'].grid_columnconfigure(1, weight=3)
        self.swpCondNotebookTabs['assign'].grid_columnconfigure(3, weight=1)

        self.swpCondNotebookTabItems['dropped']['label00'].grid(row=0, column=0, padx=5, pady=5, columnspan=6)
        for i in np.arange(5):
            self.swpCondNotebookTabItems['dropped']['label0{}'.format(i + 1)].grid(row=i + 1, column=0, padx=5, pady=5)
            self.swpCondNotebookTabItems['dropped']['qreCond{}'.format(i + 1)].grid(row=i + 1, column=1, padx=5, pady=5, sticky='ew', columnspan=5)
        self.swpCondNotebookTabItems['dropped']['label06'].grid(row=6, column=0, padx=5, pady=5)
        self.swpCondNotebookTabItems['dropped']['exclusive'].grid(row=6, column=1, padx=5, pady=5, sticky='ew', columnspan=5)
        self.swpCondNotebookTabItems['dropped']['label10'].grid(row=7, column=0, padx=5, pady=5, columnspan=6)
        for i in np.arange(6):
            self.swpCondNotebookTabItems['dropped']['label1{}'.format(i + 1)].grid(row=8, column=i, padx=5, pady=5)
        for i in np.arange(1, 6):
            self.swpCondNotebookTabItems['dropped']['itemOpen{}'.format(i)].grid(row=i + 8, column=0, padx=5, pady=5)
            self.swpCondNotebookTabItems['dropped']['itemQre{}'.format(i)].grid(row=i + 8, column=1, padx=5, pady=5, sticky='ew')
            self.swpCondNotebookTabItems['dropped']['itemStm{}'.format(i)].grid(row=i + 8, column=2, padx=5, pady=5)
            self.swpCondNotebookTabItems['dropped']['itemVal{}'.format(i)].grid(row=i + 8, column=3, padx=5, pady=5, sticky='ew')
            self.swpCondNotebookTabItems['dropped']['itemClose{}'.format(i)].grid(row=i + 8, column=4, padx=5, pady=5)
            self.swpCondNotebookTabItems['dropped']['itemConj{}'.format(i)].grid(row=i + 8, column=5, padx=5, pady=5)
        self.swpCondNotebookTabItems['dropped']['instruction'].grid(row=14, column=0, padx=5, pady=5, columnspan=6, sticky='w')
        self.swpCondNotebookTabs['dropped'].grid_columnconfigure(1, weight=3)
        self.swpCondNotebookTabs['dropped'].grid_columnconfigure(3, weight=1)

        self.swpCondNotebookTabItems['count']['label1'].grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.swpCondNotebookTabItems['count']['qreCond'].grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.swpCondNotebookTabItems['count']['label2'].grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.swpCondNotebookTabItems['count']['exclusive'].grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.swpCondNotebookTabs['count'].grid_columnconfigure(1, weight=1)

        self.swpCondNotebookTabItems['difference']['label0'].grid(row=0, column=0, padx=5, pady=5, columnspan=2)
        self.swpCondNotebookTabItems['difference']['label1'].grid(row=1, column=0, padx=5, pady=5)
        self.swpCondNotebookTabItems['difference']['qreCond1'].grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.swpCondNotebookTabItems['difference']['label00'].grid(row=2, column=0, padx=5, pady=5, columnspan=2)
        for i in np.arange(2, 11):
            self.swpCondNotebookTabItems['difference']['label{}'.format(i)].grid(row=i+1, column=0, padx=5, pady=5)
            self.swpCondNotebookTabItems['difference']['qreCond{}'.format(i)].grid(row=i+1, column=1, padx=5, pady=5, sticky='ew')
        self.swpCondNotebookTabItems['difference']['instruction'].grid(row=13, column=0, columnspan=2, padx=5, pady=5, sticky='w')
        self.swpCondNotebookTabs['difference'].grid_columnconfigure(1, weight=1)

        self.swpCondNotebookTabItems['intersection']['label0'].grid(row=0, column=0, padx=5, pady=5, columnspan=2)
        self.swpCondNotebookTabItems['intersection']['label1'].grid(row=1, column=0, padx=5, pady=5)
        self.swpCondNotebookTabItems['intersection']['qreCond1'].grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.swpCondNotebookTabItems['intersection']['label00'].grid(row=2, column=0, padx=5, pady=5, columnspan=2)
        for i in np.arange(2, 11):
            self.swpCondNotebookTabItems['intersection']['label{}'.format(i)].grid(row=i + 1, column=0, padx=5, pady=5)
            self.swpCondNotebookTabItems['intersection']['qreCond{}'.format(i)].grid(row=i + 1, column=1, padx=5, pady=5, sticky='ew')
        self.swpCondNotebookTabItems['intersection']['instruction'].grid(row=13, column=0, columnspan=2, padx=5, pady=5, sticky='w')
        self.swpCondNotebookTabs['intersection'].grid_columnconfigure(1, weight=1)

        self.swpCondNotebookTabItems['getiters']['label1'].grid(row=0, column=0, padx=5, pady=5)
        self.swpCondNotebookTabItems['getiters']['label2'].grid(row=0, column=1, padx=5, pady=5)
        self.swpCondNotebookTabItems['getiters']['qreCond'].grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        self.swpCondNotebookTabItems['getiters']['itemVal'].grid(row=1, column=1, padx=5, pady=5)
        self.swpCondNotebookTabItems['getiters']['instruction'].grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='w')
        self.swpCondNotebookTabs['getiters'].grid_columnconfigure(0, weight=1)

        self.swpCondNotebookTabItems['numcompared']['label1'].grid(row=0, column=0, padx=5, pady=5)
        self.swpCondNotebookTabItems['numcompared']['label2'].grid(row=1, column=0, padx=5, pady=5)
        self.swpCondNotebookTabItems['numcompared']['qreCond1'].grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.swpCondNotebookTabItems['numcompared']['qreCond2'].grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.swpCondNotebookTabItems['numcompared']['instruction'].grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='w')
        self.swpCondNotebookTabs['numcompared'].grid_columnconfigure(1, weight=1)

        for i in np.arange(0, 10):
            self.swpCondNotebookTabItems['getminnumber']['label{}'.format(i + 1)].grid(row=i, column=0, padx=5, pady=5)
            self.swpCondNotebookTabItems['getminnumber']['qreCond{}'.format(i + 1)].grid(row=i, column=1, padx=5, pady=5, sticky='ew')
        self.swpCondNotebookTabItems['getminnumber']['instruction'].grid(row=11, column=0, columnspan=2, padx=5, pady=5, sticky='w')
        self.swpCondNotebookTabs['getminnumber'].grid_columnconfigure(1, weight=1)

        for i in np.arange(0, 10):
            self.swpCondNotebookTabItems['getmaxnumber']['label{}'.format(i + 1)].grid(row=i, column=0, padx=5, pady=5)
            self.swpCondNotebookTabItems['getmaxnumber']['qreCond{}'.format(i + 1)].grid(row=i, column=1, padx=5, pady=5, sticky='ew')
        self.swpCondNotebookTabItems['getmaxnumber']['instruction'].grid(row=11, column=0, columnspan=2, padx=5, pady=5, sticky='w')
        self.swpCondNotebookTabs['getmaxnumber'].grid_columnconfigure(1, weight=1)

        self.swpCondNotebookTabItems['getvaluesbyiters']['label1'].grid(row=0, column=0, padx=5, pady=5)
        self.swpCondNotebookTabItems['getvaluesbyiters']['label2'].grid(row=1, column=0, padx=5, pady=5)
        self.swpCondNotebookTabItems['getvaluesbyiters']['qreCond1'].grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.swpCondNotebookTabItems['getvaluesbyiters']['qreCond2'].grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.swpCondNotebookTabItems['getvaluesbyiters']['instruction'].grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='w')
        self.swpCondNotebookTabs['getvaluesbyiters'].grid_columnconfigure(1, weight=1)

        for i in np.arange(1, 11):
            self.swpCondNotebookTabItems['getsum']['label{}'.format(i)].grid(row=i, column=0, padx=5, pady=5)
            self.swpCondNotebookTabItems['getsum']['qreCond{}'.format(i)].grid(row=i, column=1, padx=5, pady=5, sticky='ew')
        self.swpCondNotebookTabItems['getsum']['instruction'].grid(row=11, column=0, columnspan=2, padx=5, pady=5, sticky='w')
        self.swpCondNotebookTabs['getsum'].grid_columnconfigure(1, weight=1)

        # FRAME MATERIAL - FRAME NAVIGATION - BUTTONS
        self.swpButtons = {
            'clear': ttk.Button(self.swpMaterialFrames['navigation'], image=self.swpIcons['btnclear'], command=self.clearConfirm),
            'submit': ttk.Button(self.swpMaterialFrames['navigation'], image=self.swpIcons['btnsubmit'], command=self.addChecklistNode),
            'update': ttk.Button(self.swpMaterialFrames['navigation'], image=self.swpIcons['btnupdate'], command=self.updateChecklistNode),
        }

        self.swpButtons['clear'].pack(fill='x', side='left', padx=1, expand=True)
        self.swpButtons['update'].pack(fill='x', side='left', padx=1, expand=True)
        self.swpButtons['submit'].pack(fill='x', side='right', padx=1, expand=True)

        self.disableChildsOfFrame(self.swpMaterialFrames['navigation'], 'disabled')

        # PANEL MASTER - FRAME CHECKLIST - BUTTONS
        fr_checklistBtns = ttk.Frame(self.swpFrames['checklist'])
        fr_checklistBtns.pack(side='top', fill='x')
        fr_checklistBtnsUpDown = ttk.Frame(fr_checklistBtns)
        fr_checklistBtnsDelete = ttk.Frame(fr_checklistBtns)
        fr_checklistBtnsUpDown.pack(side='left', fill='x', expand=True)
        fr_checklistBtnsDelete.pack(side='right', fill='x')
        self.swpBtnChecklistMoveUp = ttk.Button(fr_checklistBtnsUpDown, image=self.swpIcons['btnmoveup'], command=self.moveUpChecklistNodes)
        self.swpBtnChecklistMoveDown = ttk.Button(fr_checklistBtnsUpDown, image=self.swpIcons['btnmovedown'], command=self.moveDownChecklistNodes)
        self.swpBtnChecklistDuplicate = ttk.Button(fr_checklistBtnsUpDown, image=self.swpIcons['btnduplicate'], command=self.duplicateChecklistNode)

        self.swpBtnChecklistMoveUp.grid(row=0, column=0, padx=1)
        self.swpBtnChecklistMoveDown.grid(row=0, column=1, padx=1)
        self.swpBtnChecklistDuplicate.grid(row=0, column=2, padx=1)

        self.swpBtnChecklistDelete = ttk.Button(fr_checklistBtnsDelete, image=self.swpIcons['btndelete'], command=self.deleteChecklistNodes)
        self.swpBtnChecklistDelete.pack(side='right', padx=10)

        # PANEL MASTER - FRAME CHECKLIST - TREEVIEW & SCROLLBAR
        fr_ChecklistTrv = ttk.Frame(self.swpFrames['checklist'])
        fr_ChecklistTrv.pack(side='bottom', fill='both', expand=True)

        fr_ChecklistTrv.propagate(False)
        self.swpTrvChecklist = ttk.Treeview(fr_ChecklistTrv, style='mystyle.Treeview',
        columns=['method', 'isNewVar', 'qreCond', 'cond', 'exclusive'])
        self.swpTrvChecklist.column('#0', width=300)
        self.swpTrvChecklist.column('#1', width=130)
        self.swpTrvChecklist.heading('#0', text='Items')
        self.swpTrvChecklist.heading('method', text='Method')
        self.swpTrvChecklist.heading('isNewVar', text='is new variable')

        fr_y = tk.Frame(fr_ChecklistTrv)
        fr_y.pack(side='right', fill='y')
        tk.Label(fr_y, borderwidth=1, relief='raised', font='Arial 8').pack(side='bottom', fill='x')
        swpYScrollChecklist = tk.Scrollbar(fr_y, orient="vertical", command=self.swpTrvChecklist.yview)
        swpYScrollChecklist.pack(fill='y', expand=True)
        fr_x = tk.Frame(fr_ChecklistTrv)
        fr_x.pack(side='bottom', fill='x')
        swpXScrollChecklist = tk.Scrollbar(fr_x, orient="horizontal", command=self.swpTrvChecklist.xview)
        swpXScrollChecklist.pack(fill='x', expand=True)

        self.swpTrvChecklist.configure(yscrollcommand=swpYScrollChecklist.set, xscrollcommand=swpXScrollChecklist.set)
        self.swpTrvChecklist.pack(fill='both', expand=True)

        # PANEL STATUS - FRAME STATUS - LABEL
        self.swpFrames['status'].pack(side='left', fill='x', expand=True)
        self.swpStatusLbl = ttk.Label(self.swpFrames['status'], text='Ready.')
        self.swpStatusLbl.pack(side='left')
        self.swpStatusCountLbl = ttk.Label(self.swpFrames['status'], text='')
        self.swpStatusCountLbl.pack(side='right')

        # METADATA PATH & NAME
        self.swpMetadataFile = {'path': '', 'name': ''}
        self.swpChecklistSavePath = None

        # ERROR LOG WINDOW
        self.swpWinErrLog = tk.Toplevel(self.swpWin, name='!toplevel')
        self.swpWinErrLog.iconphoto(False, tk.PhotoImage(file='Icon\Sweeper.png'))
        self.swpWinErrLog.title('Errors Log')
        self.swpWinErrLog.lower()
        self.swpWinErrLog.minsize(720, 480)
        self.swpWinErrLog.state('withdrawn')
        frameErrLog = ttk.Frame(self.swpWinErrLog)
        frameErrLog.pack(fill='both', expand=True)
        fr_leftErrLog = ttk.Frame(frameErrLog)
        fr_leftErrLog.pack(side='left', fill='both', expand=True)
        xScrollbarErrLog = ttk.Scrollbar(fr_leftErrLog, orient='horizontal')
        xScrollbarErrLog.pack(side='bottom', fill='x')
        fr_rightErrLog = ttk.Frame(frameErrLog)
        fr_rightErrLog.pack(side='right', fill='y')
        yScrollbarErrLog = ttk.Scrollbar(fr_rightErrLog, orient='vertical')
        yScrollbarErrLog.pack(side='top', fill='y', expand=True)
        tk.Label(fr_rightErrLog, borderwidth=1, relief='raised').pack(side='bottom', fill='x')
        self.swpTextErrLog = tk.Text(fr_leftErrLog, wrap='none', xscrollcommand=xScrollbarErrLog.set, yscrollcommand=yScrollbarErrLog.set)
        self.swpTextErrLog.pack(side='left', fill='both', expand=True)
        xScrollbarErrLog.config(command=self.swpTextErrLog.xview)
        yScrollbarErrLog.config(command=self.swpTextErrLog.yview)

        self.bindHotkeys()


    def bindHotkeys(self):
        self.swpWin.bind_all('<Control-o>', self.openMetadataFile)
        self.swpWin.bind_all('<Alt-q>', self.quitConfirmation)
        self.swpWin.bind_all('<Alt-c>', self.clearConfirm)
        self.swpWin.bind_all('<Control-Tab>', self.addChecklistNode)
        self.swpWin.bind_all('<Control-s>', self.saveChecklistToCsv)
        self.swpWin.bind_all('<Control-l>', self.loadChecklistFromCsv)
        self.swpWin.bind_all('<F5>', self.runChecklist)

        self.swpTrvData.bind('<Double-1>', self.inputTrvDataSelToCheckQre)
        self.swpTrvData.bind('<Button-3>', self.trvDataMenuCallback)
        self.swpTrvData.bind('<space>', self.inputTrvDataSelToCondQre)

        self.swpCheckQreMethodCbb.bind('<<ComboboxSelected>>', self.swpCheckQreMethodSelected)
        self.swpCheckQreEntry.bind('<Button-1>', self.inputTrvDataSelToEntry)

        for key in self.swpCondNotebookTabItems.keys():
            if isinstance(self.swpCondNotebookTabItems[key], dict):
                for k in self.swpCondNotebookTabItems[key].keys():
                    if ('qreCond' in k or 'itemQre' in k) \
                            and self.swpCondNotebookTabItems[key][k].winfo_class() == 'TEntry':
                        self.swpCondNotebookTabItems[key][k].bind('<Button-1>', self.inputTrvDataSelToEntry)

        self.swpTrvChecklist.bind('<Delete>', self.deleteChecklistNodes)
        self.swpTrvChecklist.bind('<Double-1>', self.trvChecklistDbl1)

        self.swpWin.protocol("WM_DELETE_WINDOW", self.quitConfirmation)
        self.swpWinErrLog.protocol("WM_DELETE_WINDOW", self.onErrLogClose)


    def unbindHotkeys(self):
        self.swpWin.unbind_all('<Control-o>')
        self.swpWin.unbind_all('<Alt-q>')
        self.swpWin.unbind_all('<Alt-c>')
        self.swpWin.unbind_all('<Control-Tab>')
        self.swpWin.unbind_all('<Control-s>')
        self.swpWin.unbind_all('<Control-l>')
        self.swpWin.unbind_all('<F5>')

        self.swpTrvData.unbind('<Double-1>')
        self.swpTrvData.unbind('<Button-3>')
        self.swpTrvData.unbind('<space>')

        self.swpCheckQreMethodCbb.unbind('<<ComboboxSelected>>')
        self.swpCheckQreEntry.unbind('<Button-1>')

        for key in self.swpCondNotebookTabItems.keys():
            if isinstance(self.swpCondNotebookTabItems[key], dict):
                for k in self.swpCondNotebookTabItems[key].keys():
                    if ('qreCond' in k or 'itemQre' in k) \
                            and self.swpCondNotebookTabItems[key][k].winfo_class() == 'TEntry':
                        self.swpCondNotebookTabItems[key][k].unbind('<Button-1>')

        self.swpTrvChecklist.unbind('<Delete>')
        self.swpTrvChecklist.unbind('<Double-1>')


    def openMetadataFile(self, event=None):
        try:
            filePath = filedialog.askopenfile(filetypes=[('Metadata file', "*.mdd")])

            strSqlWhere = None
            if filePath:
                strSqlWhere = simpledialog.askstring('SELECT * FROM VDATA', 'WHERE\t\t\t\t\t', parent=self.swpWin,
                                                     initialvalue='_LoaiPhieu = {_1} OR _LoaiPhieu = {_5}')
            if filePath and strSqlWhere:
                self.statusLabelUpdate(True, 'Opening metadata')
                lstPath = os.path.split(filePath.name)
                self.swpMetadataFile['path'] = lstPath[0]
                self.swpMetadataFile['name'] = lstPath[1].replace('.mdd', '')

                if self.funcOpenMetadataFile(self.swpMetadataFile['path'], self.swpMetadataFile['name'], strSqlWhere,
                                             self.swpTrvData, self.swpTrvChecklist):

                    self.strTitle = 'Sweeper {} - {}'.format(self.ver, self.swpMetadataFile['name'])
                    self.swpWin.title(self.strTitle)

                    self.enableFrameQre()

                    self.disableChildsOfFrame(self.swpMaterialFrames['navigation'], 'enable')

                    self.isDataActive = True

                    strCountSample = re.sub('[\'{}]', '', str(self.dto.countSample()))
                    self.swpStatusCountLbl.configure(text=strCountSample)

                    messagebox.showinfo('Opening', 'Open {} successful.'.format(self.swpMetadataFile['name']))

                else:
                    messagebox.showerror('Opening error', 'No record loaded.')

        except Exception:
            messagebox.showerror('Error', traceback.format_exc())

        finally:
            self.statusLabelUpdate()


    def funcOpenMetadataFile(self, strFilePath, strFileName, strSqlWhere, trvData, trvChecklist):
        # update to Log
        self.prgConn.insertLog(self.loginName, strFilePath, strFileName)

        if len(trvData.get_children()) > 0:
            trvData.delete(trvData.get_children())
        trvData.insert('', 0, strFileName, text=strFileName, image=self.swpIcons['database'])
        trvData.item(strFileName, open=True)

        if trvChecklist.get_children():
            for node in trvChecklist.get_children():
                trvChecklist.delete(node)

        fileName, sqlWhere = f'{strFilePath}/{strFileName}', strSqlWhere
        self.dto = ditto(fileName, sqlWhere, [])

        if self.dto.df.empty:
            return False
        else:
            self.dmToMetadataTree(trvData, strFileName, self.dto.dm)
            return True


    def dmToMetadataTree(self, tree, parent, mydict):
        strRe = re.compile(r'^.+\._[0-9]+$')
        for key in mydict:
            if isinstance(mydict[key], dict):

                if mydict[key]['isNewVar']:
                    logo = self.swpIcons['new' + mydict[key]['mddType']]
                else:
                    logo = self.swpIcons[mydict[key]['mddType']]

                if '[..]' in parent:
                    nodeText = '{}.{}'.format(parent, key)
                else:
                    nodeText = key

                if strRe.match(nodeText):
                    tree.insert('.'.join(nodeText.split('.')[0:-1]), 'end', nodeText, text=nodeText, image=logo)
                else:
                    tree.insert(parent, 'end', nodeText, text=nodeText, image=logo)

                tree.item(nodeText, tags=(bool(mydict[key]['isNewVar'])))

                if list(mydict[key]['mddVars'])[0] != key:
                    self.dmToMetadataTree(tree, nodeText, mydict[key])

            elif isinstance(mydict[key], set):
                if not key in ['iter'] and mydict['mddType'] != 'grid':
                    for val in mydict[key]:
                        if mydict['isNewVar']:
                            logoChild = self.swpIcons['newchildnode']
                        else:
                            logoChild = self.swpIcons['childnode']

                        if strRe.match(val):
                            tree.insert('.'.join(val.split('.')[0:-1]), 'end', val, text=val, image=self.swpIcons['text'])
                        else:
                            tree.insert(parent, 'end', val, text=val, image=logoChild)

                        tree.item(val, tags=(bool(mydict['isNewVar'])))

                        if parent.count('[..]') > 1:
                            strParent = parent.replace('..', 'xxx')
                            lstParent = strParent.split('.')
                            lstChild = val.split('.')
                            lstChildNew = list()
                            for i in np.arange(parent.count('[..]')):
                                lstParentTemp = strParent.split('.')
                                lstParentTemp[i] = lstChild[i]
                                strChildNew = '.'.join(lstParentTemp).replace('xxx', '..')
                                lstChildNew.append(strChildNew)

                            lstChildNew = list(dict.fromkeys(lstChildNew))

                            for i in np.arange(len(lstChildNew)):
                                try:
                                    strLvl = '{}_Lvl{}[..]'.format(parent, i)
                                    try:
                                        tree.insert(parent, '0', strLvl, text='_Level{}'.format(i), image=logoChild)
                                    except Exception:
                                        pass
                                    tree.insert(strLvl, '0', lstChildNew[i], text=lstChildNew[i], image=logoChild)
                                    tree.item(lstChildNew[i], tags=(bool(mydict['isNewVar'])))
                                except Exception:
                                    pass



    @staticmethod
    def disableChildsOfFrame(frame, stt):
        for child in frame.winfo_children():
            if child.winfo_class() != 'TLabel':
                child.configure(state=stt)


    def enableFrameQre(self):
        self.swpCheckQreEntry.config(state='normal')
        self.swpCheckQreCbx.config(state='normal', text='Checking method:')
        self.swpCheckQreCbxVal.set(False)
        self.swpCheckQreMethodCbb.config(values=self.hrc.method, state='readonly')
        self.swpMenu['File'].entryconfig('Save checklist', state='normal')
        self.swpMenu['File'].entryconfig('Load checklist', state='normal')
        self.swpMenu['Run'].entryconfig('Run checklist', state='normal')


    def swpCheckQreCbxChange(self):
        for tab in self.swpCondNotebookTabs:
            self.swpCondNotebook.tab(self.swpCondNotebookTabs[tab], state='hidden')
        self.swpCheckQreMethodCbbVal.set('')
        if self.swpCheckQreCbxVal.get():
            self.swpCheckQreLbl.config(text='New question:')
            self.swpCheckQreCbx.config(text='Creating method:')
            self.swpCheckQreMethodCbb.config(values=self.dto.method, state='readonly')
        else:
            self.swpCheckQreLbl.config(text='Question:')
            self.swpCheckQreCbx.config(text='Checking method:')
            self.swpCheckQreMethodCbb.config(values=self.hrc.method, state='readonly')


    def swpCheckQreMethodSelected(self, event=None):
        self.inputTabLogicQreCond0()
        for tab in self.swpCondNotebookTabs:
            if self.swpCheckQreMethodCbbVal.get() == tab:
                self.swpCondNotebook.select(self.swpCondNotebookTabs[tab])
                self.swpCondNotebook.tab(self.swpCondNotebookTabs[tab], state='normal')
            else:
                self.swpCondNotebook.tab(self.swpCondNotebookTabs[tab], state='hidden')
                if isinstance(self.swpCondNotebookTabItems[tab], dict):
                    for key in self.swpCondNotebookTabItems[tab].keys():
                        if self.swpCondNotebookTabItems[tab][key].winfo_class() == 'TEntry':
                            self.swpCondNotebookTabItems[tab][key].delete(0, 'end')


    def inputTabLogicQreCond0(self):
        if self.swpCheckQreMethodCbb.get() == 'logic':
            self.swpCondNotebookTabItems['logic']['qreCond0'].config(text=self.swpCheckQreEntry.get())


    def inputTrvDataSelToEntry(self, event):
        if self.swpTrvData.selection() and self.valCheckTrvDataSelNode():
            textVal = event.widget
            textVal.delete(0, 'end')
            textVal.insert(0, '|'.join(self.swpTrvData.selection()))
            self.inputTabLogicQreCond0()
            self.swpTrvData.selection_remove(self.swpTrvData.selection())


    def inputTrvDataSelToCheckQre(self, event=None):
        if self.valCheckTrvDataSelNode():
            trv = self.swpTrvData
            self.swpCheckQreEntry.delete(0, 'end')
            self.swpCheckQreEntry.insert(0, '|'.join(trv.selection()))
            self.inputTabLogicQreCond0()
            trv.selection_remove(trv.selection())


    def trvDataMenuCallback(self, event):
        trv = event.widget
        iid = trv.identify_row(event.y)
        if iid:
            trv.selection_set(iid)
            try:
                self.swpTrvDataMenu.tk_popup(event.x_root, event.y_root)
            finally:
                self.swpTrvDataMenu.grab_release()


    def trvDataMenuSelected(self, event=None):
        self.inputTrvDataSelToCheckQre()
        if self.swpTrvDataMenuSel.get() in self.rtm.method:
            self.swpCheckQreCbxVal.set(True)
        else:
            self.swpCheckQreCbxVal.set(False)
        self.swpCheckQreCbxChange()
        self.swpCheckQreMethodCbbVal.set(self.swpTrvDataMenuSel.get())
        self.swpCheckQreMethodSelected()
        self.swpTrvDataMenuSel.set('')


    def inputTrvDataSelToCondQre(self, event):
        if self.valCheckTrvDataSelNode():
            trv = event.widget
            cbbSelVal = self.swpCheckQreMethodCbbVal.get()
            if cbbSelVal:
                for key in self.swpCondNotebookTabItems[cbbSelVal].keys():
                    tabItem = self.swpCondNotebookTabItems[cbbSelVal][key]
                    if ('qreCond' in key or 'itemQre' in key) \
                            and tabItem.winfo_class() == 'TEntry':
                        if len(tabItem.get()) == 0:
                            tabItem.delete(0, 'end')
                            tabItem.insert(0, '|'.join(trv.selection()))
                        else:
                            continue
                        trv.selection_remove(trv.selection())


    def valCheckTrvDataSelNode(self):
        sel = '|'.join(self.swpTrvData.selection())
        if sel == self.swpMetadataFile['name'] or sel[-4:len(sel)] == '[..]':
            # messagebox.showerror('Wrong selection', 'Cannot select {}.'.format(sel))
            return False
        return True


    def backToArceus(self, event=None):
        self.unbindHotkeys()
        self.swpMenuBar.destroy()
        self.swpPanels['master'].destroy()
        self.swpPanels['status'].destroy()
        self.swpWinErrLog.destroy()
        self.classArceus(self.swpWin, self.prgConn, self.ver, self.loginName, self.loginPass)


    def quitConfirmation(self, event=None):
        isQuit = False
        if self.isChecklistSave:
            if messagebox.askyesno('Confirmation', 'Are you sure you want to quit?'):
                isQuit = True
        else:
            if self.swpTrvChecklist.get_children():
                if messagebox.askyesno('Save confirmation', 'Want to save your checklist changes?'):
                    self.saveChecklistToCsv()
            isQuit = True
        if isQuit:
            self.swpWin.iconify()
            isValidAcc, isValidStt = self.prgConn.tryLogin(self.loginName, self.loginPass, isLogin=False)
            if isValidAcc and isValidStt:
                self.swpWin.quit()
            else:
                self.swpWin.deiconify()
                messagebox.showerror('Quit error', 'Please check your internet connection.')


    def clearConfirm(self, event=None):
        if self.isDataActive:
            cbbSelVal = self.swpCheckQreMethodCbbVal.get()
            if cbbSelVal:
                confirmAns = messagebox.askyesnocancel('Confirmation', 'Are you sure you want to clear values?\n\n'
                                                        'Yes = clear all input values.\n'
                                                        'No = clear "' + cbbSelVal + '" values.\n'
                                                        'Cancel = do nothing.')
                if confirmAns is True:
                    self.framesQuestionClear()
                    self.framesConditionClear(cbbSelVal)
                elif confirmAns is False:
                    self.framesConditionClear(cbbSelVal)
                elif confirmAns is None:
                    pass


    def framesQuestionClear(self):
        self.swpCheckQreEntry.delete(0, 'end')
        self.swpCondNotebook.tab(self.swpCondNotebookTabs[self.swpCheckQreMethodCbbVal.get()], state='hidden')
        self.swpCheckQreCbxVal.set(False)
        self.swpCheckQreMethodCbbVal.set('')
        self.swpCheckQreMethodCbb.config(values=self.hrc.method)


    def framesConditionClear(self, cbbSelVal):
        if isinstance(self.swpCondNotebookTabItems[cbbSelVal], dict):
            for key in self.swpCondNotebookTabItems[cbbSelVal].keys():
                tabItem = self.swpCondNotebookTabItems[cbbSelVal][key]
                if tabItem.winfo_class() == 'TEntry':
                    tabItem.delete(0, 'end')
                if tabItem.winfo_class() == 'TCombobox':
                    tabItem.set('')


    def addChecklistNode(self, event=None):
        if self.isDataActive:
            self.addUpdateChecklistNode(True)


    def updateChecklistNode(self, event=None):
        if self.isDataActive:
            if len(self.swpTrvChecklist.selection()) == 0:
                messagebox.showwarning('Warning', 'Please select update item.')
            elif len(self.swpTrvChecklist.selection()) > 1:
                messagebox.showwarning('Warning', 'Cannot update multiple items.')
            else:
                if messagebox.askyesno('Confirmation', 'Update this item?'):
                    self.addUpdateChecklistNode(False)


    def duplicateChecklistNode(self, event=None):
        self.funcDuplicateChecklistNode(self.swpTrvChecklist)
        self.updateChecklistSaveStatus(self.swpWin)


    @staticmethod
    def funcDuplicateChecklistNode(trv):
        try:
            if trv.selection():
                lstSelection = list(trv.selection())
                lstSelection.reverse()
                insIndex = trv.index(trv.selection()[-1]) + 1
                for selNodeID in lstSelection:
                    selNode = trv.item(selNodeID)
                    trv.insert('', insIndex, id=uuid4().hex, text=selNode['text'], values=selNode['values'], image=selNode['image'])
                    trv.update()
            else:
                messagebox.showerror('Error', 'Please chose the item first.')

        except Exception:
            messagebox.showerror('Error', traceback.format_exc())


    def addUpdateChecklistNode(self, isAddin):
        try:
            if self.swpCheckQreEntry.get() and self.swpCheckQreMethodCbb.get():
                trv = self.swpTrvChecklist
                trvId = uuid4().hex
                trvText = self.swpCheckQreEntry.get()
                trvVals = [self.swpCheckQreMethodCbb.get(), self.swpCheckQreCbxVal.get()]

                strQreCond = str()
                strItemCond = str()
                strExclusive = str()

                # Push conditional
                selTab = self.swpCondNotebookTabItems[self.swpCheckQreMethodCbb.get()]
                if isinstance(selTab, dict):
                    for key in selTab:
                        selTabItem = selTab[key]

                        if selTabItem.winfo_class() in ['TEntry', 'TCombobox'] and selTabItem.get():
                            if 'qreCond' in key:
                                strQreCond += '{}#{}@'.format(str(selTabItem), selTabItem.get())
                            elif 'item' in key:
                                strItemCond += '{}#{}@'.format(str(selTabItem), selTabItem.get())
                            elif 'exclusive' in key:
                                strExclusive += '{}#{}@'.format(str(selTabItem), selTabItem.get())

                strQreCond = strQreCond[0:-1]
                strItemCond = strItemCond[0:-1]
                strExclusive = strExclusive[0:-1]

                trvVals.extend([strQreCond, strItemCond, strExclusive])

                # Validate Question before insert
                isQreInputErr, strQreInputErr = self.valCheckQuestionInput()
                if isAddin and not isQreInputErr:
                    self.selectInvalidQuestion(self.swpCheckQreEntry)
                    messagebox.showerror('Input error', strQreInputErr)
                    return isQreInputErr

                # Validate Inputting Conditional before insert
                isCondInputErr, strCondInputErr = self.valCheckConditionInput_New()
                if not isCondInputErr:
                    messagebox.showerror('Input error', strCondInputErr)
                    return isCondInputErr
                # if not self.valCheckConditionInput(): OLD
                #     return False

                # Insert Item
                if self.swpCheckQreMethodCbb.get() in self.rtm.method:
                    strTag = 'rtm'
                    logo = self.swpIcons['checklistCreate']
                else:
                    strTag = 'hrc'
                    logo = self.swpIcons['checklistCheck']

                if trv.selection():
                    selIndex = trv.index(trv.selection())
                    trv.insert('', selIndex, trvId, text=trvText, values=tuple(trvVals), tag=(strTag, ),
                               image=logo)

                    if not isAddin:
                        trv.delete(trv.selection())

                else:
                    trv.insert('', 'end', trvId, text=trvText, values=tuple(trvVals), tag=(strTag, ), image=logo)
                    trv.update()
                    trv.yview_moveto(1)

                # Update trvData with new var
                if trvVals[1]:
                    self.updateRtmWithChecklist()
                    self.updateTrvDataWithRtm()

                # Clear after push
                self.framesQuestionClear()
                self.framesConditionClear(trvVals[0])

                # Update checklist save status
                self.updateChecklistSaveStatus(self.swpWin)

                return True

            else:
                messagebox.showerror('Error', 'Please input question name and check method.')
                return False
        except Exception:
            messagebox.showerror('Error', traceback.format_exc())


    def updateChecklistSaveStatus(self, win):
        if self.isChecklistSave:
            self.isChecklistSave = False
            self.strTitle = self.strTitle + '*'
            win.title(self.strTitle)


    @staticmethod
    def selectInvalidQuestion(checkQre):
        checkQre.focus_set()
        checkQre.select_range(0, 'end')


    def valCheckQuestionInput(self):
        qreName = self.swpCheckQreEntry.get()
        strRe = re.compile('^\w+(\[({\w+}|\.\.)]\.\w+(\.\w+)*)*$')
        strReSec = re.compile('(((^(_SEC_AGEGROUP\.))|(^\w+(([Bb](LOCK|lock))|([Ss](EC|ec)))\w+\.))\w+)|(\w+\._\w+)')
        if not strRe.match(qreName) and not strReSec.match(qreName):
            return False, f'{qreName} is invalid.'

        isExistItem, isNewVar = self.isItemExistinTreeView(self.swpTrvData, qreName)
        methodName = self.swpCheckQreMethodCbb.get()
        if methodName in ['assign', 'dropped']:
            if isExistItem and not isNewVar:
                return False, '{} is {} exist.'.format(qreName, '' if isExistItem else 'not')
        elif methodName in ['sum']:
            strRe = re.compile('^num+[0-9]+$')
            if not isExistItem and not strRe.match(qreName):
                return False, f'{qreName} is not exist or not format text(num) + long(XYZ).'
        elif methodName in ['iterfilby']:
            strRe = re.compile('.+\w+\[\.\.]\.\w+')
            if not isExistItem or not strRe.match(qreName):
                return False, f'{qreName} is not exist or not contain any [..].'
        else:
            if (self.swpCheckQreCbxVal.get() and isExistItem) \
                    or (not self.swpCheckQreCbxVal.get() and not isExistItem):
                return False, '{} is{}exist.'.format(qreName, ' ' if isExistItem else ' not ')
        return True, None


    def valCheckConditionIsNull(self, tabItem, pre_tabItem=None):
        if tabItem.winfo_class() in ['TLabel']:
            return True
        if pre_tabItem is not None:
            if not pre_tabItem.get() and tabItem.get():
                self.selectInvalidCondition(tabItem)
                return False
        else:
            if not tabItem.get():
                return False
        return True


    def valCheckConditionCompareTabItems(self, tabItem, strItemName, dictCheckTab, key):
        if strItemName in key:
            pre_tabItem = dictCheckTab['{}{}'.format(strItemName, int(key.replace(strItemName, '')) - 1)]
            return self.valCheckConditionIsNull(tabItem, pre_tabItem)
        else:
            return True


    def valCheckConditionQreExist(self, tabItem):
        if tabItem.winfo_class() in ['TLabel']:
            return True
        isExistItem = True
        if tabItem.get():
            isExistItem, isNewVar = self.isItemExistinTreeView(self.swpTrvData, tabItem.get())
            if not isExistItem:
                self.selectInvalidCondition(tabItem)
        return isExistItem


    def valCheckMatchRegex(self, strRe, tabItem):
        if tabItem.winfo_class() in ['TLabel']:
            return True
        if not strRe.match(tabItem.get()) and tabItem.get():
            self.selectInvalidCondition(tabItem)
            return False
        return True


    def valCheckQreCondWithItemVal(self, tabItem, dictCheckTab, key, strMethod):
        tabItemCheck = None

        if strMethod in ['assign', 'dropped']:
            if 'itemQre' in key:
                tabItemCheck = dictCheckTab[key.replace('itemQre', 'itemVal')]
            elif 'itemVal' in key:
                tabItemCheck = dictCheckTab[key.replace('itemVal', 'itemQre')]
        else:
            if 'qreCond' in key:
                tabItemCheck = dictCheckTab[key.replace('qreCond', 'itemVal')]
            elif 'itemVal' in key:
                tabItemCheck = dictCheckTab[key.replace('itemVal', 'qreCond')]

        if tabItem.get() and not tabItemCheck.get():
            self.selectInvalidCondition(tabItemCheck)
            return False
        return True


    def valCheckConditionParenthesesConjunction(self, dictCheckTab, strMethod='when'):
        lstCondition = list()

        if strMethod == 'logic':
            if dictCheckTab['itemOpen0'].get():
                lstCondition.append(dictCheckTab['itemOpen0'].get())
            lstCondition.append('0')
            lstCondition.append('==')
            lstCondition.append('0')
            if dictCheckTab['itemClose0'].get():
                lstCondition.append(dictCheckTab['itemClose0'].get())
            if dictCheckTab['itemConj0'].get():
                lstCondition.append(dictCheckTab['itemConj0'].get())

        maxNum = 6 if strMethod in ['assign', 'dropped'] else 11
        for i in np.arange(1, maxNum):
            if dictCheckTab[f'itemOpen{i}'].get():
                lstCondition.append(dictCheckTab[f'itemOpen{i}'].get())
            if (not strMethod in ['assign', 'dropped'] and dictCheckTab[f'qreCond{i}'].get()) or (strMethod in ['assign', 'dropped'] and dictCheckTab[f'itemQre{i}'].get()):
                lstCondition.append(str(i))
                lstCondition.append('==')
            if dictCheckTab[f'itemVal{i}'].get():
                lstCondition.append(str(i))
            if dictCheckTab[f'itemClose{i}'].get():
                lstCondition.append(dictCheckTab[f'itemClose{i}'].get())
            if i < maxNum - 1:
                if dictCheckTab[f'itemConj{i}'].get():
                    lstCondition.append(dictCheckTab[f'itemConj{i}'].get())

        strCondition = ' '.join(lstCondition)
        try:
            if '()' in strCondition.replace(' ', ''):
                return False, 'Invalid parentheses "( )".'
            if (not strCondition.count('or') and not strCondition.count('and')) and strMethod == 'logic':
                return False, 'Missing conjunction.'
            _ = eval(strCondition)
            if not self.valCheckParentheses(strCondition):
                return False, 'Invalid parentheses.'
            return True, 'None'
        except SyntaxError as err:
            return False, err.msg
        except Exception:
            return False, traceback.format_exc()


    @staticmethod
    def selectInvalidCondition(tabItem):
        tabItem.focus_set()
        tabItem.select_range(0, 'end')


    @staticmethod
    def valCheckParentheses(strCheck):
        # lstTemp1 = strCheck.split('|')
        # lstTemp2 = list()
        # for i in np.arange(len(lstTemp1)):
        #     if not '@' in lstTemp1[i]:
        #         lstTemp2.extend([lstTemp1[i]])
        # strCheck = ''.join(lstTemp2)
        open_list = ["[", "{", "("]
        close_list = ["]", "}", ")"]
        stack = []
        for i in strCheck:
            if i in open_list:
                stack.append(i)
            elif i in close_list:
                pos = close_list.index(i)
                if len(stack) > 0 and open_list[pos] == stack[len(stack) - 1]:
                    stack.pop()
                else:
                    return False
        if len(stack) == 0:
            return True
        else:
            return False


    def valCheckConditionInput_New(self):
        # ---------------------------------------------------------------------------------------
        strMethod = self.swpCheckQreMethodCbbVal.get()
        dictCheckTab = self.swpCondNotebookTabItems[strMethod]

        for key in dictCheckTab.keys():
            tabItem = dictCheckTab[key]

            if strMethod in ['askedall', 'lsm2']:
                pass

            elif strMethod in ['yearsubtract']:
                if not self.valCheckConditionIsNull(tabItem):
                    return False, 'Please input year of birth question.'
                if not self.valCheckConditionQreExist(tabItem):
                    return False, f'{tabItem.get()} is not exist.'

            elif strMethod in ['catfromnum', 'catfromcats']:
                if 'qreCond' in key:
                    if not self.valCheckConditionIsNull(tabItem):
                        return False, f'Please input {strMethod} condition question.'
                    if not self.valCheckConditionQreExist(tabItem):
                        return False, f'{tabItem.get()} is not exist.'
                else:
                    if strMethod in ['catfromnum']:
                        strRe = re.compile('^({_\w+}=)+(([0-9]+.*[0-9]* to|over|under)+ [0-9]+.*[0-9]*$)')
                    elif strMethod in ['catfromcats']:
                        strRe = re.compile('^({_\w+}=)+{(_\w+)(,_\w+)*}$')
                    else:
                        strRe = re.compile('Error!!!!!!!!!!!!!!!!!!!!!!!')

                    if not self.valCheckMatchRegex(strRe, tabItem):
                        return False, f'{tabItem.get()} is invalid condition.'

                    if 'itemCond1' == key:
                        if not self.valCheckConditionIsNull(tabItem):
                            return False, 'Please input condition.'
                    else:
                        if not self.valCheckConditionCompareTabItems(tabItem, 'itemCond', dictCheckTab, key):
                            return False, 'Please input condition question in order.'

            elif strMethod in ['sum']:
                if 'qreCond' in key:
                    if not self.valCheckConditionQreExist(tabItem):
                        return False, f'{tabItem.get()} is not exist.'

                    if 'qreCond1' == key:
                        if not self.valCheckConditionIsNull(tabItem):
                            return False, f'Please input {strMethod} condition question.'
                    else:
                        if not self.valCheckConditionCompareTabItems(tabItem, 'qreCond', dictCheckTab, key):
                            return False, 'Please input condition question in order.'

            elif strMethod in ['allin', 'count']:
                if 'qreCond' in key:
                    if not self.valCheckConditionIsNull(tabItem):
                        return False, f'Please input {strMethod} condition question.'
                    if not self.valCheckConditionQreExist(tabItem):
                        return False, f'{tabItem.get()} is not exist.'
                else:
                    strRe = re.compile('^({|~{)_(?!.*Null|null|NULL)\w+(,_\w+)*}$')
                    if not self.valCheckMatchRegex(strRe, tabItem):
                        return False, f'{tabItem.get()} is invalid input.'

            elif strMethod in ['containsany']:
                if 'qreCond' in key:
                    if not self.valCheckConditionIsNull(tabItem):
                        return False, f'Please input {strMethod} condition question.'

                    strRe = re.compile('^({|~{)_(?!.*Null|null|NULL)\w+(,_\w+)*}$')
                    if not self.valCheckConditionQreExist(tabItem) and not self.valCheckMatchRegex(strRe, tabItem):
                        return False, f'{tabItem.get()} is not exist or not categories.'

            elif strMethod in ['notequal', 'equal']:
                if 'qreCond' in key:
                    if not self.valCheckConditionIsNull(tabItem):
                        return False, f'Please input {strMethod} condition question.'
                    if not self.valCheckConditionQreExist(tabItem):
                        return False, f'{tabItem.get()} is not exist.'

            elif strMethod in ['when']:
                if 'qreCond' in key:
                    if not self.valCheckConditionQreExist(tabItem):
                        return False, f'{tabItem.get()} is not exist.'

                    if 'qreCond1' == key:
                        if not self.valCheckConditionIsNull(tabItem):
                            return False, f'Please input {strMethod} condition question.'
                    else:
                        if not self.valCheckConditionCompareTabItems(tabItem, 'qreCond', dictCheckTab, key):
                            return False, 'Please input condition question in order.'

                    if not self.valCheckQreCondWithItemVal(tabItem, dictCheckTab, key, strMethod):
                        return False, 'Please input condition value.'

                if 'itemVal' in key:
                    strRe = re.compile('^(~|)(Null$|{_num(>|<|=|>=|<=)[0-9]+}$|{(_(?!.*(Null|null|NULL|num|Num|NUM))\w+)(,_(?!.*(Null|null|NULL|num|Num|NUM))\w+)*}$)')
                    if not self.valCheckMatchRegex(strRe, tabItem):
                        return False, f'{tabItem.get()} is invalid input.'
                    if not self.valCheckQreCondWithItemVal(tabItem, dictCheckTab, key, strMethod):
                        return False, 'Please input condition question.'

                if 'instruction' == key:
                    return self.valCheckConditionParenthesesConjunction(dictCheckTab)

            elif strMethod in ['iterfilby']:
                if 'qreCond' in key:
                    if not self.valCheckConditionQreExist(tabItem):
                        return False, f'{tabItem.get()} is not exist. new'

                    lstReCheckQre = re.findall('\w+\[..].', self.swpCheckQreEntry.get())
                    lstReCondQre = re.findall('\w+\[..].', tabItem.get())
                    strReCheckQre = ''.join(lstReCheckQre)
                    strReCondQre = ''.join(lstReCondQre)

                    if len(lstReCheckQre) <= len(lstReCondQre):
                        self.selectInvalidCondition(tabItem)
                        return False, f"{self.swpCheckQreEntry.get()}'s level must > {tabItem.get()}'s lvl."

                    # Allow 2 Level Grid filterby 1 level Cats
                    # if len(lstReCheckQre) >= 2 and (not strReCondQre in strReCheckQre or len(lstReCheckQre) - 1 != len(lstReCondQre)):
                    #     self.selectInvalidCondition(tabItem)
                    #     return False, f'{self.swpCheckQreEntry.get()} must have same parent with {tabItem.get()}.'

            elif strMethod in ['logic']:
                if 'qreCond' in key:
                    if not self.valCheckConditionQreExist(tabItem):
                        return False, f'{tabItem.get()} is not exist.'

                    if key != 'qreCond0':
                        if key == 'qreCond1':
                            if not self.valCheckConditionIsNull(tabItem):
                                return False, f'Please input {strMethod} condition question.'
                        else:
                            if not self.valCheckConditionCompareTabItems(tabItem, 'qreCond', dictCheckTab, key):
                                return False, 'Please input condition question in order.'

                        if not self.valCheckQreCondWithItemVal(tabItem, dictCheckTab, key, strMethod):
                            return False, 'Please input condition value.'

                if 'itemVal' in key:
                    strRe = re.compile('^(~|)(Null$|{_num(>|<|=|>=|<=)[0-9]+}$|{(_(?!.*(Null|null|NULL|num|Num|NUM))\w+)(,_(?!.*(Null|null|NULL|num|Num|NUM))\w+)*}$)')
                    if not self.valCheckMatchRegex(strRe, tabItem):
                        return False, f'{tabItem.get()} is invalid input.'
                    if key == 'itemVal0':
                        if not tabItem.get():
                            return False, 'Please input first condition value.'
                    else:
                        if not self.valCheckQreCondWithItemVal(tabItem, dictCheckTab, key, strMethod):
                            return False, 'Please input condition question.'

                if 'instruction' == key:
                    return self.valCheckConditionParenthesesConjunction(dictCheckTab, strMethod)

            elif strMethod in ['merge', 'difference', 'intersection']:
                strRe = re.compile('^{_(?!.*Null|null|NULL)\w+(,_\w+)*}$')
                if 'qreCond' in key:
                    if not self.valCheckConditionQreExist(tabItem) and not self.valCheckMatchRegex(strRe, tabItem):
                        return False, f'{tabItem.get()} is not exist or not categories.'

                    if 'qreCond1' == key:
                        if not self.valCheckConditionIsNull(tabItem):
                            return False, f'Please input {strMethod} condition question.'
                    else:
                        if not self.valCheckConditionCompareTabItems(tabItem, 'qreCond', dictCheckTab, key):
                            return False, 'Please input condition question in order.'

                if key == 'exclusive' and not self.valCheckMatchRegex(strRe, tabItem):
                    return False, 'Exclusive codes is not categories.'

            elif strMethod in ['assign', 'dropped']:
                strRe = re.compile('^{_(?!.*Null|null|NULL)\w+(,_\w+)*}$')
                if 'qreCond' in key:
                    if not self.valCheckConditionQreExist(tabItem) and not self.valCheckMatchRegex(strRe, tabItem):
                        return False, f'{tabItem.get()} is not exist or not categories.'

                    if 'qreCond1' == key:
                        if not self.valCheckConditionIsNull(tabItem):
                            return False, f'Please input {strMethod} condition question.'
                    else:
                        if not self.valCheckConditionCompareTabItems(tabItem, 'qreCond', dictCheckTab, key):
                            return False, 'Please input condition question in order.'

                if key == 'exclusive' and not self.valCheckMatchRegex(strRe, tabItem):
                    return False, 'Exclusive codes is not categories.'

                if 'itemQre' in key:
                    if not self.valCheckConditionQreExist(tabItem):
                        return False, f'{tabItem.get()} is not exist.'

                    if 'itemQre1' == key:
                        if not self.valCheckConditionIsNull(tabItem):
                            return False, f'Please input {strMethod} item question.'
                    else:
                        if not self.valCheckConditionCompareTabItems(tabItem, 'itemQre', dictCheckTab, key):
                            return False, 'Please input item question in order.'

                    if not self.valCheckQreCondWithItemVal(tabItem, dictCheckTab, key, strMethod):
                        return False, 'Please input item value.'

                if 'itemVal' in key:
                    strRe = re.compile('(^({|~{)+(_(?!.*(Null|null|NULL|NUM|Num|num))[A-Z|a-z0-9]+)(,_[A-Z|a-z0-9]+)*}$)')
                    if not self.valCheckMatchRegex(strRe, tabItem):
                        return False, f'{tabItem.get()} is invalid input.'
                    if not self.valCheckQreCondWithItemVal(tabItem, dictCheckTab, key, strMethod):
                        return False, 'Please input item question.'

                if 'itemConj5' == key:
                    return self.valCheckConditionParenthesesConjunction(dictCheckTab, strMethod)

            elif strMethod in ['getiters']:
                if 'qreCond' in key:
                    if not self.valCheckConditionQreExist(tabItem):
                        return False, f'{tabItem.get()} is not exist.'

                    if not self.valCheckConditionIsNull(tabItem):
                        return False, f'Please input {strMethod} grid question.'

                    if not tabItem.get().count('[..]'):
                        return False, f'{tabItem.get()} must have as least 1 "[..]".'

                if 'itemVal' in key:
                    if not self.valCheckConditionIsNull(tabItem):
                        return False, f'Please input {strMethod} value.'

                    strRe = re.compile('^(all|Null|~Null|min|max)$|'
                                       '^({|~{)+(?!.*(num|cats|cat|all|Null|min|max))(_\w+)(,_\w+)*(})$|'
                                       '^({|~{)_num(>|<|=|>=|<=)[0-9]+}$')
                    if not self.valCheckMatchRegex(strRe, tabItem):
                        return False, f'{tabItem.get()} is invalid input.'

            elif strMethod in ['numcompared']:
                if 'qreCond' in key:
                    if not self.valCheckConditionIsNull(tabItem):
                        return False, f'Please input {strMethod} condition question.'

                    strRe = re.compile('^{_num[0-9]+}$')
                    if not self.valCheckConditionQreExist(tabItem) and not self.valCheckMatchRegex(strRe, tabItem):
                        return False, f'{tabItem.get()} is not exist or not match format.'

            elif strMethod in ['getminnumber', 'getmaxnumber']:
                if 'qreCond' in key:
                    if not self.valCheckConditionQreExist(tabItem):
                        return False, f'{tabItem.get()} is not exist.'

                    if 'qreCond1' == key:
                        if not self.valCheckConditionIsNull(tabItem):
                            return False, f'Please input {strMethod} condition question.'
                    else:
                        if not self.valCheckConditionCompareTabItems(tabItem, 'qreCond', dictCheckTab, key):
                            return False, 'Please input condition question in order.'

            elif strMethod in ['getvaluesbyiters']:
                if 'qreCond' in key:
                    if not self.valCheckConditionIsNull(tabItem):
                        return False, f'Please input {strMethod} condition question.xxx'

                    if 'qreCond1' == key:
                        strRe = re.compile('^{+(_(?!.*(Null|null|NULL|num|Num|NUM))\w+)(,_\w+)*}$')
                    else:
                        strRe = re.compile('.+\w+\[..].+')

                    if not self.valCheckConditionQreExist(tabItem) and not self.valCheckMatchRegex(strRe, tabItem):
                        return False, f'{tabItem.get()} is not exist or not match format.xxx'

                    lstReCheckQre = re.findall('\w+\[..].', self.swpCheckQreEntry.get())
                    lstReCondQre = re.findall('\w+\[..].', tabItem.get())
                    strReCheckQre = ''.join(lstReCheckQre)
                    strReCondQre = ''.join(lstReCondQre)

                    if '[..]' in tabItem.get() and '[..]' in self.swpCheckQreEntry.get() and not strReCheckQre in strReCondQre:
                        self.selectInvalidCondition(tabItem)
                        return False, f'{self.swpCheckQreEntry.get()} must have same parent with {tabItem.get()}.xxx'

                    if 'qreCond1' == key and len(strReCheckQre) > 0 and lstReCheckQre != lstReCondQre:
                        self.selectInvalidCondition(tabItem)
                        return False, f'{self.swpCheckQreEntry.get()} must have same parent with {tabItem.get()}.xxx'

                    if 'qreCond2' == key:
                        if (len(lstReCondQre) > 1 and len(lstReCheckQre) == 0) or (len(lstReCondQre) <= len(lstReCheckQre)):
                            self.selectInvalidCondition(tabItem)
                            return False, f'{self.swpCheckQreEntry.get()} must have level less than {tabItem.get()}.xxx'

                        lstReCondQre1 = re.findall(r'\w+\[..].', dictCheckTab['qreCond1'].get())
                        if len(lstReCondQre) <= len(lstReCondQre1):
                            self.selectInvalidCondition(tabItem)
                            return False, f'{dictCheckTab["qreCond1"].get()} must have level less than {tabItem.get()}.xxx'

                        if len(lstReCondQre) - 1 != len(lstReCheckQre) or len(lstReCondQre) - 1 != len(lstReCondQre1):
                            self.selectInvalidCondition(tabItem)
                            return False, f'level of {tabItem.get()} = level {self.swpCheckQreEntry.get()} + 1 and level {dictCheckTab["qreCond1"].get()} + 1.'

            elif strMethod in ['getsum']:
                strRe = re.compile('^{_num[0-9]+}$')
                if 'qreCond' in key:
                    if not self.valCheckConditionQreExist(tabItem) and not self.valCheckMatchRegex(strRe, tabItem):
                        return False, f'{tabItem.get()} is not exist or not format.'

                    if 'qreCond1' == key:
                        if not self.valCheckConditionIsNull(tabItem):
                            return False, f'Please input {strMethod} condition question.'
                    else:
                        if not self.valCheckConditionCompareTabItems(tabItem, 'qreCond', dictCheckTab, key):
                            return False, 'Please input condition question in order.'


            else:
                return False, 'Not yet assign inputting validation.'

        return True, None
        #---------------------------------------------------------------------------------------


    # def valCheckConditionInput(self):
    #     strMethod = self.swpCheckQreMethodCbbVal.get()
    #     dictCheckTab = self.swpCondNotebookTabItems[strMethod]
    #     strRe = str()
    #     strInputEtr = str()
    #     strInputCbb = str()
    #     countCbb = int()
    #     strWhenLogicAssign = str()
    #     if isinstance(dictCheckTab, dict):
    #         for key in dictCheckTab.keys():
    #             tabItem = dictCheckTab[key]
    #             if ('qreCond' in key or 'itemQre' in key) and tabItem.winfo_class() in ['TEntry']:
    #                 if tabItem.get():
    #                     isExistItem, isNewVar = self.isItemExistinTreeView(self.swpTrvData, tabItem.get())
    #
    #                     if strMethod in ['containsany', 'merge', 'difference', 'intersection']:
    #                         strRe = re.compile(r'^({|~{)+(_(?!.*(Null|null|NULL))[A-Z|a-z0-9]+)(,_[A-Z|a-z0-9]+)*}$')
    #                         if not isExistItem and not strRe.match(tabItem.get()):
    #                             self.selectInvalidCondition(tabItem)
    #                             messagebox.showerror('Input error', '{} is not exist or not categories.'.format(tabItem.get()))
    #                             return False
    #                     elif strMethod in ['assign', 'dropped']:
    #                         if 'qreCond' in key:
    #                             strRe = re.compile(r'^({|~{)+(_(?!.*(Null|null|NULL))[A-Z|a-z0-9]+)(,_[A-Z|a-z0-9]+)*}$')
    #                             if not isExistItem and not strRe.match(tabItem.get()):
    #                                 self.selectInvalidCondition(tabItem)
    #                                 messagebox.showerror('Input error', '{} is not exist or not categories.'.format(tabItem.get()))
    #                                 return False
    #                         else:
    #                             if not isExistItem:
    #                                 self.selectInvalidCondition(tabItem)
    #                                 messagebox.showerror('Input error', '{} is not exist.'.format(tabItem.get()))
    #                                 return False
    #                     elif strMethod in ['numcompared']:
    #                         strRe = re.compile(r'^{_num[0-9]+}$')
    #                         if not isExistItem and not strRe.match(tabItem.get()):
    #                             self.selectInvalidCondition(tabItem)
    #                             messagebox.showerror('Input error', '{} is not exist or not match format.'.format(tabItem.get()))
    #                             return False
    #                     elif strMethod in ['getvaluesbyiters']:
    #                         if key == 'qreCond1':
    #                             strRe = re.compile(r'^{+(_(?!.*(Null|null|NULL|num|Num|NUM))[A-Z|a-z0-9]+)(,_[A-Z|a-z0-9]+)*}$')
    #                             if not isExistItem and not strRe.match(tabItem.get()):
    #                                 self.selectInvalidCondition(tabItem)
    #                                 messagebox.showerror('Input error', '{} is not exist or not match format.'.format(tabItem.get()))
    #                                 return False
    #                         else:
    #                             strRe = re.compile(r'.+[A-Z|a-z0-9_]+\[..].+')
    #                             if not isExistItem or not strRe.match(tabItem.get()):
    #                                 self.selectInvalidCondition(tabItem)
    #                                 messagebox.showerror('Input error', '{} is not exist and not match format.'.format(tabItem.get()))
    #                                 return False
    #                     else:
    #                         if not isExistItem:
    #                             self.selectInvalidCondition(tabItem)
    #                             messagebox.showerror('Input error', '{} is not exist.'.format(tabItem.get()))
    #                             return False
    #
    #                     if 'qreCond' in key:
    #                         lstRe1 = re.findall(r'[A-Z|a-z0-9_]+\[..].', self.swpCheckQreEntry.get())
    #                         lstRe2 = re.findall(r'[A-Z|a-z0-9_]+\[..].', tabItem.get())
    #                         strRe1 = ''.join(lstRe1)
    #                         strRe2 = ''.join(lstRe2)
    #
    #                         if strMethod in 'iterfilby':
    #                             if len(lstRe1) <= len(lstRe2):
    #                                 self.selectInvalidCondition(tabItem)
    #                                 messagebox.showerror('Input error', "{}'s level must > {}'s lvl."
    #                                                      .format(self.swpCheckQreEntry.get(), tabItem.get()))
    #                                 return False
    #                             if len(lstRe1) >= 2 and (not strRe2 in strRe1 or len(lstRe1) - 1 != len(lstRe2)):
    #                                 self.selectInvalidCondition(tabItem)
    #                                 messagebox.showerror('Input error', '{} must have same parent with {}.'
    #                                                      .format(self.swpCheckQreEntry.get(), tabItem.get()))
    #                                 return False
    #                         elif strMethod in 'getiters':
    #                             if len(lstRe2) == 0:
    #                                 self.selectInvalidCondition(tabItem)
    #                                 messagebox.showerror('Input error', '{} must have at least 1 "[..]".'
    #                                                      .format(tabItem.get()))
    #                                 return False
    #                         elif strMethod in ['merge', 'allin', 'containsany']: # update 6/10/2021
    #                             pass
    #                         elif strMethod in 'getvaluesbyiters':
    #                             if '[..]' in tabItem.get() and '[..]' in self.swpCheckQreEntry.get() and not strRe1 in strRe2:
    #                                 self.selectInvalidCondition(tabItem)
    #                                 messagebox.showerror('Input error', '{} must have same parent with {}.'
    #                                                      .format(self.swpCheckQreEntry.get(), tabItem.get()))
    #                                 return False
    #                             if key == 'qreCond1' and len(strRe1) > 0 and lstRe1 != lstRe2:
    #                                 self.selectInvalidCondition(tabItem)
    #                                 messagebox.showerror('Input error', '{} must have same parent with {}.'
    #                                                      .format(self.swpCheckQreEntry.get(), tabItem.get()))
    #                                 return False
    #                             if key == 'qreCond2':
    #                                 if (len(lstRe2) > 1 and len(lstRe1) == 0) or (len(lstRe2) <= len(lstRe1)):
    #                                     self.selectInvalidCondition(tabItem)
    #                                     messagebox.showerror('Input error', '{} must have level less than {}.'
    #                                                          .format(self.swpCheckQreEntry.get(), tabItem.get()))
    #                                     return False
    #
    #                                 lstRe3 = re.findall(r'[A-Z|a-z0-9_]+\[..].', dictCheckTab['qreCond1'].get())
    #                                 if len(lstRe2) <= len(lstRe3):
    #                                     self.selectInvalidCondition(tabItem)
    #                                     messagebox.showerror('Input error', '{} must have level less than {}.'
    #                                                          .format(dictCheckTab['qreCond1'].get(), tabItem.get()))
    #                                     return False
    #
    #                                 if len(lstRe2) - 1 != len(lstRe1) or len(lstRe2) - 1 != len(lstRe3):
    #                                     self.selectInvalidCondition(tabItem)
    #                                     messagebox.showerror('Input error', 'level of {} = level {} + 1 and level {} + 1.'
    #                                     .format(tabItem.get(), self.swpCheckQreEntry.get(), dictCheckTab['qreCond1'].get()))
    #                                     return False
    #                         else:
    #                             if '[..]' in tabItem.get() and '[..]' in self.swpCheckQreEntry.get() and not strRe2 in strRe1:
    #                                 self.selectInvalidCondition(tabItem)
    #                                 messagebox.showerror('Input error', '{} must have same parent with {}.'
    #                                                      .format(self.swpCheckQreEntry.get(), tabItem.get()))
    #                                 return False
    #             else:
    #                 if not tabItem.winfo_class() in ['TLabel']:
    #                     if tabItem.get():
    #                         if tabItem.winfo_class() in ['TEntry']:
    #                             if strMethod in 'catfromnum':
    #                                 strRe = re.compile(r'^({_[A-Z|a-z0-9]+}=)+(([0-9]+ to|over|under)+ [0-9]+$|[0-9]+$)')
    #                             elif strMethod in 'catfromcats':
    #                                 strRe = re.compile(r'^({_[A-Z|a-z0-9]+}=)+{(_[A-Z|a-z0-9]+)(,_[A-Z|a-z0-9]+)*}$')
    #                             elif strMethod in ['allin', 'merge', 'count']:
    #                                 strRe = re.compile(r'(^({|~{)+(_(?!.*(Null|null|NULL))[A-Z|a-z0-9]+)(,_[A-Z|a-z0-9]+)*}$)')
    #                             elif strMethod in ['when', 'logic']:
    #                                 strRe = re.compile(r'^(~|)+Null$|^({|~{)_num(>|<|=|>=|<=)[0-9]+}$|^({|~{)+(_(?!.*(Null|null|NULL|num|Num|NUM))[A-Z|a-z0-9]+)(,_[A-Z|a-z0-9]+)*}$')
    #                             elif strMethod in ['assign', 'dropped']:
    #                                 strRe = re.compile(r'(^({|~{)+(_(?!.*(Null|null|NULL))[A-Z|a-z0-9]+)(,_[A-Z|a-z0-9]+)*}$)')
    #
    #                         elif tabItem.winfo_class() in ['TCombobox']:
    #                             if strMethod in 'getiters':
    #                                 strRe = re.compile(r'^(all|Null|~Null|min|max)$|'
    #                                 r'^({|~{)+(?!.*(num|cats|cat))(_[A-Z|a-z0-9]+)(,_[A-Z|a-z0-9]+)*(})$|'
    #                                 r'^({|~{)_num(>|<|=|>=|<=)[0-9]+}$')
    #                             elif strMethod in ['when', 'logic', 'assign', 'dropped']:
    #                                 strRe = re.compile(r'\(|\)|and|or')
    #
    #                         if not strRe.match(tabItem.get()):
    #                             self.selectInvalidCondition(tabItem)
    #                             messagebox.showerror('Input error', '{} is invalid.'.format(tabItem.get()))
    #                             return False
    #
    #
    #             if strMethod in ['when', 'logic', 'assign', 'dropped']:
    #
    #                 if tabItem.winfo_class() in ['TLabel'] and strMethod in ['logic'] and 'qreCond0' in key:
    #                     strWhenLogicAssign += '|@{}'.format(self.swpCheckQreEntry.get())
    #
    #                 if tabItem.winfo_class() in ['TEntry', 'TCombobox']:
    #                     if tabItem.get():
    #                         if 'qreCond' in key:
    #                             if strMethod in ['when', 'logic']:
    #                                 strWhenLogicAssign += '|@{}'.format(tabItem.get())
    #                         elif 'itemQre' in key:
    #                             strWhenLogicAssign += '|@{}'.format(tabItem.get())
    #                         elif 'itemVal' in key:
    #                             strWhenLogicAssign += '|*{}'.format(tabItem.get())
    #                         elif 'exclusive' in key:
    #                             continue
    #                         else:
    #                             strWhenLogicAssign += '|{}'.format(tabItem.get())
    #
    #             if tabItem.winfo_class() in ['TEntry']:
    #                 strInputEtr += tabItem.get()
    #
    #             if tabItem.winfo_class() in ['TCombobox'] and not strMethod in ['when', 'assign', 'dropped']:
    #                 countCbb += 1
    #                 strInputCbb += tabItem.get()
    #
    #         if strMethod in ['when', 'logic', 'assign', 'dropped']:
    #             if not self.valCheckParentheses(strWhenLogicAssign):
    #                 messagebox.showerror('Input error', 'Parentheses is invalid')
    #                 return False
    #
    #             if strWhenLogicAssign.count('(') != strWhenLogicAssign.count(')') \
    #                     or strWhenLogicAssign.count('|and') + strWhenLogicAssign.count('|or') + 1 != strWhenLogicAssign.count('|*') \
    #                     or strWhenLogicAssign.count('@') != strWhenLogicAssign.count('*'):
    #                 messagebox.showerror('Input error', 'Characters are invalid.\n' + strWhenLogicAssign)
    #                 return False
    #             else:
    #                 strWhenLogicAssign = strWhenLogicAssign[1:]
    #                 strWhenLogicAssign = strWhenLogicAssign.replace('|(', '').replace('|)', '')
    #
    #                 if strMethod in ['when']:
    #                     strRe = re.compile(r'^@[A-Z|a-z0-9._[\]{}]+\*(~|)((({_(?!.*(Null|null|NULL|num))[A-Z|a-z0-9]+)(,_[A-Z|a-z0-9]+)*}$)|Null$|{_num(<|>|=|>=|<=)[0-9]+}$)')
    #                 else:
    #                     strRe = re.compile(r'^@[A-Z|a-z0-9._[\]{}]+\*(~|)((({_(?!.*(Null|null|NULL))[A-Z|a-z0-9]+)(,_[A-Z|a-z0-9]+)*}$)|Null$)')
    #
    #                 lstWhenLogicAssignFormated = list()
    #
    #                 if strMethod in ['when', 'logic']:
    #                     lstWhenLogicAssign = re.split('\|', strWhenLogicAssign)
    #                     step = strWhenLogicAssign.count('@')
    #                     for i in np.arange(step):
    #                         lstWhenLogicAssignFormated.extend(['{}{}'.format(lstWhenLogicAssign[i], lstWhenLogicAssign[i+step])])
    #                 else:
    #                     strWhenLogicAssign = strWhenLogicAssign.replace('|and', '#').replace('|or', '#').replace('|', '')
    #                     lstWhenLogicAssign = re.split('#', strWhenLogicAssign)
    #
    #                     lstWhenLogicAssignFormated = lstWhenLogicAssign
    #
    #                 if not list(filter(strRe.match, lstWhenLogicAssignFormated)) or lstWhenLogicAssign[-1] == '':
    #                     messagebox.showerror('Input error', 'Condition is invalid.\n' + str(lstWhenLogicAssignFormated))
    #                     return False
    #
    #         if not strInputEtr or (countCbb != 0 and not strInputCbb):
    #             messagebox.showerror('Input error', 'Please input condition.')
    #             return False
    #
    #     return True


    def isItemExistinTreeView(self, trv, itemName, child=None):
        isExist = False
        isNewVar = False

        for item in trv.get_children(child):
            if trv.item(item)['text'] == itemName:
                isExist = True
                if isinstance(trv.item(item)['tags'], list):
                    isNewVar = bool(trv.item(item)['tags'][0])
                return isExist, isNewVar
            else:
                if trv.get_children(item):
                    isExist_2 = self.isItemExistinTreeView(trv, itemName, item)
                    if isExist_2[0]:
                        return isExist_2

        return isExist, isNewVar


    def moveUpChecklistNodes(self, event=None):
        self.moveUpDownChecklistNodes(self.swpTrvChecklist, True)
        # Update checklist save status
        self.updateChecklistSaveStatus(self.swpWin)

    def moveDownChecklistNodes(self, event=None):
        self.moveUpDownChecklistNodes(self.swpTrvChecklist, False)
        # Update checklist save status
        self.updateChecklistSaveStatus(self.swpWin)


    @staticmethod
    def moveUpDownChecklistNodes(trv, isMoveUp):
        try:
            if trv.selection():
                for row in trv.selection():
                    if isMoveUp:
                        moveIdx = -1
                    else:
                        moveIdx = len(trv.selection())
                    if trv.index(row) + moveIdx < 0:
                        break
                    trv.move(row, '', trv.index(row) + moveIdx)
        except Exception:
            messagebox.showerror('Error', traceback.format_exc())


    def deleteChecklistNodes(self, event=None):
        self.funcDeleteChecklistNodes(self.swpTrvChecklist, self.swpTrvData)
        # Update checklist save status
        self.updateChecklistSaveStatus(self.swpWin)


    def funcDeleteChecklistNodes(self, trv, trvData):
        try:
            if trv.selection():
                if messagebox.askyesno('Delete item', 'You want to delete selection item(s)?'):
                    trvUnselId = set(trv.get_children()).difference(set(trv.selection()))
                    for rowid in trv.selection():
                        trvSelItem = trv.item(rowid)
                        if trvUnselId:
                            if trvSelItem['values'][0] in self.rtm.method:
                                isLeft = False
                                for unselId in trvUnselId:
                                    trvUnselItem = trv.item(unselId)
                                    if trvUnselItem['text'] == trvSelItem['text']:
                                        isLeft = True
                                if not isLeft:
                                    isExist, temp = self.isItemExistinTreeView(trvData, trvSelItem['text'])
                                    if isExist:
                                        trvData.delete(trvSelItem['text'])
                        else:
                            if trvSelItem['values'][0] in self.rtm.method:
                                trvData.delete(trvSelItem['text'])
                        trv.delete(rowid)

            else:
                messagebox.showerror('Delete item error', 'Please select checklist item(s) first.')
        except Exception:
            messagebox.showerror('Error', traceback.format_exc())


    def trvChecklistDbl1(self, event=None):
        try:
            trv = self.swpTrvChecklist
            if len(trv.selection()) == 1:
                trvSelItem = trv.item(trv.selection())
                self.swpCheckQreEntry.delete(0, 'end')
                self.swpCheckQreEntry.insert(0, trvSelItem['text'])
                self.swpCheckQreMethodCbb.set(trvSelItem['values'][0])
                self.swpCheckQreCbxVal.set(trvSelItem['values'][1])

                self.swpCheckQreMethodSelected()

                # clear before pull
                self.framesConditionClear(trvSelItem['values'][0])

                # Pull conditional
                strQreCond = trvSelItem['values'][2]
                strItemCond = trvSelItem['values'][3]
                strExclusive = trvSelItem['values'][4]

                self.addValToWidgetByStr(self.swpWin, [strQreCond, strItemCond, strExclusive])

                if self.swpCheckQreCbxVal.get():
                    self.swpCheckQreMethodCbb.config(values=self.dto.method)
                else:
                    self.swpCheckQreMethodCbb.config(values=self.hrc.method)

                trv.selection_remove(trv.selection())

        except Exception:
            messagebox.showerror('Error', traceback.format_exc())


    @staticmethod
    def addValToWidgetByStr(win, lstToAdd):
        for strAddin in lstToAdd:
            if strAddin:
                for pair in strAddin.split('@'):
                    name, val = pair.split('#')
                    widget = win.nametowidget(name)
                    if widget.winfo_class() == 'TEntry':
                        widget.delete(0, 'end')
                        widget.nametowidget(name).insert(0, val)
                    else:
                        widget.set(val)


    def saveChecklistToCsv(self, event=None):
        try:
            if self.swpTrvChecklist.get_children():
                if self.isDataActive:
                    if self.swpChecklistSavePath:
                        filePath = self.swpChecklistSavePath
                    else:
                        filePath = filedialog.asksaveasfile(filetypes=[('CSV file', '*.csv')],
                            mode='w', defaultextension='.csv',
                            initialfile='{}_Checklist.csv'.format(self.swpMetadataFile['name']))
                        self.swpChecklistSavePath = filePath

                    if filePath:
                        with open(filePath.name, 'w', newline='') as myChecklist:
                            csvWriter = csv.writer(myChecklist, delimiter=';')
                            strBakPath = r'{}\Sweeper\{}_Checklist_bak.csv'.format(os.getenv('APPDATA'), self.swpMetadataFile['name'])
                            bakDir = os.path.dirname(strBakPath)
                            if not os.path.exists(bakDir):
                                os.makedirs(bakDir)
                            myChecklist_bak = open(strBakPath, 'w', newline='')
                            csvBakWriter = csv.writer(myChecklist_bak, delimiter=';')
                            for row_id in self.swpTrvChecklist.get_children():
                                row = [row_id, self.swpTrvChecklist.item(row_id)]
                                csvWriter.writerow(row)
                                csvBakWriter.writerow(row)
                            # update checklist save status
                            self.isChecklistSave = True
                            self.strTitle = self.strTitle.replace('*', '')
                            self.swpWin.title(self.strTitle)
                            messagebox.showinfo('Save', 'Checklist is saved successful.')
            else:
                messagebox.showerror('Save error', 'Check list is null.')
        except Exception:
            messagebox.showerror('Error', traceback.format_exc())


    def loadChecklistFromCsv(self, event=None):
        try:
            if self.isDataActive:
                filePath = filedialog.askopenfile(filetypes=[('CSV file', "*.csv")])
                if filePath:
                    self.statusLabelUpdate(True, 'Loading checklist')
                    with open(filePath.name) as myChecklist:
                        csvRead = csv.reader(myChecklist, delimiter=';')
                        trvChecklist = self.swpTrvChecklist
                        for item in trvChecklist.get_children():
                            trvChecklist.delete(item)
                        for row in csvRead:
                            row_id = row[0]
                            row_data = eval(row[1])

                            isNewVar = eval(row_data['values'][1])
                            if isNewVar:
                                imgIcon = self.swpIcons['checklistCreate']
                            else:
                                imgIcon = self.swpIcons['checklistCheck']

                            trvChecklist.insert('', 'end', id=row_id, text=row_data['text'], values=row_data['values'],
                                                image=imgIcon)
                        # Update trvData with checklist loading
                        self.updateRtmWithChecklist()
                        self.updateTrvDataWithRtm()
                        self.statusLabelUpdate()
                        messagebox.showinfo('Load', 'Checklist is loaded successful.')
        except Exception:
            messagebox.showerror('Error', traceback.format_exc())


    def runChecklist(self, event=None):
        try:
            if messagebox.askyesno('Running', 'Run checklist?'):
                if self.isDataActive:
                    if len(self.swpTrvChecklist.get_children()) > 0:

                        self.statusLabelUpdate(True, 'Running')

                        startTime = time.time()

                        self.updateRtmWithChecklist()
                        self.updateTrvDataWithRtm()

                        self.rtm.df.to_csv('{}\Rawdata.csv'.format(self.swpMetadataFile['path']), encoding='utf-8-sig')

                        self.hrc = hurricane(self.rtm.df, self.rtm.dm, self.rtm.dictOutput)
                        strSummary, strDetail = self.hrc.sweep()

                        strDir_ErrorLog = '{}\sweeperErrorLog.txt'.format(self.swpMetadataFile['path'])
                        if os.path.exists(strDir_ErrorLog):
                            os.remove(strDir_ErrorLog)

                        self.statusLabelUpdate()

                        if len(strSummary) > 0:
                            txt = open(strDir_ErrorLog, 'w+', encoding='utf-8-sig')
                            txt.write(strDetail)
                            txt.close()
                            messagebox.showerror('Run error', 'ERRORS are detected. Please check result file. '
                            '\nProcess END in %.4fs' % (time.time() - startTime))
                            self.swpTextErrLog.delete('1.0', 'end')
                            self.swpTextErrLog.insert('insert', strDetail)
                            self.swpIsErrLogActive.set(True)
                        else:
                            messagebox.showinfo('Run successful', 'NO error is detected. '
                            '\nProcess END in %.4fs' % (time.time() - startTime))
                            self.swpIsErrLogActive.set(False)
                        self.errLogCallback()
                    else:
                        messagebox.showerror('Run error', 'Checklist is null.')
        except PermissionError:
            messagebox.showerror('Error', 'Please close \'Rawdata.csv\' before run.')

        except Exception:
            messagebox.showerror('Error', traceback.format_exc())

        finally:
            self.statusLabelUpdate()


    def statusLabelUpdate(self, isStart=False, strLbl=''):
        if isStart:
            self.swpWin.config(cursor='wait')
            self.swpStatusLbl.configure(text=strLbl)
            self.swpWin.after(1, self.swpWin.update())
        else:
            self.swpStatusLbl.configure(text='Ready.')
            self.swpWin.config(cursor='')


    def updateRtmWithChecklist(self):
        lstInput = self.convertChecklistToRotomList()
        self.rtm = rotom(self.dto.df, self.dto.dm, lstInput)
        self.rtm.convert()


    def updateTrvDataWithRtm(self):
        self.swpTrvData.delete(self.swpTrvData.get_children())
        self.swpTrvData.insert('', 0, self.swpMetadataFile['name'], text=self.swpMetadataFile['name'],
                               image=self.swpIcons['database'])
        self.swpTrvData.item(self.swpMetadataFile['name'], open=True)
        self.dmToMetadataTree(self.swpTrvData, self.swpMetadataFile['name'], self.rtm.dm)


    def convertChecklistToRotomList(self):
        lstInput = list()
        trvChecklist = self.swpTrvChecklist

        for row_id in trvChecklist.get_children():
            trvItem = trvChecklist.item(row_id)
            lstItem = self.convertChecklistItem(trvItem)
            lstInput.append(lstItem)

        return lstInput


    def convertChecklistItem(self, trvItem):
        strQreCond = self.restringChecklistItem(trvItem['values'], 'QreCond')
        strCondItems = self.restringChecklistItem(trvItem['values'], 'CondItems')
        strExs = self.restringChecklistItem(trvItem['values'], 'Exs')
        lstItem = [trvItem['text'], trvItem['values'][0]]
        if strQreCond:
            lstItem.extend([strQreCond])
        if strCondItems:
            lstItem.extend([strCondItems])

        if trvItem['values'][0] in ['allin', 'merge', 'assign', 'dropped', 'count']:
            lstItem.extend([strExs])
        return lstItem


    def restringChecklistItem(self, lstItem, strType):
        strResult = ''
        if strType in ['QreCond', 'Exs']:
            if 'QreCond' in strType:
                strResult = lstItem[2]
            else:
                strResult = lstItem[4]
            if strResult:
                strResult = re.sub(r'[A-Z|a-z0-9,.!]+#', '', strResult).replace('@', '|')
        elif strType in ['CondItems']:
            strResult = lstItem[3]
            if strResult:
                if 'assign' in lstItem[0] or 'dropped' in lstItem[0]:
                    strResult = re.sub(r'[A-Z|a-z0-9,.!]+#', '', strResult)
                    lstResult = strResult.split('@')
                    strTemp = ''
                    lstTemp = list()
                    idx = 0
                    for i in lstResult:
                        if i == 'and' or i == 'or':
                            strTemp += self.convertAssignCond(lstTemp) + i.replace('and', '&').replace('or', '|')
                            lstTemp = list()
                        else:
                            lstTemp.extend([i])
                            if idx == len(lstResult) - 1:
                                strTemp += self.convertAssignCond(lstTemp)
                        idx += 1
                    strResult = strTemp
                elif 'when' in lstItem[0] or 'logic' in lstItem[0]:
                    strResult = re.sub(r'[A-Z|a-z0-9,.!]+#', '', strResult)
                    lstResult = strResult.split('@')
                    for i in np.arange(len(lstResult)):
                        if lstResult[i].lower() == 'and':
                            lstResult[i] = '&'
                        elif lstResult[i].lower() == 'or':
                            lstResult[i] = '|'
                        elif lstResult[i].lower() == 'null':
                            lstResult[i] = '{_isnull}'
                        elif lstResult[i].lower() == '~null':
                            lstResult[i] = '{_notnull}'
                        elif lstResult[i].isnumeric() or lstResult[i].isdecimal():
                            lstResult[i] = '{_num' + lstResult[i] + '}'

                    strResult = ''.join(lstResult)

                else:
                    strResult = re.sub(r'[A-Z|a-z0-9,.!]+#', '', strResult).replace('@', '|')

        return strResult


    @staticmethod
    def convertAssignCond(lst):
        strResult = ''
        if len(lst) == 2:
            a, b = lst
            strResult = '[{}]*{}'.format(a, b)
        elif len(lst) == 3:
            a, b, c = lst
            if a == '(':
                strResult = '{}[{}]*{}'.format(a, b, c)
            if c == ')':
                strResult = '[{}]*{}{}'.format(a, b, c)
        elif len(lst) == 4:
            a, b, c, d = lst
            strResult = '{}[{}]*{}{}'.format(a, b, c, d)
        if '~' in strResult:
            strResult = strResult.replace('*~', '*').replace('[', '~[')
            strResult = strResult.replace('~[{', '[{')
        return strResult


    def onErrLogClose(self, event=None):
        self.swpIsErrLogActive.set(False)
        self.errLogCallback()


    def errLogCallback(self, event=None):
        if self.swpIsErrLogActive.get():
            self.swpWinErrLog.state('normal')
            self.swpWinErrLog.focus()
        else:
            self.swpWinErrLog.state('withdrawn')