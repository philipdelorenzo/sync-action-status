import os
import sys
import json
import yaml
import time
import argparse
import subprocess # We will use subprocess to run the gh command to get the deployment pipelines

from github import Github

# Authentication is defined via github.Auth
from github import Auth

from icecream import ic # We will use icecream to print out the job information
from datetime import datetime, timezone, UTC

BASE = os.path.dirname(os.path.abspath(__file__)) # Get the base directory of the script
WORKDIR = os.environ.get("WORKDIR") # Get the workflows directory

class GithubAPI:
    def __init__(
            self,
            token: str,
            api_data: str
            ) -> None:
        self.token = token
        self.api_data = api_data # The API data to use for the Github API repos/{username}/{repo}/actions/runs

        self.repo_actions_data = self.actions_runs
        print(type(self.repo_actions_data))

    def actions_runs(self) -> str:
        return f"https://api.github.com/repos/{self.api_data}/actions/runs"

        
# using an access token
def auth(gh_token: str) -> Auth.Token:
    return Auth.Token(gh_token)

# Public Web Github
def github(auth: Auth.Token) -> Github:
    return Github(auth=auth)

# Github Enterprise with custom hostname
#g = Github(base_url="https://{hostname}/api/v3", auth=auth)

# Then play with your Github objects:
def get_repos(api: Github) -> list:
    repos = []
    for repo in api.get_user().get_repos():
        repos.append(repo)
    
    return repos


def get_workflow_data(repo: str) -> list[dict]:
    """This function will return the deployment workflows for the SRE Deployments Repo -- @manscaped-dev/manscaped-sre-deployments.

    Args:
        repo (str): The repository to get the workflow data from.

    Returns:
        lists: The deployment workflows for the SRE Deployments Repo -- @manscaped-dev/manscaped-sre-deploy

        For example:
        [
            {
                "name": "workflow-name",
                "id": "workflow-id",
                "path": "workflow-path"
            },
            ...
        ]
    """
    # Let's get a JSON objects of the name, id of the workflows
    _cmd = [
            "gh",
            "workflow",
            "list",
            "--repo",
            repo,
            '--json=name,id,path,state',
        ]

    return json.loads(subprocess.check_output(_cmd).decode("utf-8").strip())
