import numpy as np
import re
import helpinghand as hp


class rotom:

    def __init__(self, df, dm, lstInput):
        self.df = df
        self.dm = dm
        self.lstInput = lstInput
        self.dictOutput = dict()
        self.method = ['merge', 'assign', 'count', 'difference', 'intersection', 'getiters', 'numcompared', 'dropped',
                       'getminnumber', 'getmaxnumber', 'getvaluesbyiters', 'getsum']


    def convert(self):
        lstAddin = list()
        lstOutput = list()
        for lst in self.lstInput:
            if lst[1].lower() in self.method:
                # lstAddin.append(lst)
                dictAddin = self.convertOutputDict([lst])
                if 'merge' in dictAddin.keys():
                    self.df, self.dm = self.toMerge(dictAddin['merge'])
                if 'getiters' in dictAddin.keys():
                    self.df, self.dm = self.toGetIters(dictAddin['getiters'])
                if 'numcompared' in dictAddin.keys():
                    self.df, self.dm = self.toNumCompared(dictAddin['numcompared'])
                if 'assign' in dictAddin.keys():
                    self.df, self.dm = self.toAssign(dictAddin['assign'], True)
                if 'dropped' in dictAddin.keys():
                    self.df, self.dm = self.toAssign(dictAddin['dropped'], False)
                if 'difference' in dictAddin.keys():
                    self.df, self.dm = self.toDiffInter(dictAddin['difference'], 'diff')
                if 'intersection' in dictAddin.keys():
                    self.df, self.dm = self.toDiffInter(dictAddin['intersection'], 'inter')
                if 'count' in dictAddin.keys():
                    self.df, self.dm = self.toCount(dictAddin['count'])
                if 'getminnumber' in dictAddin.keys():
                    self.df, self.dm = self.toGetMinMaxNum(dictAddin['getminnumber'], True)
                if 'getmaxnumber' in dictAddin.keys():
                    self.df, self.dm = self.toGetMinMaxNum(dictAddin['getmaxnumber'], False)
                if 'getvaluesbyiters' in dictAddin.keys():
                    self.df, self.dm = self.toGetValsByIters(dictAddin['getvaluesbyiters'])
                if 'getsum' in dictAddin.keys():
                    self.df, self.dm = self.toGetSum(dictAddin['getsum'])
            else:
                lstOutput.append(lst)

        self.dictOutput = self.convertOutputDict(lstOutput)
        return self.df, self.dm, self.dictOutput, self.method


    def convertOutputDict(self, lstInput):
        dictMethod = dict()
        for lst in lstInput:
            lstrex1 = re.findall(r'\[..]\.', lst[0])
            if len(lstrex1) == 0:
                strNew = str()
                if len(lst) > 2:
                    for var in lst[2].split('|'):
                        if '[..]' in var:
                            strNew += '|'.join(self.getListGridVarsByStr(self.dm, [var])) + '|'
                        else:
                            strNew += var + '|'
                    lst[2] = strNew[0:-1]

                strMethod = lst[1].lower()
                lstMethod = [lst[i] for i in np.arange(len(lst)) if i != 1]
                if strMethod in dictMethod.keys():
                    dictMethod[strMethod].append(lstMethod)
                else:
                    dictMethod[strMethod] = [lstMethod]

            else:
                strRex = r'.[A-Z|a-z0-9_]+\[\{+[A-Z|a-z0-9_]+\}\]'
                if len(re.findall(strRex, lst[0])) > 0:
                    strGridName = re.sub(strRex, '', lst[0])
                else:
                    strGridName = lst[0]
                lstGridName = strGridName.replace('].', ']|.').split('|.')
                del lstGridName[len(lstGridName)-1]
                strGridName = '.'.join(lstGridName)

                lstGridVars = self.getListGridVarsByStr(self.dm, [strGridName])

                for var in lstGridVars:
                    lstTmp = lst.copy()
                    lstTmp[0] = lstTmp[0].replace(strGridName, str(var))
                    strNew = str()

                    if len(lstTmp) > 2:
                        for vartoMerge in lstTmp[2].split('|'):
                            if '[..]' in vartoMerge:
                                strNew += '|'.join(self.getListGridVarsByStr(self.dm, [str(var), vartoMerge])) + '|'
                            else:
                                strNew += vartoMerge + '|'
                        lstTmp[2] = strNew[0:-1]

                    strMethod = lstTmp[1].lower()
                    lstMethod = [lstTmp[i] for i in np.arange(len(lstTmp)) if i != 1]
                    if strMethod in dictMethod.keys():
                        dictMethod[strMethod].append(lstMethod)
                    else:
                        dictMethod[strMethod] = [lstMethod]

        if 'iterfilby' in dictMethod.keys():
            dictMethod['iterfilby'] = self.formatIterationFilter(dictMethod['iterfilby'])

        return dictMethod


    @staticmethod
    def getListGridVarsByStr(dm, lstVarsInput):
        strRex = r'[A-Z|a-z0-9_]+\[\{+[A-Z|a-z0-9_]+\}\]'
        if len(lstVarsInput) == 1:
            varName = ''
            strVarInput = lstVarsInput[0]
        else:
            varName = lstVarsInput[0]
            strVarInput = lstVarsInput[1]
        lstRex = re.findall(strRex, strVarInput)
        if len(lstRex) > 0:
            strVarInput = re.sub(r'\[{+[A-Z|a-z0-9_]+}]', '[..]', strVarInput)
        lstFullVars = eval("dm['" + "']['".join(strVarInput.replace('].', ']|.').split('|.')) + "']['mddVars']")
        lstVars = list()
        for var in lstFullVars:
            isAdd = True

            if len(varName) > 0:
                lstRexVarName = re.findall(r'\[{+[A-Z|a-z0-9_]+}]', varName)
                lstRexVar = re.findall(r'\[{+[A-Z|a-z0-9_]+}]', var)
                if len(lstRexVar) < len(lstRexVarName):
                    lstVarName = varName.replace('].', ']|.').split('|.')
                    for i in np.arange(len(lstRexVar) - len(lstRexVarName), 0):
                        del lstVarName[i]
                    varName = '.'.join(lstVarName)

                if len(lstRexVarName) == 1 and len(lstRexVar) == 1:
                    if not set(lstRexVarName).intersection(set(lstRexVar)):  # edit 06/10/2021
                        isAdd = False
                else:
                    if not varName in var:
                        isAdd = False

            if len(lstRex) > 0:
                for i in np.arange(len(lstRex)):
                    if not lstRex[i] in var:
                        isAdd = False
            if isAdd and not var in lstVars:
                lstVars.append(var)
        return lstVars


    @staticmethod
    def formatIterationFilter(lstIterFil):
        dictFormated = dict()
        for lst in lstIterFil:
            lstQreFil = re.findall(r'[A-Z|a-z0-9_]+\[{+[A-Z|a-z0-9_]+}]', lst[0])
            lstQreToFil = re.findall(r'[A-Z|a-z0-9_]+\[{+[A-Z|a-z0-9_]+}]', lst[1])
            lstIters = list()
            if len(lstQreFil) == len(lstQreToFil):
                strRe = re.sub(r'\[{+[A-Z|a-z0-9_]+}]', '[..]', lstQreFil[len(lstQreToFil) - 1])
                lstIters.extend(re.findall(r'\[{+[A-Z|a-z0-9_]+}]', lstQreFil[len(lstQreToFil) - 1]))
                strQreFormated = strRe.join(lst[0].rsplit(lstQreFil[len(lstQreToFil) - 1], 1))
            else:
                strRe = re.sub(r'\[{+[A-Z|a-z0-9_]+}]', '[..]', lstQreFil[len(lstQreToFil)])
                lstIters.extend(re.findall(r'\[{+[A-Z|a-z0-9_]+}]', lstQreFil[len(lstQreToFil)]))
                strQreFormated = strRe.join(lst[0].rsplit(lstQreFil[len(lstQreToFil)], 1))
            for i in np.arange(len(lstIters)):
                lstIters[i] = lstIters[i].replace('[{', '').replace('}]', '')
            lstIters = list(dict.fromkeys(lstIters))

            if strQreFormated in dictFormated.keys():
                dictFormated[strQreFormated][2].extend(lstIters)
            else:
                dictFormated[strQreFormated] = [strQreFormated, lst[1], lstIters]
        return list(dictFormated.values())


    def toMerge(self, lstMerge):
        df = self.df.copy()
        dm = self.dm.copy()
        for lst in lstMerge:
            strQreResult = lst[0]
            strQres = lst[1]
            setExclusiveCats = set(lst[2].replace('{', '').replace('}', '').split(','))
            if not strQreResult in df.columns:
                df[strQreResult] = [set({})] * df.shape[0]
            isConstSet = False
            setCats = set()
            for qre in strQres.split('|'):
                if qre[0] == "{":
                    isConstSet = True
                    setCats = set(qre.replace('{', '').replace('}', '').split(','))
                    lstCats = [setCats] * df.shape[0]
                    qreVals = lstCats
                else:
                    qreVals = df[qre]

                df[strQreResult] = [a.union(b).difference(setExclusiveCats)
                                            for a, b in zip(df[strQreResult], qreVals)]

            for i in df.index:
                if (df.at[i, strQreResult] == set({})) \
                        or (isConstSet and len(df.at[i, strQreResult].difference(setCats)) == 0):
                    df.at[i, strQreResult] = {}
            dm = hp.toDm(dm, strQreResult, 200, True)
        return df, dm


    def toGetIters(self, lstGetIters):
        df = self.df.copy()
        dm = self.dm.copy()
        for lst in lstGetIters:
            strQreResult = lst[0]
            lstQres = lst[1].split('|')
            if lst[2] == 'all':
                df[strQreResult] = [self.getItersByVarName(lstQres[0], self.dm)] * df.shape[0]
            else:
                if lst[2] == 'min' or lst[2] == 'max':
                    dfTemp = df.loc[:, lstQres].copy()
                    if lst[2] == 'min':
                        dfTemp['min'] = dfTemp.min(axis=1)
                    else:
                        dfTemp['max'] = dfTemp.max(axis=1)

                lstIters = list()
                for idx in df.index:
                    setIters = set()
                    for qre in lstQres:
                        strdfloc = "df.loc[{}, '{}'] ".format(str(idx), qre)
                        if 'num' in lst[2].lower():
                            strCond = strdfloc + lst[2].replace('{_num', '').replace('}', '').replace('=', '==')
                        elif 'null' == lst[2].lower():
                            strCond = 'len({}) == 0'.format(strdfloc)
                        elif '~null' == lst[2].lower():
                            strCond = 'len({}) > 0'.format(strdfloc)
                        elif 'min' == lst[2].lower() or 'max' == lst[2].lower():
                            strCond = "{} == dfTemp.loc[idx, '{}']".format(strdfloc, lst[2].lower())
                        else:
                            strCond = "hp.iscontainsany(" + strdfloc + ", {'" + lst[2].replace(",", r"','").replace('{', '').replace('}', '') + "'})"

                        if '~' in strCond:
                            strCond = 'not ' + strCond.replace('~', '')

                        if eval(strCond):
                            cat = re.findall(r'\[{+[A-Z|a-z0-9_]+}', qre.split('].')[-2])[0].replace('[{', '').replace('}', '')
                            setIters.add(cat)

                    lstIters.append(setIters)

                df[strQreResult] = lstIters
                df[strQreResult].replace(to_replace=[set()], value=[{}], inplace=True)

            dm = hp.toDm(dm, strQreResult, 200, True)
        return df, dm


    @staticmethod
    def getItersByVarName(strVarName, dm):
        lstVar = re.sub(r'\[{+[A-Z|a-z0-9_]+}]', '[..]', strVarName).split('._')
        lstVar = lstVar[0:-1]
        if len(lstVar) == 1:
            lstIters = dm[lstVar[0]]['iter']
        elif len(lstVar) == 2:
            lstIters = dm[lstVar[0]][lstVar[1]]['iter']
        else:
            lstIters = dm[lstVar[0]][lstVar[1]][lstVar[2]]['iter']
        return lstIters


    def toAssign(self, lstAssign, isAssign):
        df = self.df.copy()
        dm = self.dm.copy()
        for lst in lstAssign:
            strQreResult = lst[0]
            strQres = lst[1]
            lstQres = strQres.split('|')
            strCondition = lst[2]
            if lst[3]:
                setExclusiveCats = set(lst[3].lower().replace('{', '').replace('}', '').split(','))
            else:
                setExclusiveCats = set({})

            if not strQreResult in df.columns:
                if '{' in lstQres[0]:
                    df[strQreResult] = [set({})] * df.shape[0]
                else:
                    if df.dtypes[lstQres[0]] in [np.int, np.float]:
                        df[strQreResult] = [np.nan] * df.shape[0]
                    else:
                        df[strQreResult] = [set({})] * df.shape[0]

            isNumeric = False
            for idx in df.index:
                if eval(self.convertStrCondition(strQreResult, strCondition)):
                    for qre in lstQres:
                        if qre[0] == '{':
                            setCats = set(qre.lower().replace('{', '').replace('}', '').split(','))
                            qreVals = setCats
                            isCat = True
                        else:
                            qreVals = df.loc[idx, qre]

                            if isinstance(qreVals, (np.int, np.float)):
                                isCat = False
                                isNumeric = True
                            else:
                                isCat = True

                        if isCat:
                            if isAssign:
                                df.at[idx, strQreResult] = set(df.loc[idx, strQreResult]).union(set(qreVals)).difference(setExclusiveCats)
                            else:
                                df.at[idx, strQreResult] = set(df.loc[idx, strQreResult]).difference(set(qreVals)).difference(setExclusiveCats)

                            if df.at[idx, strQreResult] == set():
                                df.at[idx, strQreResult] = {}
                        else:
                            if isAssign:
                                if not np.isnan(qreVals):
                                    if df.at[idx, strQreResult] == set():
                                        df.at[idx, strQreResult] = 0
                                    df.at[idx, strQreResult] += qreVals
                            else:
                                df.at[idx, strQreResult] = np.nan

            if isNumeric:
                df[strQreResult].replace(to_replace=[set()], value=[np.nan], inplace=True)

            if df.dtypes[strQreResult] in [np.int]:
                dm = hp.toDm(dm, strQreResult, 3, True)
            elif df.dtypes[strQreResult] in [np.float]:
                dm = hp.toDm(dm, strQreResult, 5, True)
            else:
                dm = hp.toDm(dm, strQreResult, 200, True)
        return df, dm


    @staticmethod
    def convertStrCondition(strQreResult, strCond):
        if '[..]' in strCond:
            strRe = re.findall(r'[A-Z|a-z0-9_]+\[{+[A-Z|a-z0-9_]+}]', strQreResult)
            strFormatedCond = re.sub(r'[A-Z|a-z0-9_]+\[\..]', strRe[0], strCond)
        else:
            strFormatedCond = strCond
        strFormatedCond = strFormatedCond.replace('[{', '<<').replace('}]', '>>')
        strFormatedCond = strFormatedCond.replace(",", "', '").replace("[", "hp.iscontainsany(df.loc[idx ,'").replace("]", "'], ").replace("*{", "{'").replace("}", "'})")
        strFormatedCond = strFormatedCond.replace(r'&', ' and ').replace(r'|', ' or ').replace(r'~', ' not ')
        strFormatedCond = strFormatedCond.replace('<<', '[{').replace('>>', '}]')
        return strFormatedCond


    def toCount(self, lstCount):
        df = self.df.copy()
        dm = self.dm.copy()
        for lst in lstCount:
            strQreResult = lst[0]
            strQres = lst[1]
            setExclusiveCats = set(lst[2].replace('{', '').replace('}', '').split(','))
            if not strQreResult in df.columns:
                df[strQreResult] = [0] * df.shape[0]
            df[strQreResult] = df[strQreResult].astype(np.int32)
            isConstSet = False
            setCats = set()
            for qre in strQres.split('|'):
                if qre[0] == "{":
                    isConstSet = True
                    setCats = set(qre.replace('{', '').replace('}', '').split(','))
                    lstCats = [setCats] * df.shape[0]
                    qreVals = lstCats
                else:
                    qreVals = df[qre]

                df[strQreResult] = [a + len(set(b).difference(setExclusiveCats))
                                            for a, b in zip(df[strQreResult], qreVals)]

            for i in df.index:
                isQreNull = True
                for qre in strQres.split('|'):
                    try:
                        if set(df.at[i, qre]) != set({}):
                            isQreNull = False
                    except KeyError as keyerr:
                        print(keyerr)
                if isQreNull or (isConstSet and df.at[i, strQreResult] == len(setCats)):
                    df.at[i, strQreResult] = -9999
            df.replace(to_replace=[-9999], value=[np.nan], inplace=True)
            dm = hp.toDm(dm, strQreResult, 3, True)
        return df, dm


    def toDiffInter(self, lstDiffInter, strMethod):
        df = self.df.copy()
        dm = self.dm.copy()
        for lst in lstDiffInter:
            strQreResult = lst[0]
            strQres = lst[1]
            if not strQreResult in df.columns:
                df[strQreResult] = [set({})] * df.shape[0]
            isConstSet = False
            setCats = set()
            index = 0
            qreVals1 = list()
            qreValsMerge = [set({})] * df.shape[0]
            for qre in strQres.split('|'):
                if index == 0:
                    if qre[0] == "{":
                        isConstSet = True
                        setCats = set(qre.replace('{', '').replace('}', '').split(','))
                        lstCats = [setCats] * df.shape[0]
                        qreVals1 = lstCats
                    else:
                        qreVals1 = df[qre]
                        qreVals1.replace(to_replace=[{}], value=[set({})], inplace=True)
                else:
                    if qre[0] == "{":
                        isConstSet = True
                        setCats = set(qre.replace('{', '').replace('}', '').split(','))
                        lstCats = [setCats] * df.shape[0]
                        qreVals2 = lstCats
                    else:
                        qreVals2 = df[qre]
                        qreVals2.replace(to_replace=[{}], value=[set({})], inplace=True)

                    qreValsMerge = [a.union(b) for a, b in zip(qreValsMerge, qreVals2)]
                index += 1

            if strMethod == 'diff':
                df[strQreResult] = [a.difference(b) for a, b in zip(qreVals1, qreValsMerge)]
            else:
                df[strQreResult] = [a.intersection(b) for a, b in zip(qreVals1, qreValsMerge)]

            for i in df.index:
                if (df.at[i, strQreResult] == set({})) \
                        or (isConstSet and len(df.at[i, strQreResult].difference(setCats)) == 0 and strMethod == 'diff'):
                    df.at[i, strQreResult] = {}

            dm = hp.toDm(dm, strQreResult, 200, True)
        return df, dm


    def toNumCompared(self, listNumQre):
        df = self.df.copy()
        dm = self.dm.copy()
        for lst in listNumQre:
            strQreResult = lst[0]
            lstQre = lst[1].split('|')
            if not strQreResult in df.columns:
                df[strQreResult] = [set({})] * df.shape[0]
            for i in np.arange(len(lstQre)):
                if '_num' in lstQre[i]:
                    df[lstQre[i]] = [float(lstQre[i].replace('{_num', '').replace('}', ''))] * df.shape[0]
            lstCompared = list()
            for a, b in zip(df[lstQre[0]], df[lstQre[1]]):
                if np.isnan(a) or np.isnan(b):
                    lstCompared.append({})
                else:
                    if a == b:
                        lstCompared.append({'_equal'})
                    elif a > b:
                        lstCompared.append({'_over'})
                    elif a < b:
                        lstCompared.append({'_under'})
            df[strQreResult] = lstCompared
            for i in np.arange(len(lstQre)):
                if '_num' in lstQre[i]:
                    df.drop(lstQre[i], axis='columns', inplace=True)
            dm = hp.toDm(dm, strQreResult, 200, True)
        return df, dm


    def toGetMinMaxNum(self, listNumQre, isGetMin):
        df = self.df.copy()
        dm = self.dm.copy()
        for lst in listNumQre:
            strQreResult = lst[0]
            lstQre = lst[1].split('|')
            if not strQreResult in df.columns:
                df[strQreResult] = [np.nan] * df.shape[0]
            dfTemp = df.loc[:, lstQre].copy()
            if isGetMin:
                df[strQreResult] = dfTemp.min(axis=1)
            else:
                df[strQreResult] = dfTemp.max(axis=1)
            dm = hp.toDm(dm, strQreResult, 5, True)
        return df, dm


    def toGetValsByIters(self, listGetVals):
        df = self.df.copy()
        dm = self.dm.copy()
        for lst in listGetVals:
            strQreResult = lst[0]
            lstQres = lst[1].split('|')
            strItersQre = lstQres[0]
            lstGrid = lstQres[1:]
            lstGrid = self.convertLstToGetValsByIters(strItersQre, lstGrid)
            if not strQreResult in df.columns:
                df[strQreResult] = [set({})] * df.shape[0]
            for idx in df.index:
                if strItersQre[0] == '{':
                    catIters = list(strItersQre.replace('{', '').replace('}', '').split(','))
                else:
                    catIters = list(df.at[idx, strItersQre])
                lstVals = list()
                for cat in catIters:
                    for grd in lstGrid:
                        lstVals.extend(list(df.at[idx, grd.replace('iter', cat)]))
                df.at[idx, strQreResult] = set(lstVals)
            dm = hp.toDm(dm, strQreResult, 200, True)
        return df, dm


    @staticmethod
    def convertLstToGetValsByIters(strItersQre, lstGrid):
        lstItersQre = strItersQre.replace('].', ']|').split('|')
        lstGridResult = list()

        for item in lstGrid:
            if len(lstItersQre) == 0:
                lstGridResult.append(re.sub(r'\[{_\w+}]', '[{iter}]', item))
            else:
                lstGridItems = item.replace('].', ']|').split('|')
                lstGridItems[len(lstItersQre)-1] = re.sub(r'\[{_\w+}]', '[{iter}]', lstGridItems[len(lstItersQre)-1])
                lstGridResult.append('.'.join(lstGridItems))

        lstGridResult = list(dict.fromkeys(lstGridResult))
        return lstGridResult


    def toGetSum(self, lstSum):
        df = self.df.copy()
        dm = self.dm.copy()
        for lst in lstSum:
            strQreResult = lst[0]
            strQres = lst[1]

            if not strQreResult in df.columns:
                df[strQreResult] = [-99999] * df.shape[0]

            isConstNum = False
            numConst = -88888
            for qre in strQres.split('|'):
                if qre[0] == '{':
                    isConstNum = True
                    numConst = float(qre.replace('{_num', '').replace('}', ''))
                    lstCats = [numConst] * df.shape[0]
                    qreVals = lstCats
                else:
                    qreVals = df[qre]

                df[strQreResult] = [a + b if not np.isnan(b) else a for a, b in zip(df[strQreResult], qreVals)]

            df.replace(to_replace=[-99999], value=[np.nan], inplace=True)

            for idx in df.index:
                if not np.isnan(df.loc[idx, strQreResult]):
                    df.at[idx, strQreResult] = df.at[idx, strQreResult] + 99999
                if isConstNum and df.at[idx, strQreResult] == numConst:
                    df.at[idx, strQreResult] = np.nan

            dm = hp.toDm(dm, strQreResult, 5, True)
        return df, dm