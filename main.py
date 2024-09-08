import os

from src.checks import check_gh_token
from src.exceptions import GHTokenError


if __name__ == '__main__':
    # Let's check to ensure that our token is set
    check_gh_token()
