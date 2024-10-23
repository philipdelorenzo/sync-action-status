import os
import json
import subprocess # We will use subprocess to run the gh command to get the deployment pipelines

from github import Github

# Authentication is defined via github.Auth
from github import Auth

from icecream import ic # We will use icecream to print out the job information
from src.shared import get_workflow_data
#from datetime import datetime, timezone, UTC

BASE = os.path.dirname(os.path.abspath(__file__)) # Get the base directory of the script
WORKDIR = os.environ.get("WORKDIR") # Get the workflows directory

class GithubAPI:
    def __init__(
            self,
            token: str,
            api_data: str
            ) -> None:
        self.token: str = token
        self.api_data: str = api_data # The API data to use for the Github API repos/{username}/{repo}/actions/runs

        self.repo_actions_url = self.actions_runs()
        ic(f"Repo Actions Data(Type) --> {type(self.repo_actions_url)}")

    def actions_runs(self) -> str:
        return f"https://api.github.com/{self.api_data}/actions/runs"

# using an access token
def auth(gh_token: str) -> Auth.Token:
    return Auth.Token(gh_token)

# Public Web Github
def github(auth: Auth.Token) -> Github:
    return Github(auth=auth)

# Then play with your Github objects:
def get_repos(api: Github) -> list:
    repos = []
    for repo in api.get_user().get_repos():
        repos.append(repo)
    
    return repos
