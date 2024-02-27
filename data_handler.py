from scrtip_parsing_pr import ParseDataGit
from jinja2 import Environment, FileSystemLoader
from google_sheet_data_handeler import get_name_discord_acc_dict, get_name_status_work_dict, change_data_in_goodle_sheet



class DataHandlerGit(ParseDataGit):
    def __init__(self,token1, name_repo, sheet_google_token):
        super().__init__(token=token1, repo_name=name_repo)
        self.sheet_google_token = sheet_google_token
        # 1WEX-4FBdcUHsJpf7ybKZP52R3X4SfEqdJ8xM-1Tbxt8
        # Workdata
        # A2:B

    def generate_temp_messasge(self, type_work: str, script_path: str, result_path: str, name_google_list: str, range_data: str):
        path_to_result_temp_message = script_path # путь до шаблона после собработки скриптом
        path_to_temp_message = result_path
        path_temp_message='/'.join(path_to_temp_message.split('/')[:-1])
        name_of_file = path_to_temp_message.split('/')[-1]
        path_res_temp_message = path_to_result_temp_message
        if path_res_temp_message is None or path_res_temp_message is None: # проверка на наличие пути к шаблонам
            print("Set path to result and script message")
            raise Exception
        name_status_list_of_dict = []
        students_status = self.get_status_to_proctering() # cловарь с именами и статусами допуска
        discord_login = get_name_discord_acc_dict(sheet_key=self.sheet_google_token, # ключ к оределенному гугл ссылке докмента
                          name_list=name_google_list, # название листа в документе
                          range_data=range_data) # промежутки считывания информации


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

        
    def update_status_to_proctoring(self, name_list_sheet):
        status_to_proctering_from_git = self.get_status_to_proctering()
        status_to_procteting_from_gs = get_name_status_work_dict(sheet_key=self.sheet_google_token, name_list=name_list_sheet)


if __name__ == '__main__':
    a = DataHandlerGit(token1='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',name_repo='test_repo', 
                       sheet_google_token='1WEX-4FBdcUHsJpf7ybKZP52R3X4SfEqdJ8xM-1Tbxt8')
    name_list = 'Workdata'
    r_data = 'A2:B'
    script_text = 'templates/script_templates/temp_for_lb.txt'
    res_text = 'templates/result_templates/result_template.txt'
    # a.generate_temp_messasge(type_work='lb', script_path=script_text, result_path=res_text,
    #                          name_google_list=name_list, range_data=r_data)
    # print(a.update_status_to_proctoring(name_list_sheet="Workdata"))
    change_data_in_goodle_sheet(sheet_key='1WEX-4FBdcUHsJpf7ybKZP52R3X4SfEqdJ8xM-1Tbxt8', 
                                name_list='Workdata', cell='D2', data_in_cell='hello 123', 
                                gid=0, color={'green':1, 'blue':1, 'red':1})
        

        

