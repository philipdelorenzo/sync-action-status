# Author: Philip De lorenzo <philip.delorenzo@gmail.com>
import os
import argparse

from src.exceptions import GHTokenError, RepoError, GithubActorError


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
    if (not args.repo) or (args.repo == ""):
        raise RepoError("The --repo argument is required (this is the repository that houses the receiver action).")

    if args.is_org:
        if (not args.org) or (args.org == ""):
            raise RepoError("The --org argument is required if this is an organization (this is the organization that houses the receiver action).")

    if (os.getenv('GH_ACTOR') is None) or (os.getenv('GH_ACTOR') == ""):
        raise GithubActorError("Cannot retrieve the Github Actor - This is needed for the action to run.")
    