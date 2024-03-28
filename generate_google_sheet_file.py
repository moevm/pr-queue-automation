import httplib2 
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials	

NAMEFILE = ''
with open('GOOGLE_KEY.txt', mode="r", encoding="utf-8") as results: 
         NAMEFILE = results.readline()

CREDENTIALS_FILE = NAMEFILE  # Имя файла с закрытым ключом, вы должны подставить свое

# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API 

spreadsheet = service.spreadsheets().create(body = {
    'properties': {'title': 'StudentsWorkData', 'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Workdata',
                               'gridProperties': {'rowCount': 100, 'columnCount': 15}}}]
}).execute()
spreadsheetId = spreadsheet['spreadsheetId'] # сохраняем идентификатор файла

#выдаем разрешение пользователю через google drive
driveService = build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
access = driveService.permissions().create(
    fileId = spreadsheetId,
    body = {'type': 'user', 'role': 'writer', 'emailAddress': 'asdasfasfdasf084@gmail.com'},  # Открываем доступ на редактирование
    fields = 'id'
).execute()

print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)
print("Индификатор файла - ", spreadsheetId)