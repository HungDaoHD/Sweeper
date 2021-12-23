import numpy as np
import pandas as pd
import win32com.client as w32
from class_Rotom import rotom
import helpinghand
import re


class ditto:

    def __init__(self, fileName, sqlWhere, lstInput):
        self.fileName = fileName
        self.sqlWhere = sqlWhere
        self.lstInput = lstInput
        self.df, self.dm, self.dictOutput, self.method = self.transform()


    def transform(self):
        constr = 'Provider=mrOleDB.Provider.2;Data Source=mrDataFileDsc;' \
                 f'Location={self.fileName}.ddf;Initial Catalog={self.fileName}.mdd;' \
                 'Mode=ReadWrite;Mr Init Category Names=1'
        conn = w32.Dispatch(r'ADODB.Connection')
        conn.Open(constr)
        adoRS = w32.Dispatch(r'ADODB.Recordset')
        adoRS.Open(f'SELECT * FROM VDATA WHERE {self.sqlWhere}' if self.sqlWhere else 'SELECT * FROM VDATA', conn, 1, 3)

        dm = dict()
        myDict = dict()

        if not adoRS.EOF:
            myRows = adoRS.GetRows()
            myRows = np.array(myRows)
            index = 0
            for fld in adoRS.Fields:
                fname = self.lowerCodeInFieldName(fld.Name)
                ftype = fld.Type
                myDict = self.toRowData(myDict, myRows[index], fname, ftype)
                dm = helpinghand.toDm(dm, fname, ftype, isNewVar=False)
                index += 1

        adoRS.Close()
        conn.Close()

        df = pd.DataFrame(myDict)
        lst = list()
        mth = list()
        if not df.empty:
            df, dm = self.dropAvaiableCols(df, dm)
            df, dm, lst, mth = rotom(df, dm, self.lstInput).convert()
        return df, dm, lst, mth


    @staticmethod
    def lowerCodeInFieldName(fname):
        if '{' in fname and '.' in fname:
            lst = fname.split('.')
            for i in np.arange(len(lst)):
                if '{' in lst[i]:
                    strReplace = (re.findall(r'\[{+[A-Z|a-z0-9_]+}]', lst[i])[0]).lower()
                    lst[i] = re.sub(r'\[{+[A-Z|a-z0-9_]+}]', strReplace, lst[i])
            fname = '.'.join(lst)
        return fname


    @staticmethod
    def toRowData(myDict, rawRow, dName, dType):
        row = list()
        for r in rawRow:
            if dType == 7:  # datetime
                if str(r) == 'None':
                    r = np.nan
                else:
                    r = str(r)
            elif dType == 200:  # cats
                if str(r) == 'None':
                    r = {}
                else:
                    r = set(str(r).replace('{', '').replace('}', '').split(','))
            elif dType == 202:  # text
                if str(r) == 'None':
                    r = ''
                else:
                    r = str(r)
            elif dType == 3:  # long
                if str(r) == 'None':
                    r = np.nan
                else:
                    r = int(r)
            elif dType == 5:  # double
                if str(r) == 'None':
                    r = np.nan
                else:
                    r = float(r)
            else:
                if str(r) == 'None':
                    r = np.nan
            row.append(r)
        myDict[dName] = row
        return myDict


    @staticmethod
    def dropAvaiableCols(df, dm):
        lstDropDms = ['Respondent.Serial', 'Respondent.Serial.SourceFile', 'Respondent.Origin', 'Respondent.Origin.Other',
                   'DataCollection.Status', 'DataCollection.InterviewerID', 'DataCollection.StartTime',
                   'DataCollection.FinishTime', 'DataCollection.MetadataVersionNumber',
                   'DataCollection.MetadataVersionGUID', 'DataCollection.RoutingContext', 'DataCollection.Variant',
                   'DataCollection.EndQuestion', 'DataCollection.TerminateSignal', 'DataCollection.SeedValue',
                   'DataCollection.InterviewEngine', 'DataCollection.CurrentPage', 'DataCollection.Debug',
                   'DataCollection.ServerTimeZone', 'DataCollection.InterviewerTimeZone',
                   'DataCollection.RespondentTimeZone', 'DataCollection.BatchID', 'DataCollection.BatchName',
                   'DataCollection.DataEntryMode', 'DataCollection.Removed', 'DataCleaning.Note', 'DataCleaning.Status',
                   'DataCleaning.ReviewStatus', 'Comp', 'Version', 'ScreeningTable', 'Language', 'RANSEED', 'Thanks',
                   'AscribeFlag', 'CleanFlag', 'Wave', 'ELAPSEDTIME', 'ReportEventFilter', '_Interview_Year',
                   '_STARTDATE', '_STARTTIME', '_ENDDATE', '_ENDTIME', '_SPANTIME', '_TOTALTIME', '_TIMEOUTCOUNT',
                   '_RESTARTCOUNT', '_ProjectName', '_ProjectType', '_ImageName', '_Language', '_Area',
                   '_ResDistricts', '_ResWards', '_ResAddressOther', '_Sampling', '_Sampling._97', '_Sample']

        lstDropIf = ['System_LocationID', 'NWB_STATUS', 'NWB_LAST_SAVE_ON_SERVER', 'NWB_LAST_SUBMIT',
                         'NWB_CANCEL_REASON', 'NWB_CANCEL_REASON.ZZZ', 'SHELL_QFA', 'SHELL_QFB', 'SHELL_QFC', 'SHELL_QFD',
                         'SHELL_QFE', 'SHELL_QFF', 'System_Date', 'System_TimeIn', 'System_TimeOut', 'SHELL_START_DATE',
                         'SHELL_START_TIME', 'SHELL_INT_LENGTH', 'SHELL_BLOCK.SHELL_APPLICATION_ID',
                         'SHELL_BLOCK.SHELL_INTERVIEWER_LOGIN', 'SHELL_BLOCK.SHELL_SCH1', 'SHELL_BLOCK.SHELL_SCH2',
                         'SHELL_BLOCK.SHELL_SCH3', 'SHELL_BLOCK.SHELL_GEOLOCATION_OUTCOME',
                         'SHELL_BLOCK.SHELL_GEOLOCATION_LATITUDE', 'SHELL_BLOCK.SHELL_GEOLOCATION_LONGITUDE',
                         'SHELL_BLOCK.SHELL_GEOLOCATION_ACCURACY', 'SHELL_BLOCK.SHELL_GEOLOCATION_TIMESTAMP',
                         'SHELL_CHAINID', 'SHELL_COUNTRY', 'SHELL_LANGUAGE', 'SHELL_INTRO_GDPR',
                         'SHELL_RECORDING_CONFIRMATION', 'SHELL_GENDER', 'SHELL_AGE', 'SHELL_AGE._A1',
                         'SHELL_AGE_RECODED', '_ProjectName', '_ResName',
                       '_Area', '_ResAddress', '_ResHouseNo', '_ResStreet', '_ResDistricts',
                       '_ResDistrictSelected', '_ResWards', '_ResWardSelected', '_ResPhone', '_ResPhone._1',
                       '_ResCellPhone', '_ResCellPhone._1', '_Email', '_Email._1', '_IntID', '_IntName', '_ENDDATE',
                       '_ENDTIME', '_SPANTIME', '_TOTALTIME', 'SHELL_DDG_STATUS', 'SHELL_NAME',
                       'SHELL_BLOCK_TEL.SHELL_HOMETEL', 'SHELL_BLOCK_TEL.SHELL_MOBTEL', 'SHELL_TEL',
                       'SHELL_BLOCK_ADDRESS.SHELL_HOUSENO', 'SHELL_BLOCK_ADDRESS.SHELL_STREET',
                       'SHELL_BLOCK_ADDRESS.SHELL_DISTRICT', 'SHELL_BLOCK_ADDRESS.SHELL_TOWN',
                       'SHELL_BLOCK_ADDRESS.SHELL_ZIP', 'SHELL_ADDRESS', 'SHELL_BLOCK_EMAIL.SHELL_IIS_PANEL',
                       'SHELL_BLOCK_EMAIL.SHELL_EMAIL', 'SHELL_BLOCK_EMAIL.SHELL_EMAIL_DUMMY', '_BHP', 'SHELL_SUP']
        try:
            df['ID'] = df['ID'].astype(int)
            df = df.set_index('ID')
            lstDrop = lstDropDms
        except KeyError:
            df['InstanceID'] = df['InstanceID'].astype(int)
            df = df.set_index('InstanceID')
            lstDrop = lstDropIf
        dfDrop = df.drop(columns=list(df.columns.intersection(lstDrop).values))
        for k in lstDrop:
            try:
                dm.pop(k)
            except Exception:
                pass
        return dfDrop, dm


    def countSample(self):
        dfSample = self.df['_LoaiPhieu'].copy().to_frame()
        dictSample = {
            'Total': dfSample.shape[0],
            'Main': dfSample[dfSample['_LoaiPhieu'] == {'_1'}].shape[0],
            'Booster': dfSample[dfSample['_LoaiPhieu'] == {'_5'}].shape[0],
            'Extra': dfSample[dfSample['_LoaiPhieu'] == {'_2'}].shape[0],
            'Cancel': dfSample[dfSample['_LoaiPhieu'] == {'_3'}].shape[0],
            'Non': dfSample[dfSample['_LoaiPhieu'] == {'_6'}].shape[0],
            'Uncompleted': dfSample[dfSample['_LoaiPhieu'] == {'_4'}].shape[0],
        }
        return dictSample