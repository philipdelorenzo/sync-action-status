# Author: Philip De lorenzo <philip.delorenzo@gmail.com>
import os
import requests
import argparse

from exceptions import GHTokenError, RepoError, GithubActorError, RepoOwnershipMixmatch


def check_gh_token(gh_token: str) -> None:
    """This function checks to ensure that the GH_TOKEN environment variable is set.

    Args:
        gh_token (str): The GitHub token to check.

    Raises:
        GHTokenNotSet: If the GH_TOKEN environment variable is not set.
    """
    if (not gh_token) or (gh_token == ""):
        raise GHTokenError(message="GH_TOKEN environment variable not set.")
    
    if not gh_token.startswith("ghp_"):
        raise GHTokenError(message="GH_TOKEN environment variable is not a valid GitHub token.")


def prerequisites(args: argparse.ArgumentParser.parse_args) -> None:
    """This function checks to ensure that all prerequisites are met before running the script."""
    if (not args.target_repo) or (args.target_repo == ""):
        raise RepoError("The --target_repo argument is required (this is the repository that houses the receiver action).")


def is_org(github_actor: str) -> bool:
    """This function will return True if the Github actor is an organization."""
    if requests.get(f"https://github.com/org/{github_actor}").status_code == 200:
        return True
    
    return False

def repo_owner_verification(args: argparse.ArgumentParser.parse_args) -> None:
    """This function will verify that the owner of the repository is the same as the owner of the action."""
    current_actor = args.current_repo.split("/")[0]
    target_actor = args.target_repo.split("/")[0]

    if current_actor != target_actor:
        return False

    if current_actor == target_actor:
        return True
