from scrtip_parsing_pr import ParseDataGit
from jinja2 import Environment, FileSystemLoader
from google_sheet_data_handeler import get_name_discord_acc_dict, get_name_status_work_dict_sheet, change_data_in_goodle_sheet



class DataHandlerGit(ParseDataGit):
    def __init__(self, git_token, name_repo, git_owner_name, link_to_google_sheet=None):
        super().__init__(token=git_token, repo_name=name_repo, root=git_owner_name)
        self.sheet_google_token = None
        self.google_sheet_gid = None
        if link_to_google_sheet is not None:
            self.sheet_google_token = link_to_google_sheet.split('/')[5] # специльный ключ документа
            self.google_sheet_gid = link_to_google_sheet.split('=')[-1] # специльный индификатор документа
    
    def generate_temp_messasge(self, type_work: str, script_path: str, result_path: str, name_google_sheet: str=None, range_data: str="A2:B"):
        """
        range_data - промежуток в таблице с парой (имя) (логин дискорд), лучше не менять.
        """
        path_to_temp_message = script_path # путь до шаблона после обработки скриптом
        path_to_result_temp_message = result_path # путь до готового шаблона 
        path_without_name_tmp_file='/'.join(path_to_temp_message.split('/')[:-1]) # путь расположения файла без его названия
        name_of_file = path_to_temp_message.split('/')[-1] # название шаблона со скриптом Jinja

        if path_to_result_temp_message is None or path_to_temp_message is None: # проверка на наличие пути к шаблонам
            print("Set path to result and script message")
            raise Exception
        
        name_status_list_of_dict = []
        students_status = self.get_status_to_proctering() # cловарь с {(имя)_(рaбота): (статус допуска)}

        if self.sheet_google_token is not None:
            discord_login = get_name_discord_acc_dict(sheet_key=self.sheet_google_token, # ключ к оределенному гугл ссылке докмента
                            name_sheet=name_google_sheet, # название листа в документе
                            range_data=range_data) # промежутки считывания информации


        for student in students_status:
            buffer_dict = {}
            name_surname = ' '.join(student.split('_')[:-1])
            status = students_status[student]
            t_work = student.split('_')[-1]
            condition1 = bool(set(type_work.split()) & set([t_work]))
            condition2 = type_work in ('lb cw', 'cw lb')
            condition3 = type_work in t_work
            if status == 'passed' and (condition1 or condition3 or condition2):
                buffer_dict['name'] = name_surname
                buffer_dict['type_work'] = t_work
                buffer_dict['discord_login'] = 0
                if self.sheet_google_token is not None:
                    buffer_dict['discord_login'] = discord_login[name_surname]
                name_status_list_of_dict.append(buffer_dict)

        environment = Environment(loader=FileSystemLoader(path_without_name_tmp_file)) # среда для шаблона jinja 

        results_filename = path_to_result_temp_message
        template = environment.get_template(name_of_file)

        context = {
            "students": name_status_list_of_dict, #список для подстановки данных в шаблон
        }

        with open(results_filename, mode="w", encoding="utf-8") as results: 
            results.write(template.render(context))
            print(f"Data has been written to {results_filename}")

        
    def update_status_to_proctoring_in_gsheet(self, name_sheet):
        status_to_proctering_from_git = super().get_status_to_proctering()
        status_to_procteting_from_gs = get_name_status_work_dict_sheet(sheet_key=self.sheet_google_token, name_sheet=name_sheet)
        for stud in status_to_proctering_from_git:
            name, surname, type_work = stud.split('_')
            name = name.strip()
            try:
                status = status_to_proctering_from_git[stud]
                if status == 'passed':
                    status_to_procteting_from_gs[f'{name} {surname}'][type_work] = 'допущен'
                elif status == 'deadline':
                    status_to_procteting_from_gs[f'{name} {surname}'][type_work] = 'дедлайн'
                elif status == 'protected':
                    status_to_procteting_from_gs[f'{name} {surname}'][type_work] = 'защитил'
                else:
                    status_to_procteting_from_gs[f'{name} {surname}'][type_work] = ''
            except KeyError:
                print(f'{name} {surname} некорректно записан в гугл таблице или в гихаб репозитории')
        # заполнение листа новыйми данными (заполнение происходит через 1 ячейку)
        start_cell = ['D', 2]
        for stud in status_to_procteting_from_gs:
            gs = status_to_procteting_from_gs
            for work in status_to_procteting_from_gs[stud]:
                status = gs[stud][work]
                cell = f'{start_cell[0]}{start_cell[1]}'
                color_status = {'red':202, 'green':202, 'blue':202}
                if status == 'допущен':
                    color_status = {'red':15, 'green':249, 'blue':46}
                elif status == 'защитил':
                    color_status = {'red':0, 'green':208, 'blue':28}
                change_data_in_goodle_sheet(sheet_key=self.sheet_google_token, 
                                 name_sheet=name_sheet, cell=cell, data_in_cell=status, 
                                 gid=self.google_sheet_gid, color=color_status)
                start_cell[0] = chr(ord(start_cell[0]) + 2) # перепригиваю через букву чтобы перени на новую ячейку
            start_cell[0] = 'D'
            start_cell[1] += 1

        

        

