import re
import numpy as np
from pandas.core.common import flatten
import datetime
import helpinghand as hp



class hurricane:

    def __init__(self, df, dm, dictCheck):
        self.df = df
        self.dm = dm
        self.dictCheck = dictCheck
        self.method = ['askedall', 'yearsubtract', 'catfromnum', 'catfromcats', 'lsm2', 'sum', 'allin', 'containsany',
                       'notequal', 'equal', 'when', 'iterfilby', 'logic']

    def sweep(self):
        strSummary = str()
        strDetail = str()

        for mth in self.dictCheck.keys():
            if mth in ['notequal']:
                lstChecked = getattr(self, 'equal')(self.dictCheck[mth], False)
            elif mth in ['equal']:
                lstChecked = getattr(self, 'equal')(self.dictCheck[mth], True)
            else:
                lstChecked = getattr(self, mth)(self.dictCheck[mth])
            strSummary += lstChecked[0]
            strDetail += lstChecked[1]

        return strSummary, strDetail


    def askedall(self, lstCheck):
        strSummary = str()
        strDetail = str()
        lstFlat = list(flatten(lstCheck))
        dfCheck = self.df.loc[:, lstFlat].copy()
        dfCheck.replace(to_replace=[{}], value=np.nan, inplace=True)
        dfCheck.replace(to_replace=[''], value=np.nan, inplace=True)
        nullCols = dfCheck.columns[dfCheck.isnull().any()]
        dfCheck = dfCheck[dfCheck.isnull().any(axis=1)][nullCols]
        if not dfCheck.empty:
            strSummary = 'Asked all question: {} is Null\n'.format(nullCols.values)
            strDetail = ''
            for col in dfCheck.columns:
                sr = dfCheck.loc[dfCheck[col].isnull(), col]
                sr.replace(to_replace=np.nan, value='{} value missing'.format(col), inplace=True)
                strDetail += sr.to_string() + '\n'
        return strSummary, strDetail


    def yearsubtract(self, lstCheck):
        strSummary = str()
        strDetail = str()
        now = datetime.datetime.now()
        for qreNum, qreYear in lstCheck:
            dfCheck = self.df.loc[:, [qreNum, qreYear]].copy()
            dfCheck['checkValue'] = now.year - dfCheck[qreYear]
            dfCheck = dfCheck.loc[(dfCheck['checkValue'] != dfCheck[qreNum])]
            if not dfCheck.empty:
                strSummary += 'Year Subtract question: {} is not correct\n'.format([qreNum, qreYear])
                dfCheck['yearsubtract'] = ['{} - {}({}) = {}'.format(now.year, qreYear, a, now.year - a) for a in
                                                  dfCheck[qreYear]]
                dfCheck.drop([qreYear, 'checkValue'], axis='columns', inplace=True)
                strDetail += dfCheck.to_string() + '\n'
        return strSummary, strDetail


    def catfromnum(self, lstCheck):
        strSummary = str()
        strDetail = str()
        for qreCat, qreNum, strRecode in lstCheck:
            dfCheck = self.df.loc[:, [qreCat, qreNum]].copy()
            dfCheck.replace(to_replace=np.nan, value=-999999, inplace=True)
            dfCheck['recode'] = self.recodeCatFromNum(dfCheck[qreNum], strRecode)

            dfCheck['checkValue'] = [(len(a) > 0 and hp.iscontainsany(a, b))
                                     or (len(a) == 0 and len(b) == 0)
                                     for a, b in zip(dfCheck[qreCat], dfCheck['recode'])]

            dfCheck = dfCheck.loc[~(dfCheck['checkValue'])]
            dfCheck.replace(to_replace=-999999, value=np.nan, inplace=True)
            if not dfCheck.empty:
                strSummary += 'Category from number question: {} is not correct\n'.format([qreCat, qreNum, strRecode])
                dfCheck['catfromnum'] = ['{}({}) => {}'.format(qreNum, a, b).replace('\'', '') for a, b in
                                                zip(dfCheck[qreNum], dfCheck['recode'])]
                dfCheck.drop([qreNum, 'recode', 'checkValue'], axis='columns', inplace=True)
                strDetail += dfCheck.to_string() + '\n'
        return strSummary, strDetail


    @staticmethod
    def recodeCatFromNum(dfNum, strRe):
        lst = list()
        lstRecode = strRe.split('|')
        for x in dfNum:
            lstx = list()
            if x == -999999:
                lstx.append({})
            else:
                for l in lstRecode:
                    y1, y2 = l.split('=')
                    y2 = y2.replace('to', ' <= x <= ').replace('over', 'x > ').replace('under', 'x < ')
                    if not 'x' in y2:
                        y2 = 'x == ' + y2
                    y1 = y1.replace('{', '').replace('}', '')
                    if eval(y2):
                        lstx.append({y1})
            if lstx:
                lst.extend(lstx)
            else:
                lst.append({'outOfRange'})
        return lst


    def catfromcats(self, lstCheck):
        strSummary = str()
        strDetail = str()
        for qre1, qre2, strRecode in lstCheck:
            dfCheck = self.df.loc[:, [qre1, qre2]].copy()
            dfCheck.replace(to_replace=[{}], value=[set({})], inplace=True)
            dfCheck['recode'] = self.recodeCatFromCats(dfCheck[qre2], strRecode)
            dfCheck['checkValue'] = [len(a) > 0 and hp.iscontainsany(a, b) for a, b in zip(dfCheck[qre1], dfCheck['recode'])]
            dfCheck = dfCheck.loc[~(dfCheck['checkValue'])]
            if not dfCheck.empty:
                strSummary += 'Category from categories question: {} is not correct\n'.format([qre1, qre2, strRecode])
                dfCheck['catfromcats'] = ['{}({}) => {}'.format(qre2, a, b).replace('\'', '') for a, b in
                                         zip(dfCheck[qre2], dfCheck['recode'])]
                dfCheck.drop([qre2, 'recode', 'checkValue'], axis='columns', inplace=True)
                strDetail += dfCheck.to_string() + '\n'
        return strSummary, strDetail


    @staticmethod
    def recodeCatFromCats(dfCat, strRe):
        lst = list()
        lstRecode = strRe.replace('{', '').replace('}', '').split('|')
        for x in dfCat:
            lstx = list()
            if len(x) == 0:
                lstx.append({})
            else:
                for l in lstRecode:
                    y1, y2 = l.split('=')
                    y2 = set(y2.split(','))
                    if len(x.intersection(y2)) > 0:
                        lstx.append({y1})
                        isExist = True
            if lstx:
                lst.extend(lstx)
            else:
                lst.append({'outOfRange'})
        return lst


    def lsm2(self, lstCheck):
        strSummary = str()
        strDetail = str()
        for qre in lstCheck:
            dfCheck = self.df.loc[:, ['_LSM2_1', '_LSM2_2', qre[0]]].copy()
            dfCheck['recode'] = hp.lsmRecode(dfCheck['_LSM2_1'].values.tolist(), dfCheck['_LSM2_2'].values.tolist())
            dfCheck['checkValue'] = [len(a) > 0 and hp.iscontainsany(a, b) for a, b in
                                     zip(dfCheck[qre[0]].values.tolist(), dfCheck['recode'].values.tolist())]
            dfCheck = dfCheck.loc[~(dfCheck['checkValue'])]
            if not dfCheck.empty:
                strSummary += 'Lsm question: {} is not correct\n'.format(qre)
                dfCheck['lsm2'] = ['{}({}) + {}({}) => {}'.format('_LSM2_1', a, '_LSM2_2', b, c).replace('\'', '')
                                   for a, b, c in zip(dfCheck['_LSM2_1'], dfCheck['_LSM2_2'], dfCheck['recode'])]
                dfCheck.drop(['_LSM2_1', '_LSM2_2', 'recode', 'checkValue'], axis='columns', inplace=True)
                strDetail += dfCheck.to_string() + '\n'
        return strSummary, strDetail


    def sum(self, lstCheck):
        strSummary = str()
        strDetail = str()
        for qreSum, qresToSum in lstCheck:
            lstQresToSum = qresToSum.split('|')
            lstToLoc = [qreSum]
            lstToLoc.extend(lstQresToSum)
            try:
                dfCheck = self.df.loc[:, lstToLoc].copy()
            except KeyError as keyErr:
                dfCheck = self.df.loc[:, lstQresToSum].copy()
                dfCheck[qreSum] = [int(qreSum.replace('num', ''))] * dfCheck.shape[0]
            dfCheck['checkValue'] = [-999999] * dfCheck.shape[0]
            dfCheck['sum'] = '' * dfCheck.shape[0]
            dfCheck.replace(to_replace=np.nan, value=-999999, inplace=True)
            for x in lstQresToSum:
                strErr = ''
                for idx in dfCheck.index:
                    if dfCheck.loc[idx, x] != -999999:
                        if dfCheck.loc[idx, 'checkValue'] == -999999:
                            dfCheck.loc[idx, 'checkValue'] = 0
                        dfCheck.loc[idx, 'checkValue'] += dfCheck.loc[idx, x]
                        dfCheck.loc[idx, 'sum'] += '{}({}) + '.format(x, dfCheck.loc[idx, x].astype(str))
            dfCheck = dfCheck.loc[((dfCheck[qreSum] != dfCheck['checkValue']) & (dfCheck['checkValue'] != -999999))]
            dfCheck.replace(to_replace=-999999, value=np.nan, inplace=True)
            if not dfCheck.empty:
                strSummary += 'Sum question: {} is not correct\n'.format(qreSum)
                dfCheck['sum'] = dfCheck['sum'].str[0:-2] + '= ' + dfCheck['checkValue'].astype(str)
                lstQresToSum.append('checkValue')
                dfCheck.drop(lstQresToSum, axis='columns', inplace=True)
                strDetail += dfCheck.to_string() + '\n'
        return strSummary, strDetail


    def allin(self, lstCheck):
        strSummary = str()
        strDetail = str()
        for qreSub, qreAll, strExc in lstCheck:
            dfCheck = self.df.loc[:, [qreSub, qreAll]].copy()
            dfCheck.replace(to_replace=[{}], value=[set({})], inplace=True)
            setExc = set(strExc.replace('{', '').replace('}', '').split(','))
            dfCheck['checkValue'] = [a.issubset(b) or a.issubset(setExc) for a, b in zip(dfCheck[qreSub], dfCheck[qreAll])]
            dfCheck = dfCheck.loc[~(dfCheck['checkValue'])]
            if not dfCheck.empty:
                strSummary += 'Allin question: {} is not correct\n'.format([qreSub, qreAll])
                dfCheck['allin'] = ['{} NOT allin {}'.format(qreSub, qreAll)] * dfCheck.shape[0]
                dfCheck.drop('checkValue', axis='columns', inplace=True)
                strDetail += dfCheck.to_string() + '\n'
        return strSummary, strDetail


    def containsany(self, lstCheck):
        strSummary = str()
        strDetail = str()
        for qre1, qre2 in lstCheck:
            try:
                dfCheck = self.df.loc[:, [qre1, qre2]].copy()
            except KeyError:
                lstval = qre2.replace('{', '').replace('}', '').replace('~', '').split(',')
                qre2temp = [set(lstval)] * self.df.shape[0]
                dfCheck = self.df.loc[:, [qre1]].copy()
                dfCheck[qre2] = qre2temp
            dfCheck.replace(to_replace=[{}], value=[set({})], inplace=True)
            if '~' in qre2:
                dfCheck['checkValue'] = [len(a) > 0 and len(a.intersection(b)) == 0 for a, b in
                                         zip(dfCheck[qre1], dfCheck[qre2])]
            else:
                dfCheck['checkValue'] = [not (len(a) > 0 and len(a.intersection(b)) == 0) for a, b in
                                        zip(dfCheck[qre1], dfCheck[qre2])]
            dfCheck = dfCheck.loc[~(dfCheck['checkValue'])]
            if not dfCheck.empty:
                strSummary += 'Contains any question: {} is not correct\n'.format([qre1, qre2])
                if '~' in qre2:
                    dfCheck['containsany'] = ['{} containsany {}'.format(qre1, qre2.replace('~', ''))] * dfCheck.shape[0]
                else:
                    dfCheck['containsany'] = ['{} NOT containsany {}'.format(qre1, qre2)] * dfCheck.shape[0]
                dfCheck.drop('checkValue', axis='columns', inplace=True)
                strDetail += dfCheck.to_string() + '\n'
        return strSummary, strDetail


    def equal(self, lstCheck, isequal):
        strSummary = str()
        strDetail = str()
        for qre1, qre2 in lstCheck:
            dfCheck = self.df.loc[:, [qre1, qre2]].copy()
            dfCheck.replace(to_replace=[{}], value=[set({})], inplace=True)
            dfCheck.replace(to_replace=[np.nan], value=[0], inplace=True)
            if isequal:
                if dfCheck.dtypes[qre1] in [np.int32, np.int64, np.float]:
                    dfCheck['checkValue'] = [a == b for a, b in zip(dfCheck[qre1], dfCheck[qre2])]
                else:
                    dfCheck['checkValue'] = [len(a.difference(b)) == 0 and len(b.difference(a)) == 0 for a, b in
                                             zip(dfCheck[qre1], dfCheck[qre2])]
                strErr = 'Equal'

            else:
                if dfCheck.dtypes[qre1] in [np.int32, np.int64, np.float]:
                    dfCheck['checkValue'] = [a != b for a, b in zip(dfCheck[qre1], dfCheck[qre2])]
                else:
                    dfCheck['checkValue'] = [not (hp.iscontainsany(a, b) or hp.iscontainsany(b, a)) for a, b in
                                             zip(dfCheck[qre1], dfCheck[qre2])]
                strErr = 'Not Equal'

            dfCheck = dfCheck.loc[~(dfCheck['checkValue'])]

            if not dfCheck.empty:
                strSummary += '{} question: {} is not correct\n'.format(strErr, [qre1, qre2])
                strErrFormat = 'Not {}'.format(strErr) if isequal else strErr.replace('Not ', '')
                dfCheck[strErr] = ['{} {} {}'.format(qre1, strErrFormat, qre2)] * dfCheck.shape[0]
                dfCheck.drop('checkValue', axis='columns', inplace=True)
                strDetail += dfCheck.to_string() + '\n'
        return strSummary, strDetail


    def when(self, lstCheck):
        strSummary = str()
        strDetail = str()

        for qre, qresCond, strCond in lstCheck:
            lstQresCond = qresCond.split('|')
            lstCatsCond = re.findall(r'{_[A-Z|a-z0-9,_><=!]+}', strCond)
            lstToLoc = [qre]
            lstToLoc.extend(lstQresCond)
            lstToLoc = list(dict.fromkeys(lstToLoc))
            dfCheck = self.df.loc[:, lstToLoc].copy()
            qreType = dfCheck.dtypes[lstToLoc[0]]
            dfCheck.replace(to_replace=[{}], value=[set({})], inplace=True)
            if qreType == np.float or qreType == np.int:
                # dfCheck.replace(to_replace=[np.nan], value=[''], inplace=True)
                dfCheck[lstToLoc[0]].replace(to_replace=[np.nan], value=[''], inplace=True)
                dfCheck = dfCheck.astype({lstToLoc[0]: str})
            else:
                # dfCheck.replace(to_replace=[np.nan], value=[set({})], inplace=True)
                dfCheck[lstToLoc[0]].replace(to_replace=[np.nan], value=[set({})], inplace=True)
            strCondIters = re.sub(r'{_[A-Z|a-z0-9,_><=!]+}', '{xxxx}', strCond)
            strIters = str()
            strZip = str()
            for i in np.arange(len(lstQresCond)):
                strIter = 'a' + str(i)
                strIters += strIter + ', '
                strZip += "dfCheck['" + lstQresCond[i] + "'], "
                if 'num' in lstCatsCond[i]:
                    lstQresCond[i] = strIter + " " + lstCatsCond[i].replace("{_num", "").replace("}", "")
                elif 'isnull' in lstCatsCond[i].lower():
                    lstQresCond[i] = "len(" + strIter + ") == 0"
                elif 'notnull' in lstCatsCond[i].lower():
                    lstQresCond[i] = "len(" + strIter + ") > 0"
                else:
                    lstQresCond[i] = "hp.iscontainsany(" + strIter + ", {'" + lstCatsCond[i].replace(",", r"','") + "'})"
                strCondIters = re.sub('{xxxx}', lstQresCond[i].replace(r"'{", "'").replace("}'", "'"), strCondIters, 1)
            strCondItersNull = "not (len(a) == 0 and (" + strCondIters.replace(r'&', ' and ').replace(r'|', ' or ').replace(r'~', ' not ') + "))"
            strCondItersNotNull = "not (len(a) != 0 and not (" + strCondIters.replace(r'&', ' and ').replace(r'|', ' or ').replace(r'~', ' not ') + "))"
            strIters = 'a, ' + strIters[:-2]
            strZip = "dfCheck['" + qre + "'], " + strZip[:-2]

            try:
                dfCheck['checkValueNull'] = eval("[(" + strCondItersNull + ") for " + strIters + " in zip(" + strZip + ")]")
            except TypeError as typeErr:
                strCondItersNull = strCondItersNull.replace('len(a) == 0', 'len(str(a)) == 0')
                strCondItersNotNull = strCondItersNotNull.replace('len(a) != 0', 'len(str(a)) != 0')

            dfCheck['checkValueNull'] = eval("[(" + strCondItersNull + ") for " + strIters + " in zip(" + strZip + ")]")
            dfCheck['checkValueNotNull'] = eval("[(" + strCondItersNotNull + ") for " + strIters + " in zip(" + strZip + ")]")

            dfCheck = dfCheck.loc[~(dfCheck['checkValueNull']) | ~(dfCheck['checkValueNotNull'])]
            if not dfCheck.empty:
                strSummary += 'Condition question: {} is not correct\n'.format(lstToLoc)
                dfCheck = dfCheck.copy()
                dfCheck['checkValueNull'].replace({False: '{} should NOT be NULL.'.format(qre), True: ''}, inplace=True)
                dfCheck['checkValueNotNull'].replace({False: '{} should be NULL.'.format(qre), True: ''}, inplace=True)
                dfCheck['when'] = dfCheck['checkValueNull'].astype(str) + dfCheck['checkValueNotNull'].astype(str)
                dfCheck.drop(['checkValueNull', 'checkValueNotNull'], axis='columns', inplace=True)
                strDetail += dfCheck.to_string() + '\n'
        return strSummary, strDetail


    def iterfilby(self, lstCheck):
        strSummary = str()
        strDetail = str()
        dfCheck = self.df.loc[:].copy()
        dfCheck.replace(to_replace=[''], value=[set({})], inplace=True)
        dfCheck.replace(to_replace=[{}], value=[set({})], inplace=True)
        dfCheck.replace(to_replace=[np.nan], value=[set({})], inplace=True)
        for qreGrid, qreFil, iters in lstCheck:
            lstCheckNull = list()
            lstLblNull = list()
            lstCheckNotNull = list()
            lstLblNotNull = list()
            setIters = set(iters)
            for idx in dfCheck.index:
                dfIdxCheck = dfCheck.loc[idx]
                lstCheckValNull = list()
                strLblValNull = ''
                lstCheckValNotNull = list()
                strLblValNotNull = ''
                val = list()
                if isinstance(dfIdxCheck[qreFil], (np.int32, np.int64, np.float)):
                    val.extend('_' + str(int(i)) for i in np.arange(1, dfIdxCheck[qreFil] + 1))
                    val = set(val)
                else:
                    val = dfIdxCheck[qreFil]

                if len(val) > 0:
                    itersMustBeNull = setIters.difference(val)
                    val = val.difference({'_98', '_99', '_998', '_999'})
                    for ans in val:
                        qreGridReplace = qreGrid.replace('..', '{' + str(ans.lower()) + '}')
                        if dfIdxCheck[qreGridReplace] == set({}):
                            lstCheckValNull.extend([False])
                            strLblValNull += qreGridReplace + ','
                        else:
                            lstCheckValNull.extend([True])
                else:
                    itersMustBeNull = setIters

                for ans in itersMustBeNull:
                    qreGridReplace = qreGrid.replace('..', '{' + str(ans.lower()) + '}')
                    if dfIdxCheck[qreGridReplace] != set({}):
                        lstCheckValNotNull.extend([False])
                        strLblValNotNull += qreGridReplace + ','
                    else:
                        lstCheckValNotNull.extend([True])

                lstCheckNull.append(all(lstCheckValNull))
                lstLblNull.append(strLblValNull[0:-1])

                lstCheckNotNull.append(all(lstCheckValNotNull))
                lstLblNotNull.append(strLblValNotNull[0:-1])

            dfCheck['checkValueNull'] = lstCheckNull
            dfCheck['checkLabelNull'] = lstLblNull

            dfCheck['checkValueNotNull'] = lstCheckNotNull
            dfCheck['checkLabelNotNull'] = lstLblNotNull

            dfErr = dfCheck.loc[~(dfCheck['checkValueNull']) | ~(dfCheck['checkValueNotNull']),
                                [qreFil, 'checkLabelNull', 'checkValueNull', 'checkLabelNotNull', 'checkValueNotNull']]

            if not dfErr.empty:
                strSummary += 'Iterations filter question: {} is not correct\n'.format([qreGrid, qreFil])

                dfErr['checkValueNull'].replace({False: 'Should NOT be NULL.', True: np.nan}, inplace=True)
                dfErr['checkValueNotNull'].replace({False: 'Should be NULL.', True: np.nan}, inplace=True)
                dfErr['ErrorVars'] = dfErr[['checkLabelNull', 'checkLabelNotNull']].values.tolist()
                dfErr['ErrorType'] = dfErr[['checkValueNull', 'checkValueNotNull']].values.tolist()
                dfErr = dfErr.explode(['ErrorType', 'ErrorVars'])
                dfErr = dfErr.loc[dfErr['ErrorType'].notnull(), [qreFil, 'ErrorVars', 'ErrorType']]
                dfErr['ErrorVars'] = dfErr['ErrorVars'].str.split(',')
                dfErr = dfErr.explode(['ErrorVars'])
                dfErr.rename({qreFil: 'iterfilby {}'.format(qreFil)}, axis=1, inplace=True)
                strDetail += dfErr.to_string() + '\n'
        return strSummary, strDetail


    def logic(self, lstCheck):
        strSummary = str()
        strDetail = str()
        for qre, qresCond, strCond in lstCheck:
            lstQresCond = [qre]
            lstQresCond.extend(qresCond.split('|'))
            lstCatsCond = re.findall(r'{_[A-Z|a-z0-9,_><=!]+}', strCond)
            lstUnique = lstQresCond.copy()
            lstUnique = list(dict.fromkeys(lstUnique))
            dfCheck = self.df.loc[:, lstUnique].copy()
            dfCheck.replace(to_replace=[{}], value=[set({})], inplace=True)
            strCondIters = re.sub(r'{_[A-Z|a-z0-9,_><=!]+}', '{xxxx}', strCond)
            strIters = str()
            strZip = str()
            for i in np.arange(len(lstQresCond)):
                strIter = 'a{}'.format(i)
                strIters += '{}, '.format(strIter)
                if lstQresCond[i] in strZip:
                    dfCheck[strIter] = dfCheck[lstQresCond[i]]
                    strZip += "dfCheck['{}'], ".format(strIter)
                else:
                    strZip += "dfCheck['{}'], ".format(lstQresCond[i])
                if 'num' in lstCatsCond[i].lower():
                    lstQresCond[i] = '{} {}'.format(strIter, lstCatsCond[i].replace("{_num", "").replace("}", ""))
                elif 'isnull' in lstCatsCond[i].lower():
                    lstQresCond[i] = 'len({}) == 0'.format(strIter)
                elif 'notnull' in lstCatsCond[i].lower():
                    lstQresCond[i] = 'len({}) > 0'.format(strIter)
                else:
                    lstQresCond[i] = "hp.iscontainsany(" + strIter + ", {'" + lstCatsCond[i].replace(",", r"','") + "'})"
                strCondIters = re.sub('{xxxx}', lstQresCond[i].replace(r"'{", "'").replace("}'", "'"), strCondIters, 1)
            strCondItersTrue = "not (len(a0) > 0 and (" + strCondIters.replace(r'&', ' and ').replace(r'|', ' or ').replace(r'~', ' not ') + "))"
            dfCheck['checkValue'] = eval("[(" + strCondItersTrue + ") for " + strIters + " in zip(" + strZip + ")]")
            dfCheck = dfCheck.loc[~(dfCheck['checkValue'])]
            if not dfCheck.empty:
                dfCheck = dfCheck.copy()
                strSummary += 'Logic question: {} is not correct\n'.format([qre, qresCond])
                strPopup = (re.sub('.+and \(|\)$|hp\.iscontainsany|\'', '', strCondItersTrue)).replace(', ', '=')
                lstPopup = [qre]
                lstPopup.extend(qresCond.split('|'))
                for i in np.arange(len(lstPopup)):
                    strPopup = strPopup.replace('a{}'.format(i), lstPopup[i])
                dfCheck['logic'] = [strPopup] * dfCheck.shape[0]
                lstPopup.extend(['logic'])
                lstPopup = list(dict.fromkeys(lstPopup))
                dfCheck = dfCheck.loc[:, lstPopup]
                strDetail += dfCheck.to_string() + '\n'
        return strSummary, strDetail