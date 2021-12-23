import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from class_Sweeper import sweeper
from class_Rotom import rotom
from class_Hurricane import hurricane
import traceback
import os
import re
import pandas as pd
import numpy as np
from uuid import uuid4
import time
import calendar


class mlv(sweeper):

    def __init__(self, win, prgConn, strVer, loginName, loginPass, classArceus):
        self.mlvWin = win

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
        self.dfClient = pd.DataFrame()

        # Init
        self.mlvWin.state('zoomed')
        self.mlvWin.minsize(1200, 600)

        # Save status
        self.isChecklistSave = True

        # metadata status
        self.isDataActive = False

        # METADATA PATH & NAME
        self.mlvMetadataFile = {'path': '', 'name': ''}
        self.mlvChecklistSavePath = None

        # About
        strAbout = f'Sweeper version {self.ver}'
        strAbout += '\n\nAuthor: Hung.Dao\nEmail: hung.dao@ipsos.com'
        strAbout += '\n\nDescription: \nSweeper is developed with the aim of helping users to reduce their time spent on checking data. The data can be immediately not only checked after a checklist is created but also delivered to CSG after FW Manager has confirmed it.'
        self.strAbout = strAbout

        # Projects
        self.mlvListProject = ['None', 'KEVIN', 'FIRST CLASS', 'NEWBIE', 'URANUS', 'NIECE']

        # tkinter Style
        mlvStyle = ttk.Style()
        mlvStyle.configure('mystyle.Treeview.Heading', font=('Calibri', 11, 'bold'))

        # ICON - Keep var name
        self.swpIcons = {
            'open': tk.PhotoImage(file='Icon\Menubar\Open.png').subsample(5, 5),
            'load': tk.PhotoImage(file='Icon\Menubar\Load.png').subsample(5, 5),
            'save': tk.PhotoImage(file='Icon\Menubar\Save.png').subsample(5, 5),
            'quit': tk.PhotoImage(file='Icon\Menubar\Quit.png').subsample(6, 6),
            'run': tk.PhotoImage(file='Icon\Menubar\Run.png').subsample(6, 6),
            'features': tk.PhotoImage(file='Icon\Menubar\Features.png').subsample(5, 5),
            'errorlog': tk.PhotoImage(file='Icon\Menubar\ErrorLog.png').subsample(5, 5),
            'about': tk.PhotoImage(file='Icon\Menubar\About.png').subsample(1, 1),
            'clientDb': tk.PhotoImage(file='Icon\Menubar\ClientDb.png').subsample(6, 6),

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

        # MAIN FRAME OF MLV
        self.frMlvMain = ttk.Frame(self.mlvWin, name='frMlvMain')
        self.frMlvMain.pack(fill='both', expand=True)

        # MENU BAR
        self.mlvWin.option_add('*tearOff', False)
        self.mlvMenuBar = tk.Menu(self.frMlvMain, name='!mlvMenuBar')
        self.mlvWin.config(menu=self.mlvMenuBar)

        self.mlvMenuItems = {
            'File': tk.Menu(self.mlvMenuBar),
            'Database': tk.Menu(self.mlvMenuBar),
            'Run': tk.Menu(self.mlvMenuBar),
            'Help': tk.Menu(self.mlvMenuBar),
        }

        # MENU BAR - CREATE ITEMS
        self.mlvMenuBar.add_cascade(menu=self.mlvMenuItems['File'], label='File')
        self.mlvMenuBar.add_cascade(menu=self.mlvMenuItems['Database'], label='Database')
        self.mlvMenuBar.add_cascade(menu=self.mlvMenuItems['Run'], label='Run')
        self.mlvMenuBar.add_cascade(menu=self.mlvMenuItems['Help'], label='Help')

        # MENU BAR - ADD COMMAND
        self.mlvMenuItems['File'].add_command(label='Open metadata', command=self.mlvOpenMetadataFile)
        self.mlvMenuItems['File'].add_separator()
        self.mlvMenuItems['File'].add_command(label='Features', command=self.mlvBackToArceus)
        self.mlvMenuItems['File'].add_separator()
        self.mlvMenuItems['File'].add_command(label='Quit', command=self.mlvQuitConfirmation)

        self.mlvMenuProject = tk.Menu(self.mlvMenuItems['Database'])
        self.mlvMenuItems['Database'].add_cascade(menu=self.mlvMenuProject, label='Project')
        self.mlvMenuProjectSel = tk.StringVar()
        for prj in self.mlvListProject:
            self.mlvMenuProject.add_radiobutton(label=prj, variable=self.mlvMenuProjectSel, command=self.projectSelected)

        self.mlvMenuItems['Database'].add_separator()
        self.mlvMenuItems['Database'].add_command(label='Load client database', command=self.loadExcelDB)

        self.mlvMenuItems['Run'].add_command(label='Export weekly report', command=self.exportWeeklyReport)
        self.mlvMenuItems['Help'].add_command(label='About', command=lambda: messagebox.showinfo('About', self.strAbout))

        # MENU BAR - CONFIGURE
        self.mlvMenuItems['File'].entryconfig('Open metadata', image=self.swpIcons['open'], compound='left')
        self.mlvMenuItems['File'].entryconfig('Features', image=self.swpIcons['features'], compound='left')
        self.mlvMenuItems['File'].entryconfig('Quit', image=self.swpIcons['quit'], compound='left')

        self.mlvMenuItems['Database'].entryconfig('Project', state='disabled')
        self.mlvMenuItems['Database'].entryconfig('Load client database', image=self.swpIcons['clientDb'], compound='left', state='disabled')

        self.mlvMenuItems['Run'].entryconfig('Export weekly report', image=self.swpIcons['run'], compound='left', state='disabled')
        self.mlvMenuItems['Help'].entryconfig('About', image=self.swpIcons['about'], compound='left')

        # PANELS
        self.mlvPanels = {
            'master': ttk.PanedWindow(self.frMlvMain, orient=tk.HORIZONTAL, name='!mlvPanelsMaster'),
            'status': ttk.PanedWindow(self.frMlvMain, orient=tk.VERTICAL, name='!mlvPanelsStatus')
        }

        self.mlvPanels['master'].pack(fill='both', expand=True, side='top')
        self.mlvPanels['status'].pack(fill='x', expand=True, side='left')

        # FRAMES in PANELS
        self.mlvFrames = {
            'metadata': ttk.Frame(self.mlvPanels['master'], name='!mlvFramesMetadata'),
            'material': ttk.Frame(self.mlvPanels['master'], name='!mlvFramesMaterial', relief=tk.FLAT),
            'checklist': ttk.Frame(self.mlvPanels['master'], name='!mlvFramesChecklist', relief=tk.FLAT),
            'status': ttk.Frame(self.mlvPanels['status'], name='!mlvFramesStatus'),
        }

        # PANEL MASTER - ADD FRAMES
        self.mlvPanels['master'].add(self.mlvFrames['metadata'], weight=3)
        self.mlvPanels['master'].add(self.mlvFrames['material'], weight=1)
        self.mlvPanels['master'].add(self.mlvFrames['checklist'], weight=3)

        # PANEL MASTER - FRAME METADATA - NOTEBOOK DATA
        self.mlvNbData = ttk.Notebook(self.mlvFrames['metadata'], name='!mlvNbData')
        self.mlvNbData.pack(fill='both', expand=True)

        self.frMlvMetadata = ttk.Frame(self.mlvNbData)
        self.frMlvClientDb = ttk.Frame(self.mlvNbData)
        self.mlvNbData.add(self.frMlvMetadata, text='Metadata')
        self.mlvNbData.add(self.frMlvClientDb, text='Client Database')
        self.mlvNbData.tab(self.frMlvClientDb, state='disabled')

        # PANEL MASTER - FRAME METADATA - METADATA TREEVIEW
        self.mlvTrvData = ttk.Treeview(self.frMlvMetadata, name='!mlvTrvData', style='mystyle.Treeview')
        self.mlvTrvData.pack(side='left', fill='both', expand=True)
        self.mlvTrvData.column('#0', width=100)
        self.mlvTrvData.heading('#0', text=f'Welcome, {self.loginName}')

        # PANEL MASTER - FRAME METADATA - METADATA SCROLLBAR
        mlvScrollbarData = ttk.Scrollbar(self.frMlvMetadata, orient=tk.VERTICAL, command=self.mlvTrvData.yview)
        mlvScrollbarData.pack(side='right', fill='y')
        self.mlvTrvData.config(yscrollcommand=mlvScrollbarData.set)

        # PANEL MASTER - FRAME METADATA - CLIENT DATABASE - NOTEBOOK
        self.mlvNbClientDb = ttk.Notebook(self.frMlvClientDb, name='!mlvNbClientDb')
        self.mlvNbClientDb.pack(fill='both', expand=True)

        self.frNbClientDbSummary = ttk.Frame(self.mlvNbClientDb)
        self.frNbClientDbDetail = ttk.Frame(self.mlvNbClientDb)
        self.mlvNbClientDb.add(self.frNbClientDbSummary, text='Summary')
        self.mlvNbClientDb.add(self.frNbClientDbDetail, text='Detail')

        # PANEL MASTER - FRAME METADATA - CLIENT DATABASE - NOTEBOOK - SUMMARY
        lblDateUpload = ttk.Label(self.frNbClientDbSummary, text='Uploaded at')
        lblMonth = ttk.Label(self.frNbClientDbSummary, text='Month')
        lblTotal = ttk.Label(self.frNbClientDbSummary, text='Total')
        lblW1 = ttk.Label(self.frNbClientDbSummary, text='Week 1')
        lblW2 = ttk.Label(self.frNbClientDbSummary, text='Week 2')
        lblW3 = ttk.Label(self.frNbClientDbSummary, text='Week 3')
        lblW4 = ttk.Label(self.frNbClientDbSummary, text='Week 4')
        lblW5 = ttk.Label(self.frNbClientDbSummary, text='Week 5')

        self.valDateUpload = tk.StringVar()
        self.valMonth = tk.StringVar()
        self.valTotal = tk.StringVar()
        self.valW1 = tk.StringVar()
        self.valW2 = tk.StringVar()
        self.valW3 = tk.StringVar()
        self.valW4 = tk.StringVar()
        self.valW5 = tk.StringVar()

        valueDateUpload = ttk.Label(self.frNbClientDbSummary, textvariable=self.valDateUpload, relief=tk.SOLID)
        valueMonth = ttk.Label(self.frNbClientDbSummary, textvariable=self.valMonth, relief=tk.SOLID)
        valueTotal = ttk.Label(self.frNbClientDbSummary, textvariable=self.valTotal, relief=tk.SOLID)
        valueW1 = ttk.Label(self.frNbClientDbSummary, textvariable=self.valW1, relief=tk.SOLID)
        valueW2 = ttk.Label(self.frNbClientDbSummary, textvariable=self.valW2, relief=tk.SOLID)
        valueW3 = ttk.Label(self.frNbClientDbSummary, textvariable=self.valW3, relief=tk.SOLID)
        valueW4 = ttk.Label(self.frNbClientDbSummary, textvariable=self.valW4, relief=tk.SOLID)
        valueW5 = ttk.Label(self.frNbClientDbSummary, textvariable=self.valW5, relief=tk.SOLID)

        lblDateUpload.grid(row=0, column=0, padx=5, pady=5)
        lblMonth.grid(row=1, column=0, padx=5, pady=5)
        lblTotal.grid(row=2, column=0, padx=5, pady=5)
        lblW1.grid(row=3, column=0, padx=5, pady=5)
        lblW2.grid(row=4, column=0, padx=5, pady=5)
        lblW3.grid(row=5, column=0, padx=5, pady=5)
        lblW4.grid(row=6, column=0, padx=5, pady=5)
        lblW5.grid(row=7, column=0, padx=5, pady=5)

        valueDateUpload.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        valueMonth.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        valueTotal.grid(row=2, column=1, padx=5, pady=5, sticky='we')
        valueW1.grid(row=3, column=1, padx=5, pady=5, sticky='we')
        valueW2.grid(row=4, column=1, padx=5, pady=5, sticky='we')
        valueW3.grid(row=5, column=1, padx=5, pady=5, sticky='we')
        valueW4.grid(row=6, column=1, padx=5, pady=5, sticky='we')
        valueW5.grid(row=7, column=1, padx=5, pady=5, sticky='we')

        self.frNbClientDbSummary.grid_columnconfigure(1, weight=1)

        # PANEL MASTER - FRAME METADATA - NOTEBOOK - CLIENT DATABASE TREEVIEW & SCROLLBAR
        self.frNbClientDbDetail.propagate(False)
        self.mlvTrvClientDb = ttk.Treeview(self.frNbClientDbDetail, name='!mlvTrvClientDb', style='mystyle.Treeview', columns=['RID'])
        self.mlvTrvClientDb.heading('#0', text='Index')
        self.mlvTrvClientDb.column('#0', width=50, stretch=tk.NO)

        fr_y_ClientDB = tk.Frame(self.frNbClientDbDetail)
        fr_y_ClientDB.pack(side='right', fill='y')
        tk.Label(fr_y_ClientDB, borderwidth=1, relief='raised', font='Arial 8').pack(side='bottom', fill='x')
        mlvYScrollClientDB = tk.Scrollbar(fr_y_ClientDB, orient="vertical", command=self.mlvTrvClientDb.yview)
        mlvYScrollClientDB.pack(fill='y', expand=True)

        fr_x_ClientDB = tk.Frame(self.frNbClientDbDetail)
        fr_x_ClientDB.pack(side='bottom', fill='x')
        mlvXScrollClientDB = tk.Scrollbar(fr_x_ClientDB, orient="horizontal", command=self.mlvTrvClientDb.xview)
        mlvXScrollClientDB.pack(fill='x', expand=True)

        self.mlvTrvClientDb.configure(yscrollcommand=mlvYScrollClientDB.set, xscrollcommand=mlvXScrollClientDB.set)
        self.mlvTrvClientDb.pack(fill='both', expand=True)

        # PANEL MASTER - FRAME CHECKLIST - BUTTONS
        fr_checklistBtns = ttk.Frame(self.mlvFrames['checklist'])
        fr_checklistBtns.pack(side='top', fill='x')
        self.fr_checklistBtnsUpDown = ttk.Frame(fr_checklistBtns)
        self.fr_checklistBtnsDelete = ttk.Frame(fr_checklistBtns)
        self.fr_checklistBtnsUpDown.pack(side='left', fill='x', expand=True)
        self.fr_checklistBtnsDelete.pack(side='right', fill='x')
        self.mlvBtnChecklistMoveUp = ttk.Button(self.fr_checklistBtnsUpDown, state='disabled', image=self.swpIcons['btnmoveup'])
        self.mlvBtnChecklistMoveDown = ttk.Button(self.fr_checklistBtnsUpDown, state='disabled', image=self.swpIcons['btnmovedown'])
        self.mlvBtnChecklistDuplicate = ttk.Button(self.fr_checklistBtnsUpDown, state='disabled', image=self.swpIcons['btnduplicate'])
        self.mlvBtnChecklistSave = ttk.Button(self.fr_checklistBtnsUpDown, state='disabled', image=self.swpIcons['save'])

        self.mlvBtnChecklistMoveUp.grid(row=0, column=0, padx=1)
        self.mlvBtnChecklistMoveDown.grid(row=0, column=1, padx=1)
        self.mlvBtnChecklistDuplicate.grid(row=0, column=2, padx=1)
        self.mlvBtnChecklistSave.grid(row=0, column=3, padx=1)

        self.mlvBtnChecklistDelete = ttk.Button(self.fr_checklistBtnsDelete, state='disabled', image=self.swpIcons['btndelete'])
        self.mlvBtnChecklistDelete.pack(side='right', padx=10)

        # PANEL MASTER - FRAME CHECKLIST - TREEVIEW & SCROLLBAR
        fr_ChecklistTrv = ttk.Frame(self.mlvFrames['checklist'])
        fr_ChecklistTrv.pack(side='bottom', fill='both', expand=True)

        fr_ChecklistTrv.propagate(False)
        self.mlvTrvChecklist = ttk.Treeview(fr_ChecklistTrv, style='mystyle.Treeview', columns=['DataType', 'Status', 'cond'])
        self.mlvTrvChecklist.column('#0', width=200)
        self.mlvTrvChecklist.column('#1', width=80)
        self.mlvTrvChecklist.column('#2', width=80)
        self.mlvTrvChecklist.heading('#0', text='Columns')
        self.mlvTrvChecklist.heading('#1', text='Data type')
        self.mlvTrvChecklist.heading('#2', text='Status')

        fr_y = tk.Frame(fr_ChecklistTrv)
        fr_y.pack(side='right', fill='y')
        tk.Label(fr_y, borderwidth=1, relief='raised', font='Arial 8').pack(side='bottom', fill='x')
        mlvYScrollChecklist = tk.Scrollbar(fr_y, orient="vertical", command=self.mlvTrvChecklist.yview)
        mlvYScrollChecklist.pack(fill='y', expand=True)
        fr_x = tk.Frame(fr_ChecklistTrv)
        fr_x.pack(side='bottom', fill='x')
        mlvXScrollChecklist = tk.Scrollbar(fr_x, orient="horizontal", command=self.mlvTrvChecklist.xview)
        mlvXScrollChecklist.pack(fill='x', expand=True)

        self.mlvTrvChecklist.configure(yscrollcommand=mlvYScrollChecklist.set, xscrollcommand=mlvXScrollChecklist.set)
        self.mlvTrvChecklist.pack(fill='both', expand=True)

        self.mlvBtnChecklistMoveUp.configure(command=self.mlvMoveUpChecklistNodes)
        self.mlvBtnChecklistMoveDown.configure(command=self.mlvMoveDownChecklistNodes)
        self.mlvBtnChecklistDuplicate.configure(command=self.mlvDuplicateChecklistNode)
        self.mlvBtnChecklistSave.configure(command=self.saveChecklistToAPI)
        self.mlvBtnChecklistDelete.configure(command=self.mlvDeleteChecklistNodes)

        # PANEL STATUS - FRAME STATUS - LABEL
        self.mlvFrames['status'].pack(side='left', fill='x', expand=True)
        self.mlvStatusLbl = ttk.Label(self.mlvFrames['status'], text='Ready.')
        self.mlvStatusLbl.pack(side='left')
        self.mlvStatusCountLbl = ttk.Label(self.mlvFrames['status'], text='')
        self.mlvStatusCountLbl.pack(side='right')

        # PANEL MASTER - FRAMES MATERIAL - PACK FRAMES
        self.mlvMaterialFrames = {
            'question': ttk.Frame(self.mlvFrames['material'], name='!mlvMaterialFramesQuestion', relief=tk.FLAT),
            'navigation': ttk.Frame(self.mlvFrames['material'], name='!mlvMaterialFramesNavigation', relief=tk.FLAT),
            'condition': ttk.Frame(self.mlvFrames['material'], name='!mlvMaterialFramesCondition', relief=tk.FLAT),
        }

        self.mlvMaterialFrames['question'].grid(row=0, column=0, sticky='snew')
        self.mlvMaterialFrames['navigation'].grid(row=0, column=1, sticky='snew')
        self.mlvMaterialFrames['condition'].grid(row=1, column=0, columnspan=2, sticky='snew')
        self.mlvFrames['material'].grid_columnconfigure(0, weight=1)
        self.mlvFrames['material'].grid_rowconfigure(1, weight=1)

        # PANEL MASTER - FRAME MATERIAL - FRAME QUESTION - QUESTION
        mlvCheckQreLbl = ttk.Label(self.mlvMaterialFrames['question'], text='Question:')
        mlvCheckQreLbl.grid(row=1, column=0, padx=5, pady=10, sticky='w')

        self.mlvCheckQre = ttk.Entry(self.mlvMaterialFrames['question'], name='!mlvCheckQre', state='disabled')
        self.mlvCheckQre.grid(row=1, column=1, padx=5, pady=10, sticky='ew')

        # PANEL MASTER - FRAME MATERIAL - FRAME QUESTION - REPORT TYPE
        mlvReportTypeLbl = ttk.Label(self.mlvMaterialFrames['question'], text='Report type:')
        mlvReportTypeLbl.grid(row=2, column=0, padx=5, pady=0, sticky='w')

        self.lstReportType = ['Num', 'Text', 'Date', 'SA', 'MA']
        self.mlvReportType = ttk.Combobox(self.mlvMaterialFrames['question'], name='!mlvReportType', state='disabled',
                                          values=self.lstReportType)
        self.mlvReportType.grid(row=2, column=1, padx=5, pady=0, sticky='ew')
        self.mlvMaterialFrames['question'].columnconfigure(1, weight=1)

        # PANEL MASTER - FRAME MATERIAL - FRAME QUESTION - STATUS
        mlvQreSttLbl = ttk.Label(self.mlvMaterialFrames['question'], text='Status')
        mlvQreSttLbl.grid(row=3, column=0, padx=5, pady=10, sticky='w')

        self.mlvQreStatus = ttk.Combobox(self.mlvMaterialFrames['question'], name='!mlvQreStatus', values=['Enable', 'Disable'], state='disabled')
        self.mlvQreStatus.grid(row=3, column=1, padx=5, pady=10, sticky='ew')

        # FRAME MATERIAL - FRAME NAVIGATION - BUTTONS
        self.mlvNavBtns = {
            'clear': ttk.Button(self.mlvMaterialFrames['navigation'], state='disabled', image=self.swpIcons['btnclear'], command=self.mlvClearConfirm),
            'submit': ttk.Button(self.mlvMaterialFrames['navigation'], state='disabled', image=self.swpIcons['btnsubmit'], command=self.mlvAddChecklistNode),
            'update': ttk.Button(self.mlvMaterialFrames['navigation'], state='disabled', image=self.swpIcons['btnupdate'], command=self.mlvUpdateChecklistNode),
        }

        self.mlvNavBtns['clear'].pack(fill='x', side='left', padx=1, expand=True)
        self.mlvNavBtns['update'].pack(fill='x', side='left', padx=1, expand=True)
        self.mlvNavBtns['submit'].pack(fill='x', side='right', padx=1, expand=True)

        # FRAME MATERIAL - FRAME CONDITION - NOTEBOOK
        self.mlvNbCond = ttk.Notebook(self.mlvMaterialFrames['condition'], name='!mlvNbCond')
        self.mlvNbCond.pack(fill='both', expand=True)

        self.mlvNbCondTabs = dict()
        for rpType in self.lstReportType:
            self.mlvNbCondTabs[rpType] = ttk.Frame(self.mlvNbCond, name=f'!mlvNbCondTabs_{rpType}')
            self.mlvNbCond.add(self.mlvNbCondTabs[rpType], text=rpType)
            self.mlvNbCond.tab(self.mlvNbCondTabs[rpType], state='hidden')

        self.mlvNbCondTabItems = {
            'Num': {
                'label': ttk.Label(self.mlvNbCondTabs['Num'], text='Report column name'),
                'reportColName': ttk.Entry(self.mlvNbCondTabs['Num'], name='!mlvNbCondNumReportColName'),
            },
            'Text': {
                'label': ttk.Label(self.mlvNbCondTabs['Text'], text='Report column name'),
                'reportColName': ttk.Entry(self.mlvNbCondTabs['Text'], name='!mlvNbCondTextReportColName'),
            },
            'Date': {
                'label': ttk.Label(self.mlvNbCondTabs['Date'], text='Report column name'),
                'reportColName': ttk.Entry(self.mlvNbCondTabs['Date'], name='!mlvNbCondDateReportColName'),
            },
            'MA': {
                'label1': ttk.Label(self.mlvNbCondTabs['MA'], text='Report column name'),
                'reportColName': ttk.Entry(self.mlvNbCondTabs['MA'], name='!mlvNbCondMAReportColName'),
                'label2': ttk.Label(self.mlvNbCondTabs['MA'], text='Report column count'),
                'numReportCol': ttk.Spinbox(self.mlvNbCondTabs['MA'], name='!mlvNbCondMANumReportCol', from_=1, to=20),
            },
            'SA': {
                'label1': ttk.Label(self.mlvNbCondTabs['SA'], text='Report column name'),
                'reportColName': ttk.Entry(self.mlvNbCondTabs['SA'], name='!mlvNbCondSAReportColName'),
                'label2': ttk.Label(self.mlvNbCondTabs['SA'], text='Mdd code'),
                'label3': ttk.Label(self.mlvNbCondTabs['SA'], text='Report label'),

                'mddCode0': ttk.Entry(self.mlvNbCondTabs['SA'], name='!mlvNbCondSAMddCode0'),
                'reportLbl0': ttk.Entry(self.mlvNbCondTabs['SA'], name='!mlvNbCondSAReportLbl0'),

                'mddCode1': ttk.Entry(self.mlvNbCondTabs['SA'], name='!mlvNbCondSAMddCode1'),
                'reportLbl1': ttk.Entry(self.mlvNbCondTabs['SA'], name='!mlvNbCondSAReportLbl1'),

                'mddCode2': ttk.Entry(self.mlvNbCondTabs['SA'], name='!mlvNbCondSAMddCode2'),
                'reportLbl2': ttk.Entry(self.mlvNbCondTabs['SA'], name='!mlvNbCondSAReportLbl2'),

                'mddCode3': ttk.Entry(self.mlvNbCondTabs['SA'], name='!mlvNbCondSAMddCode3'),
                'reportLbl3': ttk.Entry(self.mlvNbCondTabs['SA'], name='!mlvNbCondSAReportLbl3'),

                'mddCode4': ttk.Entry(self.mlvNbCondTabs['SA'], name='!mlvNbCondSAMddCode4'),
                'reportLbl4': ttk.Entry(self.mlvNbCondTabs['SA'], name='!mlvNbCondSAReportLbl4'),

                'mddCode5': ttk.Entry(self.mlvNbCondTabs['SA'], name='!mlvNbCondSAMddCode5'),
                'reportLbl5': ttk.Entry(self.mlvNbCondTabs['SA'], name='!mlvNbCondSAReportLbl5'),

                'mddCode6': ttk.Entry(self.mlvNbCondTabs['SA'], name='!mlvNbCondSAMddCode6'),
                'reportLbl6': ttk.Entry(self.mlvNbCondTabs['SA'], name='!mlvNbCondSAReportLbl6'),

                'mddCode7': ttk.Entry(self.mlvNbCondTabs['SA'], name='!mlvNbCondSAMddCode7'),
                'reportLbl7': ttk.Entry(self.mlvNbCondTabs['SA'], name='!mlvNbCondSAReportLbl7'),

                'mddCode8': ttk.Entry(self.mlvNbCondTabs['SA'], name='!mlvNbCondSAMddCode8'),
                'reportLbl8': ttk.Entry(self.mlvNbCondTabs['SA'], name='!mlvNbCondSAReportLbl8'),

                'mddCode9': ttk.Entry(self.mlvNbCondTabs['SA'], name='!mlvNbCondSAMddCode9'),
                'reportLbl9': ttk.Entry(self.mlvNbCondTabs['SA'], name='!mlvNbCondSAReportLbl9'),

                'mddCode10': ttk.Entry(self.mlvNbCondTabs['SA'], name='!mlvNbCondSAMddCode10'),
                'reportLbl10': ttk.Entry(self.mlvNbCondTabs['SA'], name='!mlvNbCondSAReportLbl10'),
            },
        }

        for rpType in self.lstReportType:
            if rpType in ['Num', 'Text', 'Date']:
                self.mlvNbCondTabItems[rpType]['label'].grid(row=1, column=0, padx=5, pady=5)
                self.mlvNbCondTabItems[rpType]['reportColName'].grid(row=1, column=1, padx=5, pady=5, sticky='ew')
                self.mlvNbCondTabs[rpType].grid_columnconfigure(1, weight=1)
            elif rpType in ['MA']:
                self.mlvNbCondTabItems[rpType]['label1'].grid(row=1, column=0, padx=5, pady=5)
                self.mlvNbCondTabItems[rpType]['reportColName'].grid(row=1, column=1, padx=5, pady=5, sticky='ew')
                self.mlvNbCondTabItems[rpType]['label2'].grid(row=2, column=0, padx=5, pady=5)
                self.mlvNbCondTabItems[rpType]['numReportCol'].grid(row=2, column=1, padx=5, pady=5, sticky='ew')
                self.mlvNbCondTabs[rpType].grid_columnconfigure(1, weight=1)
            else:
                self.mlvNbCondTabItems[rpType]['label1'].grid(row=1, column=0, padx=5, pady=5)
                self.mlvNbCondTabItems[rpType]['reportColName'].grid(row=1, column=1, padx=5, pady=5, sticky='ew')
                self.mlvNbCondTabItems[rpType]['label2'].grid(row=2, column=0, padx=5, pady=5)
                self.mlvNbCondTabItems[rpType]['label3'].grid(row=2, column=1, padx=5, pady=5, sticky='ew')
                for i in np.arange(11):
                    self.mlvNbCondTabItems[rpType][f'mddCode{i}'].grid(row=i + 3, column=0, padx=5, pady=5, sticky='w')
                    self.mlvNbCondTabItems[rpType][f'reportLbl{i}'].grid(row=i + 3, column=1, padx=5, pady=5, sticky='ew')
                self.mlvNbCondTabs[rpType].grid_columnconfigure(1, weight=1)

        self.mlvReportType.bind('<<ComboboxSelected>>', self.reportTypeSelected)
        self.mlvTrvData.bind('<Double-1>', self.mlvInputTrvDataSelToCheckQre)
        self.mlvCheckQre.bind('<Button-1>', self.mlvInputTrvDataSelToCheckQre)
        self.mlvTrvChecklist.bind('<Double-1>', self.mlvTrvChecklistDbl1)
        self.mlvWin.protocol("WM_DELETE_WINDOW", self.mlvQuitConfirmation)


    def mlvBackToArceus(self, event=None):
        self.frMlvMain.destroy()
        self.classArceus(self.mlvWin, self.prgConn, self.ver, self.loginName, self.loginPass)


    def mlvQuitConfirmation(self, event=None):
        isQuit = False
        if self.isChecklistSave:
            if messagebox.askyesno('Confirmation', 'Are you sure you want to quit?'):
                isQuit = True
        else:
            if self.mlvTrvChecklist.get_children():
                if messagebox.askyesno('Save confirmation', 'Want to save your checklist changes?'):
                    self.saveChecklistToAPI()
            isQuit = True

        if isQuit:
            self.mlvWin.iconify()
            isValidAcc, isValidStt = self.prgConn.tryLogin(self.loginName, self.loginPass, isLogin=False)
            if isValidAcc and isValidStt:
                self.mlvWin.quit()
            else:
                self.mlvWin.deiconify()
                messagebox.showerror('Quit error', 'Please check your internet connection.')


    def mlvOpenMetadataFile(self, event=None):
        try:
            filePath = filedialog.askopenfile(filetypes=[('Metadata file', "*.mdd")])
            strSqlWhere = None
            if filePath:
                strSqlWhere = simpledialog.askstring('SELECT * FROM VDATA', 'WHERE\t\t\t\t\t', parent=self.mlvWin,
                                                     initialvalue='_LoaiPhieu IS NOT NULL')
            if filePath and strSqlWhere:
                self.mlvStatusLabelUpdate(True, 'Opening metadata')
                lstPath = os.path.split(filePath.name)
                self.mlvMetadataFile['path'] = lstPath[0]
                self.mlvMetadataFile['name'] = lstPath[1].replace('.mdd', '')

                if self.funcOpenMetadataFile(self.mlvMetadataFile['path'], self.mlvMetadataFile['name'],
                                             strSqlWhere, self.mlvTrvData, self.mlvTrvChecklist):

                    self.strTitle = 'Sweeper {} - {}'.format(self.ver, self.mlvMetadataFile['name'])
                    self.mlvWin.title(self.strTitle)

                    self.mlvMenuProjectSel.set('None')
                    self.mlvMenuItems['Database'].entryconfig('Project', state='normal')
                    self.mlvNbData.tab(self.frMlvClientDb, state='disabled')
                    self.mlvChildsOfFrameState(self.mlvMaterialFrames['question'], True)
                    self.mlvChildsOfFrameState(self.mlvMaterialFrames['navigation'], True)
                    for rpType in self.lstReportType:
                        self.mlvNbCond.tab(self.mlvNbCondTabs[rpType], state='hidden')
                    self.mlvChildsOfFrameState(self.fr_checklistBtnsUpDown, True)
                    self.mlvChildsOfFrameState(self.fr_checklistBtnsDelete, True)
                    self.mlvMenuItems['Run'].entryconfig('Export weekly report', state='disabled')

                    if self.mlvTrvClientDb.get_children():
                        for node in self.mlvTrvClientDb.get_children():
                            self.mlvTrvClientDb.delete(node)

                    self.isDataActive = True

                    strCountSample = re.sub('[\'{}]', '', str(self.dto.countSample()))
                    self.mlvStatusCountLbl.configure(text=strCountSample)

                    messagebox.showinfo('Opening', 'Open {} successful.'.format(self.mlvMetadataFile['name']))

                else:
                    messagebox.showerror('Opening error', 'No record loaded.')

        except Exception:
            messagebox.showerror('Error', traceback.format_exc())
        finally:
            self.mlvStatusLabelUpdate()


    def mlvStatusLabelUpdate(self, isStart=False, strLbl=''):
        if isStart:
            self.mlvWin.config(cursor='wait')
            self.mlvStatusLbl.configure(text=strLbl)
            self.mlvWin.after(1, self.mlvWin.update())
        else:
            self.mlvStatusLbl.configure(text='Ready.')
            self.mlvWin.config(cursor='')


    def projectSelected(self, event=None):
        try:
            strProjectSel = self.mlvMenuProjectSel.get()

            if strProjectSel == 'None':
                self.mlvCheckQre.delete(0, 'end')
                self.mlvReportType.set('')
                self.mlvQreStatus.set('')
                self.mlvNbData.tab(self.frMlvClientDb, state='disabled')
                self.mlvChildsOfFrameState(self.mlvMaterialFrames['question'], True)
                self.mlvChildsOfFrameState(self.mlvMaterialFrames['navigation'], True)
                for rpType in self.lstReportType:
                    self.mlvNbCond.tab(self.mlvNbCondTabs[rpType], state='hidden')
                self.mlvChildsOfFrameState(self.fr_checklistBtnsUpDown, True)
                self.mlvChildsOfFrameState(self.fr_checklistBtnsDelete, True)
                self.mlvMenuItems['Database'].entryconfig('Load client database', state='disabled')
                self.mlvMenuItems['Run'].entryconfig('Export weekly report', state='disabled')

                if self.mlvTrvChecklist.get_children():
                    for node in self.mlvTrvChecklist.get_children():
                        self.mlvTrvChecklist.delete(node)

                if self.mlvTrvClientDb.get_children():
                    for node in self.mlvTrvClientDb.get_children():
                        self.mlvTrvClientDb.delete(node)

            else:
                if strProjectSel.replace(' ', '_') in self.mlvMetadataFile['name']:
                    self.mlvNbData.tab(self.frMlvClientDb, state='normal')
                    self.mlvNbData.select(self.frMlvClientDb)
                    self.mlvChildsOfFrameState(self.mlvMaterialFrames['question'], False)
                    self.mlvChildsOfFrameState(self.mlvMaterialFrames['navigation'], False)
                    self.mlvChildsOfFrameState(self.fr_checklistBtnsUpDown, False)
                    self.mlvChildsOfFrameState(self.fr_checklistBtnsDelete, False)
                    self.mlvMenuItems['Database'].entryconfig('Load client database', state='normal')
                    self.mlvMenuItems['Run'].entryconfig('Export weekly report', state='normal')
                    self.mlvReportType.configure(state='readonly')
                    self.mlvQreStatus.configure(state='readonly')

                    # Load Checklist
                    self.loadChecklistFromAPI(strProjectSel)

                else:
                    self.mlvMenuProjectSel.set('None')

                    if self.mlvTrvChecklist.get_children():
                        for node in self.mlvTrvChecklist.get_children():
                            self.mlvTrvChecklist.delete(node)

                    if self.mlvTrvClientDb.get_children():
                        for node in self.mlvTrvClientDb.get_children():
                            self.mlvTrvClientDb.delete(node)

                    messagebox.showerror('Error', 'Incorrect project selection.')
        except Exception:
            messagebox.showerror('Error', traceback.format_exc())
        finally:
            self.mlvStatusLabelUpdate()

    def loadExcelDB(self):
        try:
            filePath = filedialog.askopenfile(filetypes=[('Xlsx file', "*.xlsx")])
            prjName = self.mlvMenuProjectSel.get()

            if filePath:
                if prjName.upper() in filePath.name.upper():
                    self.mlvStatusLabelUpdate(True, 'Opening client database')
                    lstPath = os.path.split(filePath.name)

                    self.dfClient = pd.read_excel(filePath.name, sheet_name='Report')

                    self.mlvNbData.tab(self.frMlvClientDb, state='normal')

                    isValid, errLbl = self.prgConn.tryAddMlvClientDb(prjName, self.dfClient)

                    if not isValid:
                        messagebox.showerror('Error', errLbl)
                    else:
                        isValidClientDb = self.mlvLoadClientDb(prjName)

                        self.addDfClientDbToTrv(self.mlvTrvClientDb, self.dfClient)

                        messagebox.showinfo('Opening', f'Open {lstPath[1]} successful.')
                else:
                    messagebox.showerror('Error', 'Please check the excel file.')
        except Exception:
            messagebox.showerror('Error', traceback.format_exc())
        finally:
            self.mlvStatusLabelUpdate()


    def mlvLoadClientDb(self, prjName):
        isValidClientDb, self.dfClient, strUploadedDate = self.prgConn.tryLoadMlvFormat(f'{prjName}_db')
        df = self.dfClient.copy()

        self.valDateUpload.set(strUploadedDate)

        if prjName in ['URANUS']:
            strW, strM, strY = self.mlvGetWaveInfoFromID(prjName, df['Week'].iloc[-1])
        else:
            strW, strM, strY = self.mlvGetWaveInfoFromID(prjName, df['RID'].iloc[-1])
            df['Week'] = [0] * df.shape[0]
            df = df.loc[:, ['RID', 'Week']]
            for idx in df.index:
                df.at[idx, 'Week'] = int(self.mlvGetWaveInfoFromID(prjName, df.loc[idx, 'RID'])[0])

        self.valMonth.set(strM)
        self.valTotal.set(self.dfClient.shape[0])

        self.valW1.set(df.loc[(df['Week'] == 1)].shape[0])
        self.valW2.set(df.loc[(df['Week'] == 2)].shape[0])
        self.valW3.set(df.loc[(df['Week'] == 3)].shape[0])
        self.valW4.set(df.loc[(df['Week'] == 4)].shape[0])
        self.valW5.set(df.loc[(df['Week'] == 5)].shape[0])

        return isValidClientDb


    @staticmethod
    def addDfClientDbToTrv(trvClientDb, dfClient):
        dfClientCols = dfClient.columns.values
        trvClientDb.configure(columns=dfClientCols)

        if trvClientDb.get_children():
            for node in trvClientDb.get_children():
                trvClientDb.delete(node)

        for i in range(len(dfClientCols)):
            trvClientDb.heading(f'#{i + 1}', text=dfClientCols[i])
            trvClientDb.column(f'#{i + 1}', width=100, stretch=tk.NO)

        for idx in dfClient.index:
            trvClientDb.insert('', idx, text=idx, values=dfClient.loc[idx, :].tolist())


    def reportTypeSelected(self, event=None):
        for rpType in self.lstReportType:
            self.mlvNbCond.tab(self.mlvNbCondTabs[rpType], state='hidden')

        for tab in self.mlvNbCondTabs:
            if self.mlvReportType.get() == tab:
                self.mlvNbCond.select(self.mlvNbCondTabs[tab])
                self.mlvNbCond.tab(self.mlvNbCondTabs[tab], state='normal')
            else:
                self.mlvNbCond.tab(self.mlvNbCondTabs[tab], state='hidden')
                if isinstance(self.mlvNbCondTabItems[tab], dict):
                    for key in self.mlvNbCondTabItems[tab].keys():
                        if self.mlvNbCondTabItems[tab][key].winfo_class() in ['TEntry', 'TSpinbox']:
                            self.mlvNbCondTabItems[tab][key].delete(0, 'end')
                        # elif self.mlvNbCondTabItems[tab][key].winfo_class() in ['TCombobox']:
                        #     self.mlvNbCondTabItems[tab][key].set('')


    @staticmethod
    def mlvChildsOfFrameState(frame, isDisabled):
        if isDisabled:
            for child in frame.winfo_children():
                if child.winfo_class() != 'TLabel':
                    child.configure(state='disabled')
        else:
            for child in frame.winfo_children():
                if child.winfo_class() == 'TCombobox':
                    child.configure(state='readonly')
                else:
                    if child.winfo_class() != 'TLabel':
                        child.configure(state='normal')


    def mlvInputTrvDataSelToCheckQre(self, event=None):
        if self.mlvValCheckTrvDataSelNode():
            trv = self.mlvTrvData
            if trv.selection():
                self.mlvCheckQre.delete(0, 'end')
                self.mlvCheckQre.insert(0, '|'.join(trv.selection()))
                trv.selection_remove(trv.selection())


    def mlvValCheckTrvDataSelNode(self):
        sel = '|'.join(self.mlvTrvData.selection())
        if sel == self.mlvMetadataFile['name'] or '[..]' in sel:
            return False
        return True


    def mlvClearConfirm(self, event=None):
        if self.isDataActive:
            cbbSelVal = self.mlvReportType.get()
            if cbbSelVal:
                confirmAns = messagebox.askyesnocancel('Confirmation', 'Are you sure you want to clear values?\n\n'
                                                                       'Yes = clear all input values.\n'
                                                                       'No = clear "' + cbbSelVal + '" values.\n'
                                                                       'Cancel = do nothing.')
                if confirmAns is True:
                    self.mlvFramesQuestionClear()
                    self.mlvFramesConditionClear(cbbSelVal)
                elif confirmAns is False:
                    self.mlvFramesConditionClear(cbbSelVal)
                elif confirmAns is None:
                    pass


    def mlvFramesQuestionClear(self):
        self.mlvCheckQre.delete(0, 'end')
        self.mlvNbCond.tab(self.mlvNbCondTabs[self.mlvReportType.get()], state='hidden')
        self.mlvReportType.set('')
        self.mlvQreStatus.set('')


    def mlvFramesConditionClear(self, cbbSelVal):
        if isinstance(self.mlvNbCondTabItems[cbbSelVal], dict):
            for key in self.mlvNbCondTabItems[cbbSelVal].keys():
                tabItem = self.mlvNbCondTabItems[cbbSelVal][key]
                if tabItem.winfo_class() == 'TEntry':
                    tabItem.delete(0, 'end')
                # if tabItem.winfo_class() == 'TCombobox':
                #     tabItem.set('')
                if tabItem.winfo_class() == 'TSpinbox':
                    tabItem.delete(0, 'end')


    def mlvAddChecklistNode(self, event=None):
        if self.isDataActive:
            self.mlvAddUpdateChecklistNode(True)


    def mlvUpdateChecklistNode(self, event=None):
        if self.isDataActive:
            if len(self.mlvTrvChecklist.selection()) == 0:
                messagebox.showwarning('Warning', 'Please select update item.')
            elif len(self.mlvTrvChecklist.selection()) > 1:
                messagebox.showwarning('Warning', 'Cannot update multiple items.')
            else:
                if messagebox.askyesno('Confirmation', 'Update this item?'):
                    self.mlvAddUpdateChecklistNode(False)


    def mlvAddUpdateChecklistNode(self, isAddin):
        try:
            if self.mlvCheckQre.get() and self.mlvReportType.get():
                trv = self.mlvTrvChecklist
                trvId = uuid4().hex
                trvText = self.mlvCheckQre.get()
                trvVals = [self.mlvReportType.get(), self.mlvQreStatus.get()]

                strItemCond = str()

                # Push conditional
                selTab = self.mlvNbCondTabItems[self.mlvReportType.get()]
                if isinstance(selTab, dict):
                    for key in selTab:
                        selTabItem = selTab[key]
                        if selTabItem.winfo_class() in ['TEntry', 'TCombobox', 'TSpinbox'] and selTabItem.get():
                                strItemCond += f'{str(selTabItem)}#{selTabItem.get()}@'

                strItemCond = strItemCond[0:-1]
                trvVals.extend([strItemCond])

                # Validate Question before insert
                isQreInputErr, strQreInputErr = self.mlvValCheckQuestionInput(self.mlvCheckQre)
                if isAddin and not isQreInputErr:
                    self.selectInvalidQuestion(self.mlvCheckQre)
                    messagebox.showerror('Input error', strQreInputErr)
                    return isQreInputErr

                # # Validate Inputting Conditional before insert
                isCondInputErr, strCondInputErr = self.mlvValCheckConditionInput()
                if not isCondInputErr:
                    messagebox.showerror('Input error', strCondInputErr)
                    return isCondInputErr

                # Insert Item
                strTag = 'mlv'
                if trv.selection():
                    selIndex = trv.index(trv.selection())
                    trv.insert('', selIndex, trvId, text=trvText, values=tuple(trvVals), tag=(strTag,),
                               image=self.swpIcons['checklistCheck'])

                    if not isAddin:
                        trv.delete(trv.selection())

                else:
                    trv.insert('', 'end', trvId, text=trvText, values=tuple(trvVals), tag=(strTag,), image=self.swpIcons['checklistCheck'])
                    trv.update()
                    trv.yview_moveto(1)

                # Clear after push
                self.mlvFramesQuestionClear()
                self.mlvFramesConditionClear(trvVals[0])

                # Update checklist save status
                self.updateChecklistSaveStatus(self.mlvWin)

                return True

            else:
                messagebox.showerror('Error', 'Please input question name and report column type.')
                return False
        except Exception:
            messagebox.showerror('Error', traceback.format_exc())


    def mlvMoveUpChecklistNodes(self, event=None):
        self.moveUpDownChecklistNodes(self.mlvTrvChecklist, True)
        self.updateChecklistSaveStatus(self.mlvWin)


    def mlvMoveDownChecklistNodes(self, event=None):
        self.moveUpDownChecklistNodes(self.mlvTrvChecklist, False)
        self.updateChecklistSaveStatus(self.mlvWin)


    def mlvDuplicateChecklistNode(self, event=None):
        self.funcDuplicateChecklistNode(self.mlvTrvChecklist)
        self.updateChecklistSaveStatus(self.mlvWin)


    def mlvDeleteChecklistNodes(self, event=None):
        self.funcDeleteChecklistNodes(self.mlvTrvChecklist, self.mlvTrvData)
        self.updateChecklistSaveStatus(self.mlvWin)


    def mlvTrvChecklistDbl1(self, event=None):
        try:
            trv = self.mlvTrvChecklist
            if len(trv.selection()) == 1:
                trvSelItem = trv.item(trv.selection())
                self.mlvCheckQre.delete(0, 'end')
                self.mlvCheckQre.insert(0, trvSelItem['text'])
                self.mlvReportType.set(trvSelItem['values'][0])
                self.mlvQreStatus.set(trvSelItem['values'][1])

                self.reportTypeSelected()

                # clear before pull
                self.mlvFramesConditionClear(trvSelItem['values'][0])

                # Pull conditional
                strItemCond = trvSelItem['values'][2]

                self.addValToWidgetByStr(self.mlvWin, [strItemCond])

                trv.selection_remove(trv.selection())

        except Exception:
            messagebox.showerror('Error', traceback.format_exc())


    def mlvValCheckQuestionInput(self, checkQre):
        qreName = checkQre.get()
        strRe = re.compile('(^\w+$)|(^\w+\.(\w+\[{\w+}]\.)*\w+$)')
        if not strRe.match(qreName):
            return False, f'{qreName} is invalid.'

        isExistItem, isNewVar = self.isItemExistinTreeView(self.mlvTrvData, qreName)
        if not isExistItem:
            return False, f'{qreName} is not exist.'

        if not self.mlvQreStatus.get():
            return False, 'Please input question status'

        return True, None


    def mlvValCheckConditionInput(self):
        strRpType = self.mlvReportType.get()
        dictCheckTab = self.mlvNbCondTabItems[strRpType]

        for key in dictCheckTab.keys():
            tabItem = dictCheckTab[key]

            if strRpType in ['Num', 'Text', 'Date']:
                if 'reportColName' in key:
                    if not self.valCheckConditionIsNull(tabItem):
                        return False, 'Please input report column name.'
                    strRe = re.compile('\w+')
                    if not self.valCheckMatchRegex(strRe, tabItem):
                        return False, f'{tabItem.get()} is invalid name.'

            elif strRpType in ['MA']:
                if 'reportColName' in key:
                    if not self.valCheckConditionIsNull(tabItem):
                        return False, 'Please input report column name.'
                    strRe = re.compile('\w+')
                    if not self.valCheckMatchRegex(strRe, tabItem):
                        return False, f'{tabItem.get()} is invalid name.'
                if 'numReportCol' in key:
                    if not self.valCheckConditionIsNull(tabItem):
                        return False, 'Please input No. report column.'
                    strRe = re.compile('20|^[1-9]$|^1[0-9]$')
                    if not self.valCheckMatchRegex(strRe, tabItem):
                        return False, 'Please input from 0 to 20.'

            elif strRpType in ['SA']:
                if 'reportColName' in key:
                    if not self.valCheckConditionIsNull(tabItem):
                        return False, 'Please input report column name.'
                    strRe = re.compile('\w+')
                    if not self.valCheckMatchRegex(strRe, tabItem):
                        return False, f'{tabItem.get()} is invalid name.'

                if 'mddCode' in key:
                    if key == 'mddCode0':
                        if not self.valCheckConditionIsNull(tabItem):
                            return False, 'Please input at least 1 code.'
                    strRe = re.compile('^_\w+$')
                    if not self.valCheckMatchRegex(strRe, tabItem):
                        return False, f'{tabItem.get()} is invalid code.'

                if 'reportLbl' in key:
                    if key == 'reportLbl0':
                        if not self.valCheckConditionIsNull(tabItem):
                            return False, 'Please input at least 1 label.'
                    strRe = re.compile('\w+')
                    if not self.valCheckMatchRegex(strRe, tabItem):
                        return False, f'{tabItem.get()} is invalid label.'

            else:
                return False, 'Not yet assign inputting validation.'

        return True, None


    def saveChecklistToAPI(self, event=None):
        try:
            trv = self.mlvTrvChecklist
            lstRows = list()
            if trv.get_children():
                if self.isDataActive:
                    for row_id in trv.get_children():
                        lstRows.append([row_id, str(trv.item(row_id))])
                isValid, errLbl = self.prgConn.trySaveMlvFormat(self.loginName, self.mlvMenuProjectSel.get(), lstRows)

                if isValid:
                    # update checklist save status
                    self.isChecklistSave = True
                    self.strTitle = self.strTitle.replace('*', '')
                    self.mlvWin.title(self.strTitle)
                    messagebox.showinfo('Save', 'Checklist is saved successful.')
                else:
                    messagebox.showerror('Save error', errLbl)
            else:
                messagebox.showerror('Save error', 'Check list is null.')
        except Exception:
            messagebox.showerror('Error', traceback.format_exc())


    def loadChecklistFromAPI(self, prjName):
        try:
            if self.isDataActive:
                self.mlvStatusLabelUpdate(True, 'Loading client database and formated-list')

                isValidClientDb = self.mlvLoadClientDb(prjName)

                isValidChecklist, dfChecklist, strUploadedDate = self.prgConn.tryLoadMlvFormat(prjName)

                if not isValidClientDb or not isValidChecklist:
                    messagebox.showinfo('Loading error', 'Please check your connection.')
                else:
                    trv = self.mlvTrvClientDb
                    for item in trv.get_children():
                        trv.delete(item)

                    if not self.dfClient.empty:
                        self.addDfClientDbToTrv(trv, self.dfClient)

                    trv = self.mlvTrvChecklist
                    for item in trv.get_children():
                        trv.delete(item)

                    if not dfChecklist.empty:
                        for idx in dfChecklist.index:
                            sr = dfChecklist.loc[idx]
                            dictItem = eval(sr['Item'])
                            trv.insert('', 'end', sr['ID'], text=dictItem['text'],
                                       image=self.swpIcons['checklistCheck'],
                                       values=dictItem['values'], open=dictItem['open'], tags=dictItem['tags'])

                    messagebox.showinfo('Load', 'Client database and formated-list are successfully loaded.')

        except Exception:
            messagebox.showerror('Error', traceback.format_exc())
        finally:
            self.mlvStatusLabelUpdate()


    @staticmethod
    def convertTrvToDictMlvCati(trv):
        dictCatiCols = dict()
        for row_id in trv.get_children():
            trvItem = trv.item(row_id)
            strMddName = trvItem['text']
            strDtype = trvItem['values'][0]
            strStt = trvItem['values'][1]
            strWidgetValues = trvItem['values'][2]
            strWidgetValues = re.sub(r'[A-Z|a-z0-9,.!_]+#', '', strWidgetValues)

            if strStt in ['Enable']:
                if strDtype in ['Num', 'Text', 'Date']:
                    dictCatiCols[strMddName] = {
                        'dataType': strDtype,
                        'reportColName': [strWidgetValues],
                    }
                elif strDtype in ['SA']:
                    lstWidgetValues = strWidgetValues.split('@')
                    lstToReplace = list()
                    lstVals = list()
                    for idx, val in enumerate(lstWidgetValues[1:]):
                        if idx % 2 == 0:
                            lstToReplace.append({val})
                        else:
                            try:
                                lstVals.append(float(val))
                            except Exception:
                                lstVals.append(val)
                    dictCatiCols[strMddName] = {
                        'dataType': strDtype,
                        'reportColName': [lstWidgetValues[0]],
                        'toReplace': lstToReplace,
                        'vals': lstVals,
                    }
                elif strDtype in ['MA']:
                    strMaColName = strWidgetValues.split('@')[0]
                    numCols = int(strWidgetValues.split('@')[1])
                    lstCols = [f'{strMaColName}{i}' for i in np.arange(1, numCols+1)]
                    dictCatiCols[strMddName] = {
                        'dataType': strDtype,
                        'reportColName': lstCols,
                    }

        return dictCatiCols


    def exportWeeklyReport(self, event=None):
        try:
            if self.isDataActive and self.mlvTrvClientDb.get_children() and self.mlvTrvChecklist.get_children():
                self.mlvStatusLabelUpdate(True, 'Exporting weekly report')
                startTime = time.time()
                dictCatiCols = self.convertTrvToDictMlvCati(self.mlvTrvChecklist)

                dfCati = self.dto.df.loc[:, dictCatiCols.keys()]
                dfCati.drop_duplicates(subset='Respondent.ID', inplace=True, keep='first')
                dfCati.replace(to_replace=[{}], value=[np.nan], inplace=True)

                lstNumType = list()
                lstDateType = list()
                lstDrop = list()
                lstReindexCols = list()
                dfCatiRowsCount = dfCati.shape[0]
                for key in dictCatiCols.keys():
                    if dictCatiCols[key]['dataType'] in ['Num']:
                        lstNumType.append(key)
                        #dfCati[dictCatiCols[key]['reportColName']] = dfCati[dictCatiCols[key]['reportColName']].apply(lambda x: float(x) if str(x) != '' else np.nan)

                    elif dictCatiCols[key]['dataType'] in ['Date']:
                        lstDateType.append(key)

                    if dictCatiCols[key]['dataType'] != 'MA':
                        if dictCatiCols[key]['dataType'] == 'SA':
                            dfCati[key].replace(to_replace=dictCatiCols[key]['toReplace'], value=dictCatiCols[key]['vals'], inplace=True)

                        dfCati.rename(columns={key: dictCatiCols[key]['reportColName'][0]}, inplace=True)
                        lstReindexCols.append(dictCatiCols[key]['reportColName'][0])

                    else:
                        lstReindexCols.append(key)
                        lstReindexCols.extend(dictCatiCols[key]['reportColName'])
                        lstNull = [[np.nan] * len(dictCatiCols[key]['reportColName'])] * dfCatiRowsCount
                        dfMA = pd.DataFrame(lstNull, columns=dictCatiCols[key]['reportColName'])
                        dfMA['Respondent.ID'] = dfCati['Respondent.ID']
                        dfCati = pd.merge(dfCati, dfMA, on='Respondent.ID', how='left')
                        lstDrop.append(key)

                dfCati = dfCati.reindex(columns=lstReindexCols)
                dfCati.insert(0, 'RID', dfCati['Respondent.ID'])
                dfCati['RID'] = dfCati['RID'].astype(int)

                for idx in dfCati.index:
                    for item in lstNumType:
                        valNum = dfCati.loc[idx, item]
                        if valNum == '':
                            valNum = np.nan
                        else:
                            valNum = float(valNum)
                        dfCati.loc[idx, item] = valNum

                    for item in lstDateType:
                        if dfCati.loc[idx, item]:
                            lstDate = dfCati.loc[idx, item].split('/')
                            dfCati.loc[idx, item] = f'{lstDate[1]}/{lstDate[0]}/{lstDate[2]}'

                    for key in dictCatiCols.keys():
                        if dictCatiCols[key]['dataType'] == 'MA':
                            if isinstance(dfCati.loc[idx, key], set):
                                for i, val in enumerate(dfCati.loc[idx, key]):
                                    dfCati.loc[idx, f"{dictCatiCols[key]['reportColName'][0][0:-1]}{i + 1}"] = int(val.replace('_', ''))

                dfCati.drop(lstDrop, inplace=True, axis=1)
                for item in lstDateType:
                    dfCati[item] = pd.to_datetime(dfCati[item])

                if 'DateInterView' in dfCati.columns.values.tolist():
                    for idx in dfCati.index:
                        if len(dfCati.loc[idx, 'DateInterView']) > 0:
                            lstDate = dfCati.loc[idx, 'DateInterView'].split('/')
                            dfCati.loc[idx, 'DateInterView'] = f'{lstDate[1]}/{lstDate[0]}/{lstDate[2]}'

                    dfCati['DateInterView'] = pd.to_datetime(dfCati['DateInterView'])

                self.dfClient['RID'] = self.dfClient['RID'].astype(int)

                if 'DUMMY_ID' in self.dfClient.columns.tolist():
                    self.dfClient['DUMMY_ID'] = self.dfClient['DUMMY_ID'].astype(str)
                else:
                    self.dfClient['Dummy ID'] = self.dfClient['Dummy ID'].astype(str)

                for col in self.dfClient.columns.tolist():
                    if '_DT' in col or 'Decision Date' in col or ' date' in col:
                        self.dfClient[col] = pd.to_datetime(self.dfClient[col])

                dfMerge = pd.merge(self.dfClient, dfCati, on='RID', how='left')

                a = dfMerge['Respondent.ID'].isnull().all()

                if dfMerge['Respondent.ID'].isnull().all():
                    messagebox.showerror('Export error', 'No record is processed.')
                else:
                    lstPhoneCols = list()
                    isDelRID = False
                    strPrjName = self.mlvMenuProjectSel.get()
                    weeklyRpName = self.mlvMenuProjectSel.get()

                    if strPrjName in ['KEVIN']:
                        lstPhoneCols = ['OTHER_PHONE', 'OTHER_PHONE2', 'OTHER_PHONE3']
                        isDelRID = True

                        dfMerge['WAVE'] = dfMerge['RID'].astype(str).str[0]
                        dfMerge['WAVE'] = dfMerge['WAVE'].astype(int)

                        strW, strM, strY = self.mlvGetWaveInfoFromID(strPrjName, dfMerge['RID'].iloc[-1])
                        weeklyRpName = f'VN NewPurchase-Agents tNPS Project_Weekly report - Week {strW} {strM} 20{strY} - {datetime.date.today():%d%m%Y}v1'

                    elif strPrjName in ['FIRST CLASS']:
                        lstPhoneCols = ['MOBILE_NUMBER', 'FIX_TELE_NUMBER', 'OTHER_PHONE', 'OTHER_PHONE2', 'OTHER_PHONE3']
                        isDelRID = True

                        dfMerge['WAVE'] = 'W' + dfMerge['RID'].astype(str).str[0] + '_' + dfMerge['RID'].astype(str).str[1:3] + '_' + dfMerge['RID'].astype(str).str[-6:-4]
                        dfMerge['WAVE'] = dfMerge['WAVE'].str.replace('_0', '_', regex=False)

                        strW, strM, strY = self.mlvGetWaveInfoFromID(strPrjName, dfMerge['RID'].iloc[-1])
                        weeklyRpName = f'FIRST CLASS - Weekly report - W{strW}M{int(strM)}_20{strY} - {datetime.date.today():%d%m%Y}v1'

                    elif strPrjName in ['NEWBIE']:
                        lstPhoneCols = ['MOBILE_NUMBER', 'FIX_TELE_NUMBER', 'OTHER_PHONE', 'OTHER_PHONE2', 'OTHER_PHONE3']
                        isDelRID = True

                        dfMerge['WAVE'] = 'W' + dfMerge['RID'].astype(str).str[-5] + '_' + dfMerge['RID'].astype(str).str[2:4] + '_' + dfMerge['RID'].astype(str).str[0:2]
                        dfMerge['WAVE'] = dfMerge['WAVE'].str.replace('_0', '_', regex=False)

                        strW, strM, strY = self.mlvGetWaveInfoFromID(strPrjName, dfMerge['RID'].iloc[-1])
                        weeklyRpName = f'2018262_NEWBIE - Weekly Topline M{strM}W{strW} - {calendar.month_abbr[int(strM)].upper()} 20{strY} - {datetime.date.today():%d%m%Y}v1'

                    elif strPrjName in ['NIECE']:
                        lstPhoneCols = ['Owner\'s Home phone', 'Owner\'s Other phone', 'Owner\'s Mobile phone']
                        isDelRID = False

                        dfMerge.insert(dfMerge.columns.get_loc('Sale Channel'), 'NewID', dfMerge['Respondent.ID'].values.tolist())
                        dfMerge.drop(['Respondent.ID'], axis=1, inplace=True)
                        dfMerge.rename(columns={'NewID': 'Respondent.ID'}, inplace=True)

                        strW, strM, strY = self.mlvGetWaveInfoFromID(strPrjName, dfMerge['RID'].iloc[-1])
                        weeklyRpName = f'Niece_Weekly report_W0{strW}_{strM} - {datetime.date.today():%d%m%Y}v1'

                    elif strPrjName in ['URANUS']:
                        lstPhoneCols = ['Phone 1', 'Phone 2', 'Phone 3', 'Phone 4']
                        isDelRID = True

                        dfMerge.insert(dfMerge.columns.get_loc('S0'), 'NewWeek', dfMerge['Week'].values.tolist())
                        dfMerge.drop(['Week'], axis=1, inplace=True)
                        dfMerge.rename(columns={'NewWeek': 'Week'}, inplace=True)

                        dfMerge.replace(to_replace='99-Don’t know/ Don’t experience', value='99', inplace=True)

                        strW, strM, strY = self.mlvGetWaveInfoFromID(strPrjName, dfMerge['Week'].iloc[-1])
                        weeklyRpName = f'VN Claim tNPS Project_Database URANUS - Week {strW} MMM - {datetime.date.today():%d%m%Y}v1'









                    ####

                    for col in lstPhoneCols:
                        dfMerge[col] = [((str(x).replace('.0', '') if str(x)[0] == '0' or str(x)[0:2] == '84' else '0' + str(x).replace('.0', '')) if str(x) != 'nan' and str(x) != '' else '') for x in dfMerge[col]]

                    if isDelRID:
                        dfMerge.drop(['RID', 'Respondent.ID'], axis=1, inplace=True)

                    excelWriter = pd.ExcelWriter(f'{self.mlvMetadataFile["path"]}/{weeklyRpName}.xlsx', engine='xlsxwriter', datetime_format='dd/mm/yyyy')
                    dfMerge.to_excel(excelWriter, sheet_name='Report', index=False)
                    excelWriter.save()

                    messagebox.showinfo('Export', 'Weekly report is successfully exported in %.4fs.' % (time.time() - startTime))

            else:
                messagebox.showerror('Export error', 'Make sure your metadata, client database and format list are available.')

        except PermissionError:
            messagebox.showerror('Error', 'Weekly report file is opening')
        except Exception:
            messagebox.showerror('Error', traceback.format_exc())
        finally:
            self.mlvStatusLabelUpdate()


    @staticmethod
    def mlvGetWaveInfoFromID(prjName, rid):
        rid, strW, strM, strY = str(rid), '', '', ''
        if prjName in ['KEVIN']:
            strW, strM, strY = rid[0], calendar.month_abbr[int(rid[1:3])].upper(), rid[3:5]
        elif prjName in ['FIRST CLASS']:
            strW, strM, strY = rid[0], rid[1:3], rid[-6:-4]
        elif prjName in ['NEWBIE']:
            strW, strM, strY = rid[-5], rid[2:4], rid[0:2]
        elif prjName in ['NIECE']:
            strW, strM, strY = rid[-5], rid[2:4], rid[0:2]
        elif prjName in ['URANUS']:
            strW, strM, strY = rid, 'NA', 'NA'

        return strW, strM, strY