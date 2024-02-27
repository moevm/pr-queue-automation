import httplib2 
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials	

CREDENTIALS_FILE = 'userdata-414709-782968eb2a5b.json'  # Имя файла с закрытым ключом, вы должны подставить свое

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API 


def get_name_discord_acc_dict(sheet_key, name_list, range_data='A2:B'):
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

def get_name_status_work_dict(sheet_key, name_list, range_data="A2:Z"):
    status_work = {}
    ranges = [f"{name_list}!{range_data}"]       
    results = service.spreadsheets().values().batchGet(spreadsheetId = sheet_key, 
                                        ranges = ranges, #  задаем промежуток считывания
                                        valueRenderOption = 'FORMATTED_VALUE',  
                                        dateTimeRenderOption = 'FORMATTED_STRING').execute() 
    sheet_values = results['valueRanges'][0]['values']
    for data_student in sheet_values:
        status_work[data_student[0]] = {}
        num_work = 1
        for status in data_student[3::2]:
            if status.lower() != 'допущен':
                status_work[data_student[0]][f'lb_{num_work}'] = ''
            else:
                status_work[data_student[0]][f'lb_{num_work}'] = 'допущен'
            num_work += 1
        if data_student[-1].lower() != 'допущен':
            status_work[data_student[0]]['cw'] = ''
        else:
            status_work[data_student[0]]['cw'] = 'допущен'
    return status_work


def change_data_in_goodle_sheet(sheet_key, name_list, cell, data_in_cell:str, gid, color:dict):
    # Установка формата ячеек
    letter, number = cell[0], cell[1]
    column, row = ord(letter) % 65, int(number) - 1
    service.spreadsheets().batchUpdate(
        spreadsheetId = sheet_key,
        body = 
    {
    "requests": 
    [
        {
        "repeatCell": 
        {
            "cell": 
            {
            "userEnteredFormat": 
                {
                "backgroundColor": color
                }
            },
            "range": 
            {
            "sheetId": gid,
            "startRowIndex": row,
            "endRowIndex": row + 1,
            "startColumnIndex": column,
            "endColumnIndex": column + 1,
            },
            "fields": "userEnteredFormat"
        }
        }
    ]
    }).execute()
    service.spreadsheets().values().batchUpdate(spreadsheetId = sheet_key, body = {
    "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
    "data": [
        {"range": f"{name_list}!{cell}",
         "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
         "values": [
                    [f"{data_in_cell}"] # Заполняем вторую строку
                   ]
        
        }
    ]
    }).execute()
