import os
import argparse

from src.checks import check_gh_token, prerequisites
from src.exceptions import GHTokenError

from src.gh import auth, github, get_repos, get_repository_dispatch

parser = argparse.ArgumentParser(
    prog='sync-action-status',
    description='Syncs the status of a GitHub action to another repository.',
    epilog='This is a test of the epilog.'
)

parser.add_argument('--is_org', action="store_true", required=False, default=False, help='The action to sync the status from.')
parser.add_argument('--interval', type=str, required=False, help='The interval to poll the action for status.')
parser.add_argument('--repo', dest='repo', type=str, required=True, help='The source repository to sync the status from.')

# If is_org is set to True, then we want to require the org argument
if parser.parse_args().is_org == "true":
    parser.add_argument('--org', dest='org', type=str, required=True, help='The source repository to sync the status from.')

args = parser.parse_args()

# Let's convert the JSON true/false to Python True/False
args.is_org = True if args.is_org == "true" else False

### Environment Variables ###
# GH_TOKEN
_gh_token = os.getenv('GH_TOKEN') # Let's set this as a variable so we don't have to pass it in in clear text


if __name__ == '__main__':
    # Let's check to ensure that our token is set
    prerequisites(args=args) # Check the prerequisites, ensure we have what we need to proceed
    check_gh_token(gh_token=_gh_token) # Check the GitHub token
    # Let's get the repository dispatch org/repo
    repo_dispatch = get_repository_dispatch(org=args.org, repo=args.repo)

    if args.is_org:
        print(f"Organization: {args.org}")

    else:
        print(f"Actor: {os.getenv('GH_ACTOR')}")

        # Let's get our auth setup for the GitHub API
        auth = auth(gh_token=_gh_token)
        api = github(auth=auth) # Connect to the GitHub API

        # Get the repos
        repos = get_repos(api=api)

        # Close the connection
        api.close()
