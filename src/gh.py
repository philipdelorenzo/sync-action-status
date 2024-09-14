import os
from github import Github

# Authentication is defined via github.Auth
from github import Auth

# using an access token
def auth(gh_token: str) -> Auth.Token:
    return Auth.Token(gh_token)

# Public Web Github
def github(auth: Auth.Token) -> Github:
    return Github(auth=auth)

# Github Enterprise with custom hostname
#g = Github(base_url="https://{hostname}/api/v3", auth=auth)

# Then play with your Github objects:
def get_repos(conn: Github) -> list:
    repos = []
    for repo in conn.get_user().get_repos():
        repos.append(repo)
    
    return repos

# To close connections after use
def close(conn: Github) -> None:
    conn.close()
