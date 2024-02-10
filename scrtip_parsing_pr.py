from github import Github
from github import Auth


class ParseDataGit():
	def __init__(self, token, repo_name):
		auth = Auth.Token(token)
		self.g = Github(auth=auth)
		self.user = self.g.get_user().login
		self.repo = self.g.get_repo(f"{self.user}/{repo_name}")
		self.pulls = self.repo.get_pulls(state='open', sort='created')

	def get_title_label_dict(self, tp_work=None):
		user_label_dict = {}
		for pr in self.pulls:
			pull_req = self.repo.get_pull(pr.number)
			title = pull_req.title
			lables = [item.name for item in pull_req.labels]
			type_of_work = title.split('_')[-1]
			if tp_work is None or type_of_work in tp_work:
				user_label_dict[title] = lables
		self.g.close()
		return user_label_dict
	


class PasreTaskGit(ParseDataGit):
	pass


git_data = ParseDataGit(token='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', repo_name='test_repo')
print(git_data.get_title_label_dict(tp_work='ef'))