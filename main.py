import argparse
from data_handler import DataHandlerGit

parser = argparse.ArgumentParser()

parser.add_argument("-t", "--gtoken", type=str, help="Токен для входа в гитхаб")
parser.add_argument("-n", "--namerepo", type=str, help="Название репозитория")
parser.add_argument("-r", "--root", type=str, help="Коорневое название репозитория (логин владельца репозитория)")
parser.add_argument("-tp", "--typew", type=str, default='lb', help="тип работы (lb или cw)")
parser.add_argument("-g", "--gllink", type=str, help="Ссылка на гугл документ с дискорд именами и статусами допуска")
parser.add_argument("-ns", "--nsheet", default="Workdata", type=str, help="Название листа с дискорд логинами именами и фамилиями и статусами допуска")
parser.add_argument("-tmpi", "--tmpinput", default='templates/script_templates/temp_for_lb.txt', type=str, help="Путь до загодовки шаблона")
parser.add_argument("-tmpr", "--tmpres", default='templates/result_templates/result_template.txt', type=str, help="Путь до готового шаблона")
parser.add_argument("-gkf", "--glkeyfile", default='userdata-414709-782968eb2a5b.json', type=str, help="Название json файла c ключом для google api (или путь до него)")
args = parser.parse_args()


def handler(gtoken, namerepo, root, typew): # обязаельные аргументы
    """
    gtoken - токен от github
    namerepo - название репозитория
    root - логин владельца репозитория
    typew - тип работы
    """
    if args.gllink is not None: # если передали ссылку на гугл таблицу
        gglink = args.gllink # ссылка на гугл таблицу
        name_google_sheet = args.nsheet # имя страницы в гугл таблице

        git_data_handler = DataHandlerGit(git_token=gtoken, 
                                      name_repo=namerepo, 
                                      git_owner_name=root,
                                      link_to_google_sheet=gglink) 
        
        git_data_handler.update_status_to_proctoring_in_gsheet(name_sheet=name_google_sheet) # обновляет информацию в гугл таблице

        git_data_handler.generate_temp_messasge(type_work=typew, 
                                            script_path=args.tmpinput, 
                                            result_path=args.tmpres,
                                            name_google_sheet=name_google_sheet) # генерирует сообщение по шаблону
        
    elif args.gllink is None: # если не передали ссылку на гугл таблицу
        git_data_handler = DataHandlerGit(git_token=gtoken, 
                                      name_repo=namerepo, 
                                      git_owner_name=root)
        
        git_data_handler.generate_temp_messasge(type_work=typew, 
                                            script_path=args.tmpinput, 
                                            result_path=args.tmpres)
if __name__ == '__main__':
    print(args.typew)
    handler(args.gtoken, args.namerepo, args.root, args.typew)