from scrtip_parsing_pr import ParseDataGit
from jinja2 import Environment, FileSystemLoader
from google_sheet_data_handeler import get_name_discord_acc_dict



class DataHandlerGit(ParseDataGit):
    def __init__(self,token1, name_repo, web_path_to_discord_table=None):
        super().__init__(token=token1, repo_name=name_repo)
        self.path_to_result_temp_message = None # путь до шаблона после собработки скриптом
        self.path_to_temp_message = None # путь до jinja скрипта с шаблоном
        self.path_table_discord_names = web_path_to_discord_table # ссылка на гугл таблицу


    def generate_temp_messasge(self, type_work):
        path_temp_message='/'.join(self.path_to_temp_message.split('/')[:-1])
        name_of_file = self.path_to_temp_message.split('/')[-1]
        path_res_temp_message=self.path_to_result_temp_message
        if path_res_temp_message is None or path_res_temp_message is None: # проверка на наличие пути к шаблонам
            print("Set path to result and script message")
            raise Exception
        name_status_list_of_dict = []
        students_status = self.get_status_to_proctering() # cловарь с именами и статусами допуска
        discord_login = get_name_discord_acc_dict(sheet_key='1WEX-4FBdcUHsJpf7ybKZP52R3X4SfEqdJ8xM-1Tbxt8',
                          name_list='Workdata',
                          range_data='A2:B')


        for student in students_status:
            buffer_dict = {}
            name = ' '.join(student.split('_')[:-1])
            status = students_status[student]
            t_work = student.split('_')[-1]
            if status == 'passed' and type_work in t_work:
                buffer_dict['name'] = name
                buffer_dict['status'] = status
                buffer_dict['discord_login'] = discord_login[name]
                name_status_list_of_dict.append(buffer_dict)

        environment = Environment(loader=FileSystemLoader(path_temp_message)) # среда для шаблона jinja 

        results_filename = path_res_temp_message
        template = environment.get_template(name_of_file)

        context = {
            "students": name_status_list_of_dict, #список для подстановки данных в шаблон
        }

        with open(results_filename, mode="w", encoding="utf-8") as results: 
            results.write(template.render(context))
            print(f"Data has been written to {results_filename}")
        
    def set_path_to_temp_message(self, path):
        self.path_to_temp_message = path
	
    def get_path_to_temp_message(self):
        return self.path_to_temp_message
    
    def set_path_to_res_temp_message(self, path):
        self.path_to_result_temp_message = path
    
    def get_path_to_res_temp_message(self):
        return self.path_to_result_temp_message
    
    def set_path_to_table_discord_names(self, path):
        self.path_table_discord_names = path
	
    def get_path_to_table_discord_names(self):
        return self.path_table_discord_names
    
    def get_data_from_google_sheet():
        pass

a = DataHandlerGit(token1='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',name_repo='test_repo')
a.set_path_to_res_temp_message('templates/result_templates/result_template.txt')
a.set_path_to_temp_message('templates/script_templates/temp_for_lb.txt')
a.generate_temp_messasge(type_work='lb')
        

        

