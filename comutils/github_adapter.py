import requests
import subprocess
from github import Github

class GithubRepositoryAdapter:
    def __init__(self, repo):
        self.repo = repo

    def add_collaborator(self, collaborator_username, permission):
        self.repo.add_to_collaborators(collaborator_username, permission)

    def remove_collaborator(self, collaborator_username):
        self.repo.remove_from_collaborators(collaborator_username)

class GithubAdapter:
    def __init__(self, personal_access_token=None):
        self.g = Github(personal_access_token)
    
    def get_repo(self, repo_name):
        try:
            full_repo_name = f"{self._get_username()}/{repo_name}"
            return GithubRepositoryAdapter(self.g.get_repo(full_repo_name))
        except Exception:
            return None
        
    def _get_username(self):
        return self.g.get_user().login
