from github import Github
from github import Auth


class ParseDataGit():
	def __init__(self, token, repo_name):
		auth = Auth.Token(token)	
		self.g = Github(auth=auth) # авторизация через токен в гитхаб пользователя
		self.user = self.g.get_user().login # логин юзера
		self.repo = self.g.get_repo(f"{self.user}/{repo_name}") # класс с информацией о репо
		self.pulls = self.repo.get_pulls(state='open', sort='created') # список со всеми пул рек в репо
		self.path_temp_name = None # путь до шаблона с именами
		self.path_table_discord_names = None # путь до таблицы с дискорд именами

	def get_title_label_dict(self, tp_work=None):
		user_label_dict = {}
		for pr in self.pulls:
			pull_req = self.repo.get_pull(pr.number) # информация о пулл рек через номер пулла студента
			title = pull_req.title
			lables = [item.name for item in pull_req.labels]
			type_of_work = title.split('_')[-1]
			if tp_work is None or type_of_work in tp_work: # фильтр для получения определнных работ (cw или lb)
				user_label_dict[title] = lables
		self.g.close()
		return user_label_dict
	
	def set_path_to_temp_names(self, path):
		self.path_temp_name = path
	
	def set_path_to_temp_names(self, path):
		self.path_table_discord_names = path


if __name__ == "__main__":
	git_data = ParseDataGit(token='', repo_name='test_repo')
	print(git_data.get_title_label_dict())
	# тестовый репозиторий https://github.com/abonent-21/test_repo
	# результат: {'Add some code': ['bug', 'enhancement', 'help wanted']}