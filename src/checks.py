# Author: Philip De lorenzo <philip.delorenzo@gmail.com>
# Copyright (c) 2024, Philip De Lorenzo
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import argparse

import requests

from src.exceptions import GHTokenError, RepoError


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
        raise GHTokenError(
            message="GH_TOKEN environment variable is not a valid GitHub token."
        )


def prerequisites(args: argparse.ArgumentParser.parse_args) -> bool:
    """This function checks to ensure that all prerequisites are met before running the script.

    Args:
        args (argparse.ArgumentParser.parse_args): The arguments passed in as an argument.

    Raises:
        RepoError: If the --target_repo argument is not set.

    Returns:
        bool: True if all prerequisites are met.
    """
    if (not args.target_repo) or (args.target_repo == ""):
        raise RepoError(
            "The --target_repo argument is required (this is the repository that houses the receiver action)."
        )

    return True


def is_org(github_actor: str) -> bool:
    """This function will return True if the Github actor is an organization."""
    if requests.get(f"https://api.github.com/orgs/{github_actor}").status_code == 200:
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
