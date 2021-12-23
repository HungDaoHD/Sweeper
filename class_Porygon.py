import pygsheets
import pandas as pd
import json
import tempfile
import os
from uuid import uuid4
from datetime import datetime
import win32api
import traceback


class porygon:

    def __init__(self):
        creds_file = self._google_creds_as_file()
        self.gc = pygsheets.authorize(service_account_file=creds_file.name)
        creds_file.close()
        os.unlink(creds_file.name)
        if os.path.exists(creds_file.name):
            os.remove(creds_file.name)
        self.wb = self.gc.open('sweeperDatabase')
        self.wbMlv = self.gc.open('MLV')


    @staticmethod
    def _google_creds_as_file():
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(json.dumps({
          "type": "service_account",
          "project_id": "sweeperdatabase",
          "private_key_id": "73472bce1d98f76c1f7f03d7327da4f3c2f31620",
          "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC0EeaDwOqMdx6v\nKtjNIG8X9iRA3Y7CJ6GcPw9/OWK7qWIs+ccLT5XjGUYAjmyxNLZp6X6RZH/kejNC\nxtJTBCx+WcxSEyr43N+KWZaQqJFp2tnNsF4mdETiyasIG1ALEjOMayeaVCxsz0mi\nikT2fQB7iWln85oPUJjCT7H41sKvlm7TjKNmU761E38Z77GjLgVBuovMqyvxkV3M\nW11ShDfXedSztz++rGzTSI77b2npHC2clM9wViGZW8ndydJRbMxt+tBHDs8oVJO/\nvlPNWoSMxF3/AdaFRCFpYvHyJCqNuDhKS5E678l6+dFF9Gq2pqnDgB3rX4FI7xp5\n9RMlhfLhAgMBAAECggEABDKQn/MGZKmk/pDuOdkVZ3njSw6YtKAg4JgI7L6YaLOt\nNRgwRbkgTzyerzk8TmTIrC8qgwm6zRQnwr9vIrFFUKXkoRsorfsHTCqd25eaWcNy\nWIM4E24AnXrCMMlJZ3pDcMGeTDb4sonVREoBC1ZLOK+YB4Zo40Ea0BjBSmgsywcz\nXo05YviD6GGHcGnivH4PZPiO+76by8BxERvZBbKVkok6LuSC3LsFF3Eqmlza59mc\n8qa7OGRPApZCPrWSDuFGDGRyuNVjXQaJB4d41u6quAymf0bG0F3vEyab2SS4fNo8\nra0rsQpP+3ggANKMnN0T8HyDNOFvcJQ9o3O1Pc8N2wKBgQDh2mwQ+Ns8eooEcvPB\nIdbiC4OLpIw9SrOeXJsi8Hr02ECdAGkflCjbzfzc9c54ylHXawxeeD9czZDZUoUh\nkYcRpZw1aCPw7LNy9e/aRoErXwtg1EDYJRr3hm3Y6QqmlPe9LuldwdC/qKysJLwr\neZcGYsMsWLp4sAasneB6A7B4+wKBgQDMGwc2Pzy9Q9TEE0PereG0hnCE35SHELtk\ndAE5XrNNXcSM9TIMUYtjbkDP+qBPdmklKve2xpmb15hT1fx0ncHyvaD2DMN0pLbR\nyLNIcbNIvK7+a1cwsLRouoqwi6kNeBpCyKDUAWPoIDRVDCWoSZBEHnzy8rTuye0R\nZQM9Idn00wKBgAetmUbqbumbcN292rOSJvAAXDR/H5Vl2L1lgJCrhEKWp3uu6+P6\n8XinhBUu9hn9JtMf/Ieppt3Mz0PUHlqJzAG5k5ntNGuYYHFkEwdkpjeHP6fHD31J\npaUMmOdq5MXNAq8XzS82y5X4cgZYKV2BALVi3ie/zHcV5OQxadQ8E9/JAoGBAKjA\nXAkc5bIyJ/LpXr74ktk4IkWpuVqmmdjnFLADPUnlEgHdJEENFqrh2FJcjDjG1Q42\n5VJIB27TJQ2DqdQdLuLsp+1nBh8lpEX0o05tO2cTIbgWtaL7Jl5EhTCMd/w75bJ7\nwIUolRqxrbL3dRcbo1y+vF3+D1wytYAhPTlJCLSjAoGAON2tsMcDtwr8bgXEJfix\n/LJQ7jooiUF5Q73PXDGqzHXkgVChqKIBRrD6HeQRcnIMez9JXE1XEN11F1W351Ax\nWVnFVpa9W1dWsa0gWxm5FI52Kyt40o4sWO7+Zkm+S3BivDACeeyH3FinkTLdPMH6\nlmrRxh5KCcsPr+jW0vt2EZ4=\n-----END PRIVATE KEY-----\n",
          "client_email": "hungdao@sweeperdatabase.iam.gserviceaccount.com",
          "client_id": "116513711359828473601",
          "auth_uri": "https://accounts.google.com/o/oauth2/auth",
          "token_uri": "https://oauth2.googleapis.com/token",
          "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
          "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/hungdao%40sweeperdatabase.iam.gserviceaccount.com"
        }).encode('utf-8'))
        temp.flush()
        return temp


    def tryLogin(self, userName, userPass, isLogin=True):
        try:
            ws = self.wb.worksheet_by_title('Users')
            dfUser = pd.DataFrame(ws.get_all_records())

            if isLogin:
                dfLogin = dfUser.loc[((dfUser['Name'] == userName) & (dfUser['Pass'] == userPass))]
            else:
                dfLogin = dfUser.loc[((dfUser['Name'] == userName) & (dfUser['Pass'] == userPass))]

            if dfLogin.empty:
                return False, False

            if isLogin:
                dfLogin = dfLogin.loc[(dfLogin['Status'] == 'inactive')]
            else:
                dfLogin = dfLogin.loc[(dfLogin['Status'] == 'active')]

            if dfLogin.empty:
                return True, False

            dfLogin = dfLogin.copy()
            if isLogin:
                dfLogin['Status'] = ['active']
                dfLogin['LoginDate'] = [str(datetime.now().replace(microsecond=0))]
            else:
                dfLogin['Status'] = ['inactive']
                dfLogin['LogoutDate'] = [str(datetime.now().replace(microsecond=0))]

            lstLoginUpdate = dfLogin.values.tolist()
            if not isLogin:
                lstLoginUpdate[0][7] = str(datetime.strptime(lstLoginUpdate[0][6], '%Y-%m-%d %H:%M:%S') - datetime.strptime(lstLoginUpdate[0][5], '%Y-%m-%d %H:%M:%S'))
            ws.update_row(lstLoginUpdate[0][0] + 1, values=lstLoginUpdate)
            return True, True
        except Exception:
            return False, False


    def checkVersion(self, strVersion):
        try:
            ws = self.wb.worksheet_by_title('Version')
            dfVer = pd.DataFrame(ws.get_all_records())
            dfVer = dfVer.loc[((dfVer['Version'] == strVersion) & (dfVer['Status'] == 'lastest'))]
            if dfVer.empty:
                return False
            return True
        except Exception:
            return False


    def insertLog(self, userName, filePath, fileName):
        ws = self.wb.worksheet_by_title('Log')
        my_list = [[uuid4().hex, userName, filePath, fileName, str(datetime.now()), win32api.GetUserName()]]
        ws.insert_rows(1, number=1, values=my_list, inherit=False)


    def tryChangePass(self, userName, userPass, newPass):
        try:
            ws = self.wb.worksheet_by_title('Users')
            dfUser = pd.DataFrame(ws.get_all_records())

            dfLogin = dfUser.loc[((dfUser['Name'] == userName) & (dfUser['Pass'] == userPass))]

            if dfLogin.empty:
                return False, 'Please check your user name and old password.'

            dfLogin = dfLogin.loc[(dfLogin['Status'] == 'inactive')]

            if dfLogin.empty:
                return False, 'You cannot change active account\'s password.'

            dfLogin = dfLogin.copy()
            dfLogin['Pass'] = newPass
            lstLoginUpdate = dfLogin.values.tolist()
            ws.update_row(lstLoginUpdate[0][0] + 1, values=lstLoginUpdate)

            return True, 'Password successfully change.'
        except Exception:
            return False, traceback.format_exc()


    def trySaveMlvFormat(self, userName, prjName, lstRows):
        try:
            wsUser = self.wbMlv.worksheet_by_title('Permission')
            dfUser = pd.DataFrame(wsUser.get_all_records())
            dfUser = dfUser.loc[((dfUser['Project'] == prjName) & (dfUser['User'] == userName))]

            if dfUser.empty:
                return False, 'You don\'t have permission to save.'
            else:
                ws = self.wbMlv.worksheet_by_title(prjName)
                wsRng = pygsheets.datarange.DataRange(start='A2', end='B100', worksheet=ws)
                wsRng.clear()

                wsRng = pygsheets.datarange.DataRange(start='A2', end=f'B{len(lstRows)+1}', worksheet=ws)
                wsRng.update_values(lstRows)
                return True, 'Checklist is successfully saved.'

        except Exception:
            return False, traceback.format_exc()


    def tryLoadMlvFormat(self, prjName):
        try:
            ws = self.wbMlv.worksheet_by_title(prjName)
            df = pd.DataFrame(ws.get_all_records())
            strUploadedDate = ''
            if '_db' in prjName:
                wsPermission = self.wbMlv.worksheet_by_title('Permission')
                dfPermission = pd.DataFrame(wsPermission.get_all_records())
                strUploadedDate = dfPermission.loc[(dfPermission['Project'] == prjName.replace('_db', '')), 'UploadedDate'].values[0]

            return True, df, strUploadedDate
        except Exception:
            return False, traceback.format_exc(), ''


    def tryAddMlvClientDb(self, prjName, dfClientDb):
        try:
            wsPermission = self.wbMlv.worksheet_by_title('Permission')
            df = pd.DataFrame(wsPermission.get_all_records())
            df.at[(df['Project'] == prjName), 'UploadedDate'] = [str(datetime.now().replace(microsecond=0))]
            wsPermission.clear()
            wsPermission.set_dataframe(df, (1, 1), encoding='utf-8', fit=True)
            wsPermission.frozen_rows = 1

            ws = self.wbMlv.worksheet_by_title(f'{prjName}_db')
            ws.clear()
            ws.set_dataframe(dfClientDb, (1, 1), encoding='utf-8', fit=True)
            ws.frozen_rows = 1
            return True, 'Client database is successfully inputted.'
        except Exception:
            return False, traceback.format_exc()