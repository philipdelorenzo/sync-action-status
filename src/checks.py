# Author: Philip De lorenzo <philip.delorenzo@gmail.com>

from src.exceptions import GHTokenError


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
