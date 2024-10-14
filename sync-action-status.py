import os
import sys
import argparse

from icecream import ic  # We will use icecream to print out the job information

from src.checks import check_gh_token, prerequisites, is_org, repo_owner_verification
from src.exceptions import RepoOwnershipMixmatch
from src.gh import auth, github, get_repository_dispatch
from src.gh_api import GithubAPI

from src.gh import (
    get_workflow_id,
    get_event_type_list_for_workflows,
    current_running_job_list,
    filter_job_list,
    follow_workflow_job
)

BASE = os.path.dirname(
    os.path.abspath(__file__)
)  # Get the base directory of the script

ic.disable()  # Disable icecream by default

parser = argparse.ArgumentParser(
    prog="sync-action-status",
    description="Syncs the status of a GitHub action to another repository.",
    epilog="This is a test of the epilog.",
)

parser.add_argument(
    "--interval",
    type=str,
    required=False,
    help="The interval to poll the action for status.",
)
parser.add_argument(
    "--current_repo",
    dest="current_repo",
    type=str,
    required=True,
    help="The current repository calling the sync action.",
)
parser.add_argument(
    "--target_repo",
    dest="target_repo",
    type=str,
    required=True,
    help="The source repository to sync the status from.",
)
parser.add_argument(
    "--debug",
    action="store_true",
    required=False,
    default=False,
    help="Run in debug mode.",
)
parser.add_argument(
    "--event_type",
    dest="event_type",
    type=str,
    required=True,
    help="The event type to sync the status from.",
)

args = parser.parse_args()

### Let's set debugging on if the flag is past
if args.debug:
    ic.enable()

# Let's print out the arguments passed in
ic(f"Arguments: {args}") # debug

# Let's check to ensure that our token is set
prerequisites(
    args=args
)  # Check the prerequisites, ensure we have what we need to proceed

# Let's ensure that the Github Actor owns the repo that we are trying to sync the status from
if not repo_owner_verification(args):
    raise RepoOwnershipMixmatch("The owner of the repository is not the same as the owner of the action.") # This will fail the Action if the owner of the repo is not the same as the owner of the action

gh_actor_org = args.target_repo.split("/")[0]  # Let's get the GitHub actor from the repo
repo_name = args.target_repo.split("/")[1]  # Let's get the repo name from the repo

if is_org(github_actor=gh_actor_org):
    args.is_org = True
    _api_data = f"/orgs/{args.target_repo}"
    ic(f"GitHub Actor: {gh_actor_org} is an organization.") # debug
    ic(f"Args: {args}") # debug
else:
    args.is_org = False
    _api_data = f"/repos/{args.target_repo}"
    ic(f"GitHub Actor: {gh_actor_org} is not an organization.") # debug
    ic(f"Args: {args}") # debug

### Environment Variables ###
# GH_TOKEN
_gh_token = os.getenv(
    "GH_TOKEN"
)  # Let's set this as a variable so we don't have to pass it in in clear text

_api = GithubAPI(
    token=_gh_token,
    api_data=_api_data
)  # Let's create an instance of the GithubAPI class

if __name__ == "__main__":
    check_gh_token(gh_token=_gh_token)  # Check the GitHub token

    # Let's get the repository dispatch org/repo
    # If the is_org flag is set to True, then we want to use the org argument
    repo_dispatch = get_repository_dispatch(args=args)

    ic(f"Actor-Org: {gh_actor_org}") # debug

    # Let's get our auth setup for the GitHub API
    auth = auth(gh_token=_gh_token)
    api = github(auth=auth)  # Connect to the GitHub API
    event_type_data = get_event_type_list_for_workflows(repo=repo_dispatch) # Let's get a list of the event types for the workflows
    
    ic(f"Event Type Data: {event_type_data}")

    # This will return a dictionary of the event types for the workflows
    filtered_events = {} # Let's create an empty dictionary to store the filtered events
    for _name, _event in event_type_data.items():
        ic(f"Event Type Name: {_name} - Event Type Data: {_event}") # debug
        if len(_event) == 1:
            if args.event_type in _event:
                print(f"Event Type: {args.event_type} found in {_event}")
                filtered_events[_name] = _event
            else:
                print(f"Event Type: {args.event_type} not found in {_event}")
                exit(5)

        elif len(_event) > 1:
            for i in _event:
                ic(f"Event Type {args.event_type} --> {_event}") # debug
                print("Development work needed here.")
                exit(0)

        else:
            print(f"Event Type: {args.event_type} not found in {_event}")
            exit(5)

    ic(f"Filtered Events: {filtered_events}")

    if len(filtered_events) > 1:
        print(f"Found multiple workflows for the event type {args.event_type}")
        sys.exit(5)

    # This currently assumes there is ONLY 1 workflow for the event type
    # This is subject to change as we mature and add more workflows - new logic will be needed here to accomadate
    if len(filtered_events) == 1:
        workflow_name = list(filtered_events.keys())[0] # This will be used as the key to find the id number of the workflow
        workflow_id = get_workflow_id(_name=workflow_name, repo=repo_dispatch) # This will return the id of the workflow passed in as an argument
        current_running_jobs = current_running_job_list(_name=workflow_name, repo=repo_dispatch)
        filtered_jobs = filter_job_list(current_running_jobs)
        _workflow_job_id = filtered_jobs['databaseId']

        ic(f"Event Type Data: {event_type_data}") # debug

        ic(f"Current Running Jobs: {current_running_jobs}") # debug
        ic(f"Filtered Jobs: {filtered_jobs}") # debug

        # Let's print the workflow name and id to the console
        print(f"Workflow Name: {workflow_name}")
        print(f"Workflow ID: {workflow_id}")
        print(f"Workflow Run ID: {_workflow_job_id}")

        # Let's follow the logs of the workflow and exit status
        follow_workflow_job(workflow_job_id=_workflow_job_id, interval=args.interval, repo=repo_dispatch)

    else:
        print(f"Multiple event types {args.event_type} found -- SRE Code changes needed to facilitate.")
        sys.exit(5)

    # Close the connection
    api.close()
