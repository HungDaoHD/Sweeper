import re
import requests


def lsmRecode(dfLsm1, dfLsm2):
    lsm = list()
    for lsm1, lsm2 in zip(dfLsm1, dfLsm2):
        if '_99' in lsm2:
            lsm.append({'_1'})
        else:
            if '_3' in lsm2: # Co 3.Máy hút bụi
                if '_7' in lsm2: # Co 7.Sat Nav
                    if '_9' in lsm2: # Co 9.Máy nghe nhạc MP3/ Ipods
                        lsm.append({'_4'})
                    else: # Ko co 9.Máy nghe nhạc MP3/ Ipods
                        lsm.append({'_3'})
                else: # Ko co 7.Sat Nav
                    if '_4' in lsm2: # Co 4.Lò vi sóng
                        if '_9' in lsm2: # Co 9.Máy nghe nhạc MP3/ Ipods
                            if '_6' in lsm2: # Co 6.Máy rửa chén
                                if '_1' in lsm1: # lsm1 1.Co
                                    lsm.append({'_4'})
                                else: # lsm1 2.Ko
                                    lsm.append({'_3'})
                            else: #Ko 6.Máy rửa chén
                                lsm.append({'_3'})
                        else: # Ko 9.Máy nghe nhạc MP3/ Ipods
                            lsm.append({'_3'})
                    else: # Ko 4.Lò vi sóng
                        lsm.append({'_3'})
            else: # Ko 3.Máy hút bụi
                if '_4' in lsm2: # Co 4.Lò vi sóng
                    if '_7' in lsm2: # Co 7.Sat Nav
                        lsm.append({'_3'})
                    else: # Ko 7.Sat Nav
                        if '_10' in lsm2: # Co 10.TV
                            lsm.append({'_3'})
                        else: # Ko 10.TV
                            lsm.append({'_2'})
                else: # Ko 4.Lò vi sóng
                    if '_5' in lsm2: # Co 5.Máy giặt
                        if '_2' in lsm2: # Co 2.Bàn ăn
                            lsm.append({'_3'})
                        else: # Ko 2.Bàn ăn
                            if '_1' in lsm2: # Co 1.Bồn rửa dành cho nhà bếp
                                if '_10' in lsm2: # Co 10.TV
                                    lsm.append({'_3'})
                                else: # Ko 10.TV
                                    lsm.append({'_2'})
                            else: # Ko 1.Bồn rửa dành cho nhà bếp
                                lsm.append({'_2'})
                    else: # Ko 5.Máy giặt
                        if '_1' in lsm2: # Co 1.Bồn rửa dành cho nhà bếp
                            lsm.append({'_2'})
                        else: #Ko 1.Bồn rửa dành cho nhà bếp
                            if '_2' in lsm2: # Co 2.Bàn ăn
                                if '_8' in lsm2: # Co 8.Laptop
                                    lsm.append({'_2'})
                                else: # Ko 8.Laptop
                                    lsm.append({'_1'})
                            else: # Ko 2.Bàn ăn
                                lsm.append({'_1'})
    return lsm


def mddType(dType):
    if dType == 7:
        strMddType = 'datetime'
    elif dType == 200:
        strMddType = 'cats'
    elif dType == 202:
        strMddType = 'text'
    elif dType == 3:
        strMddType = 'long'
    elif dType == 5:
        strMddType = 'double'
    else:
        strMddType = 'unknown'
    return strMddType


def toDm(dm, fname, ftype, isNewVar):
    rex = r'\[{+[A-Z|a-z0-9_]+}]'
    lstrex = re.findall(rex, fname)
    lstrex = [a.replace('[{', '').replace('}]', '') for a in lstrex]

    if len(lstrex) > 0:
        lstGrid = fname.replace('].', ']|.').split('|.')
        lstGrid = [re.sub(rex, '[..]', a) for a in lstGrid]

        strmddVars = lstGrid[0].replace('[..]', '[{' + lstrex[0] + '}]')
        if lstGrid[0] in dm.keys():
            dm[lstGrid[0]]['mddVars'] = dm[lstGrid[0]]['mddVars'].union({strmddVars})
            dm[lstGrid[0]]['iter'] = dm[lstGrid[0]]['iter'].union({lstrex[0]})
        else:
            dm[lstGrid[0]] = {
                'mddVars': {strmddVars},
                'iter': {lstrex[0]},
                'mddType': 'grid',
                'isNewVar': isNewVar
            }

        if len(lstGrid) == 2:
            if lstGrid[1] in dm[lstGrid[0]].keys():
                dm[lstGrid[0]][lstGrid[1]]['mddVars'] = dm[lstGrid[0]][lstGrid[1]]['mddVars'].union({fname})
            else:
                dm[lstGrid[0]][lstGrid[1]] = {
                    'mddType': mddType(ftype),
                    'mddVars': {fname},
                    'isNewVar': isNewVar
                }

        if len(lstGrid) == 3:
            strmddVars = lstGrid[0].replace('[..]', '[{' + lstrex[0] + '}].') + lstGrid[1].replace('[..]', '[{' + lstrex[1] + '}]')
            if lstGrid[1] in dm[lstGrid[0]].keys():
                dm[lstGrid[0]][lstGrid[1]]['mddVars'] = dm[lstGrid[0]][lstGrid[1]]['mddVars'].union({strmddVars})
                dm[lstGrid[0]][lstGrid[1]]['iter'] = dm[lstGrid[0]][lstGrid[1]]['iter'].union({lstrex[1]})
            else:
                dm[lstGrid[0]][lstGrid[1]] = {
                    'mddVars': {strmddVars},
                    'iter': {lstrex[1]},
                    'mddType': 'grid',
                    'isNewVar': isNewVar
                }

            if lstGrid[2] in dm[lstGrid[0]][lstGrid[1]].keys():
                dm[lstGrid[0]][lstGrid[1]][lstGrid[2]]['mddVars'] = dm[lstGrid[0]][lstGrid[1]][lstGrid[2]]['mddVars'].union({fname})
            else:
                dm[lstGrid[0]][lstGrid[1]][lstGrid[2]] = {
                    'mddType': mddType(ftype),
                    'mddVars': {fname},
                    'isNewVar': isNewVar
                }

        if len(lstGrid) == 4:

            strmddVars = lstGrid[0].replace('[..]', '[{' + lstrex[0] + '}].') + lstGrid[1].replace('[..]', '[{' + lstrex[1] + '}]')
            if lstGrid[1] in dm[lstGrid[0]].keys():
                dm[lstGrid[0]][lstGrid[1]]['mddVars'] = dm[lstGrid[0]][lstGrid[1]]['mddVars'].union({strmddVars})
                dm[lstGrid[0]][lstGrid[1]]['iter'] = dm[lstGrid[0]][lstGrid[1]]['iter'].union({lstrex[1]})
            else:
                dm[lstGrid[0]][lstGrid[1]] = {
                    'mddVars': {strmddVars},
                    'iter': {lstrex[1]},
                    'mddType': 'grid',
                    'isNewVar': isNewVar
                }

            strmddVars = lstGrid[0].replace('[..]', '[{' + lstrex[0] + '}].') \
                         + lstGrid[1].replace('[..]', '[{' + lstrex[1] + '}].') \
                         + lstGrid[2].replace('[..]', '[{' + lstrex[2] + '}]')

            if lstGrid[2] in dm[lstGrid[0]][lstGrid[1]].keys():
                dm[lstGrid[0]][lstGrid[1]][lstGrid[2]]['mddVars'] = dm[lstGrid[0]][lstGrid[1]][lstGrid[2]]['mddVars'].union({strmddVars})
                dm[lstGrid[0]][lstGrid[1]][lstGrid[2]]['iter'] = dm[lstGrid[0]][lstGrid[1]][lstGrid[2]]['iter'].union({lstrex[2]})
            else:
                dm[lstGrid[0]][lstGrid[1]][lstGrid[2]] = {
                    'mddVars': {strmddVars},
                    'iter': {lstrex[2]},
                    'mddType': 'grid',
                    'isNewVar': isNewVar
                }

            if lstGrid[3] in dm[lstGrid[0]][lstGrid[1]][lstGrid[2]].keys():
                dm[lstGrid[0]][lstGrid[1]][lstGrid[2]][lstGrid[3]]['mddVars'] = \
                    dm[lstGrid[0]][lstGrid[1]][lstGrid[2]][lstGrid[3]]['mddVars'].union({fname})
            else:
                dm[lstGrid[0]][lstGrid[1]][lstGrid[2]][lstGrid[3]] = {
                    'mddType': mddType(ftype),
                    'mddVars': {fname},
                    'isNewVar': isNewVar
                }
    else:
        dm[fname] = {'mddType': mddType(ftype), 'mddVars': {fname}, 'isNewVar': isNewVar}
    return dm


def iscontainsany(a, b):
    c = len(set(a).intersection(set(b)))
    if c == 0:
        return False
    else:
        return True


def internetConnection(url='https://translate.google.com/', timeout=1):
    try:
        _ = requests.head(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        pass
    return False