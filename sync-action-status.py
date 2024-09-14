import os
import argparse

from src.checks import check_gh_token
from src.exceptions import GHTokenError

from src.gh import auth, github, get_repos

parser = argparse.ArgumentParser(
    prog='sync-action-status',
    description='Syncs the status of a GitHub action to another repository.',
    epilog='This is a test of the epilog.'
)

parser.add_argument('--interval', type=str, required=False, help='The interval to poll the action for status.')
parser.add_argument('--repo', type=str, required=True, help='The source repository to sync the status from.')

args = parser.parse_args()

### Environment Variables ###
# GH_TOKEN
_gh_token = os.getenv('GH_TOKEN') # Let's set this as a variable so we don't have to pass it in in clear text

if __name__ == '__main__':
    # Let's check to ensure that our token is set
    check_gh_token(gh_token=_gh_token)

    # Let's get our auth setup for the GitHub API
    auth = auth(gh_token=_gh_token)

    conn = github(auth=auth) # Connect to the GitHub API

    # Get the repos
    repos = get_repos(conn=conn)

    # Close the connection
    conn.close()
