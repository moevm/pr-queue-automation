import httplib2 
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials	

CREDENTIALS_FILE = 'userdata-414709-782968eb2a5b.json'  # Имя файла с закрытым ключом, вы должны подставить свое

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API 


def get_name_discord_acc_dict(sheet_key, name_list, range_data,):
    name_login_dicord = {}
    ranges = [f"{name_list}!{range_data}"]       
    results = service.spreadsheets().values().batchGet(spreadsheetId = sheet_key, 
                                        ranges = ranges, #  задаем промежуток считывания
                                        valueRenderOption = 'FORMATTED_VALUE',  
                                        dateTimeRenderOption = 'FORMATTED_STRING').execute() 
    sheet_values = results['valueRanges'][0]['values']
    for i in sheet_values:
        name_login_dicord[i[0]] = i[1]
    return name_login_dicord
