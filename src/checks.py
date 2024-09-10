# Author: Philip De lorenzo <philip.delorenzo@gmail.com>

from src.exceptions import GHTokenError


def check_gh_token(token: str) -> None:
    """This function checks to ensure that the GH_TOKEN environment variable is set.

    Args:
        token (str): The GitHub token to check.

    Raises:
        GHTokenNotSet: If the GH_TOKEN environment variable is not set.
    """
    if (not token) or (token == ""):
        raise GHTokenError(message="GH_TOKEN environment variable not set.")
    
    if not token.startswith("ghp_"):
        raise GHTokenError(message="GH_TOKEN environment variable is not a valid GitHub token.")
