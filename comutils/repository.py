from comutils.pathy import EnsuredDirectory
from comutils.github_adapter import GithubAdapter
from git import Repo
import subprocess


class RemoteRepositoryNotFoundError(Exception):
    pass


class EnsuredRepository(EnsuredDirectory):
    def __init__(self, path):
        super().__init__(path)
        try:
            self.repo = Repo(self.path)
        except Exception:
            self.repo = Repo.init(self.path)

    def commit(self, message='Update'):
        self.repo.git.add('.')
        self.repo.index.commit(message)
    

class RemoteRepository(EnsuredRepository):
    def create_remote_origin(self, username, repo_name):
        self._validate_github_repo_exists(username, repo_name)
        remote_repo_url = f"https://github.com/{username}/{repo_name}.git"
        self.repo.create_remote('origin', remote_repo_url)

    def _validate_github_repo_exists(self, username, repo_name):
        if not GithubAdapter.get_repo(username, repo_name):
            raise RemoteRepositoryNotFoundError(f"Remote repo for {username}/{repo_name} does not exist")

    def remote_origin_exists(self):
        return any(remote.name == 'origin' for remote in self.repo.remotes)
    
    def active(self):
        return self.repo.active_branch.name

    def push(self, branch, remote='origin'):
        self.repo.git.push(remote, branch)

    def pull(self, branch, remote='origin'):
        self.repo.git.pull(remote, branch)

    def commit_and_push_active(self, message='Update'):
        self.commit(message)
        self.push(self.active())