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

parser.add_argument('--token', type=str, required=True, help='GitHub token to use for authentication.')
parser.add_argument('--repo', type=str, required=False, help='The source repository to sync the status from.')

args = parser.parse_args()

if __name__ == '__main__':
    # Let's check to ensure that our token is set
    check_gh_token(token=args.token)

    # Let's get our auth setup for the GitHub API
    auth = auth(token=args.token)

    conn = github(auth=auth) # Connect to the GitHub API

    # Get the repos
    repos = get_repos(conn=conn)

    # Close the connection
    conn.close()
