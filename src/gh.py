import os
import argparse
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
def get_repos(api: Github) -> list:
    repos = []
    for repo in api.get_user().get_repos():
        repos.append(repo)
    
    return repos

def get_repository_dispatch(args: argparse.ArgumentParser.parse_args) -> str:
    if args.is_org:
        return f"https://github.com/orgs/{args.org}/{args.repo}"
    else:
        return f"https://github.com/{args.gh_actor}/{args.repo}"


# To close connections after use
def close(api: Github) -> None:
    api.close()
