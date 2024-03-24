# pr-queue-automation


### Запуск скрипта
Для того, чтобы сформировать шаблонное сообщение, необходимо запустить ```main.py``` со следущими
параметрами. Перед запуском выполнить ```pip install -r requirements.txt```:<br>
__Обязательные параметры__:<br>
```-t --gtoken``` - токен гитхаб<br>
```-n --namerepo ``` - название репозитория<br>
```-r --root``` - Корневое название репозитория (логин владельца репозитория)<br>
```-tp --typew ``` - Тип работы, необходимый в шаблоне. 
*В переменной может быть ```-tp=lb1``` или <br>
```-tp=cw```, соответственно будут найдены работы студентов допущенныйх до 1 лабораторной<br> или до курсовой. Можно сразу найти несколько лабораторных работ или только один вид<br> лабораной вместе со всеми курсовыми, или все курсовые и все лабораторные<br><u>Примеры</u>: ```-tp='lb'``` ```-tp='lb2 cw'``` ```-tp='cw lb'``` ```-tp='lb2 lb3'```*<br>
__Необязательные параметры__:<br>
```-tmpi --tmpinput``` - путь до заготовки шаблона (Используется Jinja2).<br> *Стандартный путь ```~/templates/script_templates/temp_for_lb.txt ```*<br>
```-tmpr --tmpres``` - путь до готового шаблона (Используется Jinja2).<br> *Стандартный путь ```~/templates/result_templates/result_template.txt ```*<br>
*<u>Далее будет объяснение работы скрипта с шаблоном</u>*<br>
```-g --gllink``` - Ссылка на гугл таблицу с дискорд именами и статусами допуска<br>
```-ns --nsheet``` - Название листа в гугл таблице с дискорд логинами, именами и фамилиями,<br> и статусами допуска<br>
*<u>Скрипт работает только на шаблоне такой [таблицы](https://docs.google.com/spreadsheets/d/1WEX-4FBdcUHsJpf7ybKZP52R3X4SfEqdJ8xM-1Tbxt8/edit#gid=0)<br> (на статусы допуска можно не обращать внимание, главное, чтобы форма и данные были корректны) и на примере такого [репозитория](https://github.com/abonent-21/test_repo/pulls) (стандартый репозиторий MOEVM).</u>*<br>
*<u>Пример</u>*:<br>
[![Screenshot-from-2024-03-24-13-37-49.png](https://i.postimg.cc/htKPSnYh/Screenshot-from-2024-03-24-13-37-49.png)](https://postimg.cc/Cz6VN3SV)
### Объяснение работы c шаблоном
Шаблон работает по правилам стандартного шаблонизатора [Jinja2](https://proglib.io/p/rukovodstvo-dlya-nachinayushchih-po-shablonam-jinja-v-flask-2022-09-05). В шаблон передается список со словарями такой формы:
```py
students = [
			{'name': 'Name Surname', 
            'type_work': 'lb1', 
            'discord_login': (0  или 'дискорд логин')}, 
            # 0 если не передали таблицу с дискорд именами
            ...
			]
```
Далее при помощи цикла ```{% for student in students %}``` можно получить заначения <br> ```student.discord_login```, ```student.type_work``` и т.д.<br>
*<u>Пример</u>*:<br>
```
   {% for student in students %}
        {% if student.discord_login != 0 %}
        	@{{student.discord_login}}: работа - {{student.type_work}} вариант -
        {% else %}
        	{{student.name}}: работа - {{student.type_work}} вариант -
        {% endif %}
    {% endfor %}
```
Из примера можно понять, что в случае отсутcтвия таблицы с дискорд логинами, вместо них будут имена и<br> фамилии из репозитория.<br>
*<u>Результат</u>*:<br>
```
С гугл таблицой:
        @mark123: работа - cw вариант -
    
        @toster321: работа - lb2 вариант -
```
```
Без гугл таблицы:
        Mark Markovich: работа - cw вариант -
    
        Kopya Toster: работа - lb2 вариант -
```
### Объяснение работы c таблицой
Пример таблицы уже был упомянут, но приведу его еще раз -> [таблица](https://docs.google.com/spreadsheets/d/1WEX-4FBdcUHsJpf7ybKZP52R3X4SfEqdJ8xM-1Tbxt8/edit#gid=0)<br>
В самой таблице можно редактировать только варианты работ, имя_фамилия и логин<br> дискорда, иначе данные могут отображаться некорректно.<br>
[![Таблица](https://i.postimg.cc/GhZZbxS2/2.png)](https://postimg.cc/ZCxfcpmt)
Для того, чтобы добавить нового студента, достаточно в последней строчке верно ввести<br>
имя и фамилию (по этому параметру идет связь с гитхабом) и указать логин его дискорда. Также можно скопировать фоновый цвет предыдущих ячеек для новой строчки.<br>
__Как создать свою таблицу?__<br>
Работа с *google sheet* происходит посредством передачи запросов при помощи *google api*, о том как создать ключ для подключения к *google api* можно прочитать [здесь](https://habr.com/ru/articles/483302/).<br>
После создания ключа необходимо записать его название в файл ```GOOGlE_KEY.txt```, это можно сделать при помощи скрипта ```python3 set_google_key.py -n название_ключа.json```, где ```-n --nfile``` параметр принимающий имя json ключа. Далее необходимо скопировать таблицу в свой google sheet как в примере и передать ссылку на таблицу в параметр ```-g --gllink``` в ```main.py```.<br>

### Описание устройства кода.
Файл ```script_parsing_pr.py```
```py
class ParseDataGit():
	def __init__(self, token: str, repo_name: str, root: str):
    	token - гитхаб токен
        repo_name - имя ропозитория
        root - логин владельца репозитория
        ...
    def get_title_label_dict(self, tp_work: str=None) -> dict:
    	"""Резльтат - словарь, где ключ имя_фамилия_работа, а значение список лейблов"""
    	tp_work - тип работы, который необходимо спарсить
        Результат:
        # {'Ivan_Ivanov_lb3': ['passed', '-1', 'moodle+', 'new_changes', 'report failed'],
        # 'Kopya_Toster_lb2': ['passed',
        # 					'dedline-',
        # 					'moodle+',
        # 					'new_changes',
        # 					'report failed'],
        # 'Mark_Markovich_cw': ['3',
        # 					'passed',
        # 					'moodle+',
        # 					'new_changes',
        # 					'report failed'],
        # 'Slava_Ivanov_lb1': ['0', 'passed', 'moodle+', 'new_changes', 'report ok']}
    
    def get_status_to_proctering(self, tp_work=None)-> dict:
    	"""Резльтат - словарь, где ключ имя_фамилия_работа, а значение статус допуска"""
    	tp_work - тип работы, который необходимо спарсить
		Результат:
        #{'Ivan_Ivanov_lb3': 'passed',
		# 'Kopya_Toster_lb2': 'not passed',
		# 'Mark_Markovich_cw': 'deadline',
		# 'Slava_Ivanov_lb1': 'protected'}
	
        
```
Файл ```data_handler.py```
```py
class DataHandlerGit(ParseDataGit):
    def __init__(self, git_token, name_repo, git_owner_name, link_to_google_sheet=None):
        super().__init__(token=git_token, repo_name=name_repo, root=git_owner_name)
        
        token - гитхаб токен
        repo_name - имя ропозитория
        root - логин владельца репозитория
        link_to_google_sheet - ссылка на гугл таблицу
   
   def generate_temp_messasge(self, type_work: str, script_path: str, result_path: str, name_google_sheet: str=None, range_data: str="A2:B"):
        """ """
        range_data - промежуток в таблице с парой (имя) (логин дискорд).
       	name_google_sheet - название листа в гугл таблице
        script_path - путь до заготовки шаблона
        result_path - путь, куда будет сохранен готовый шаблон (сразу нужно указть имя файла и тип)
        
   def update_status_to_proctoring_in_gsheet(self, name_sheet):
   """Обнновлет информацию в ячейках в гугл таблице с определенным названием страницы"""
		name_sheet - название страницы в гугл таблице        
```
Стоит добавить, что у функции ```def generate_temp_messasge``` есть параметр, использующий промежуки данных, которые отвечают за эту часть таблицы.
[![Screenshot-from-2024-03-24-15-04-36.png](https://i.postimg.cc/ydTDY6HN/Screenshot-from-2024-03-24-15-04-36.png)](https://postimg.cc/47mfWgnC)<br>
Далее будет описаны 2 скрипта отвечающих за обработку данных в таблице и ее создание<br>
Файл ```generate_google_sheet_file.py```<br>
*<u>Выводит:</u>*<br>
```py
print('https://docs.google.com/spreadsheets/d/' + id листа)
 print("Индификатор файла - ", spreadsheetId) # специальный индификатор
```
Файл ```google_sheet_data_handeler.py```<br>
```py
def get_name_discord_acc_dict(sheet_key, name_sheet, range_data='A2:B'):
	"""Резльтат - словарь, где ключ имя_фамилия_работа, а значение логин дискорд"""
	range_data - промежуток в таблице с парой (имя) (логин дискорд)
    sheet_key - id листа
    name_sheet - имя листа
    
def get_name_status_work_dict_sheet(sheet_key, name_sheet, range_data="A2:Z") -> dict:
	"""Резльтат - словарь, где ключ имя_фамилия, а значение словарь, где ключи работы, а 
    их значения - статусы допуска на русском"""
	sheet_key - id листа
    name_sheet - имя листа
    range_data - вся таблица со всей информацией
    Пример:
    # {'Ivan Ivanov':{"lb1": 'дедлайн', "lb2": 'защитил',"cw": 'допущен',}}
    
def change_data_in_goodle_sheet(sheet_key, name_sheet, cell, data_in_cell:str, gid, color:dict):
	"""Обновление ячеек в гугл таблице"""
    sheet_key - id листа
    name_sheet - имя листа
    cell - ячейка. (к примеру 'A3:B2')
    gid - специальный индификатор листа
    color - фоновый цвет ячейки
```

