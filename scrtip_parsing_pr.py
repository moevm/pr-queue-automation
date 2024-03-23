from github import Github
from github import Auth
from time import sleep
import enum

class ProcteringStatus(enum.Enum):
	after_deadline = '-1'
	all_type_of_protect = ['0', '1', '2', '3']



class ParseDataGit():
	def __init__(self, token, repo_name, root):
		auth = Auth.Token(token)	
		self.g = Github(auth=auth) # авторизация через токен в гитхаб пользователя
		self.repo = self.g.get_repo(f"{root}/{repo_name}") # класс с информацией о репо
		self.pulls = self.repo.get_pulls(state='open', sort='created') # список со всеми пул рек в репо
		sleep(3)

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
	
	def get_status_to_proctering(self, tp_work=None):
		students = self.get_title_label_dict(tp_work=tp_work) # словарь ключь - title занчния - список лейблов
		status_of_students = {}
		for student in students:
			if 'deadline-' in students[student] or ProcteringStatus.after_deadline.value in students[student]:
				status_of_students[student] = 'deadline'
			elif 'passed' not in students[student]:
				status_of_students[student] = 'not passed'
			elif len(set(ProcteringStatus.all_type_of_protect.value) & set(students[student])) != 0:
				status_of_students[student] = 'protected'
			else:
				status_of_students[student] = 'passed'	
		return status_of_students


if __name__ == "__main__":
	#пример кода
	git_data = ParseDataGit(token='', repo_name='test_repo', root='abonent-21')
	print(git_data.get_title_label_dict())
	print(git_data.get_status_to_proctering())
	# тестовый репозиторий https://github.com/abonent-21/test_repo
	# результат
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
	# {'Ivan_Ivanov_lb3': 'not passed',
	# 'Kopya_Toster_lb2': 'not passed',
	# 'Mark_Markovich_cw': 'passed',
	# 'Slava_Ivanov_lb1': 'passed'}
	
