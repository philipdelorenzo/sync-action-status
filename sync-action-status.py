import os
import json
import sys
import argparse

from icecream import ic  # We will use icecream to print out the job information
from datetime import datetime, timezone, UTC

from src.checks import check_gh_token, prerequisites
from src.exceptions import GHTokenError
from src.gh import auth, github, get_repos, get_repository_dispatch

from src.gh import (
    get_workflow_data,
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
    "--is_org",
    action="store_true",
    required=False,
    default=False,
    help="The action to sync the status from.",
)
parser.add_argument(
    "--interval",
    type=str,
    required=False,
    help="The interval to poll the action for status.",
)
parser.add_argument(
    "--repo",
    dest="repo",
    type=str,
    required=True,
    help="The source repository to sync the status from.",
)

# If is_org is set to True, then we want to require the org argument
if parser.parse_args().is_org:
    parser.add_argument(
        "--org",
        dest="org",
        type=str,
        required=True,
        help="The source repository to sync the status from.",
    )
else:
    gh_actor = os.environ.get(
        "GH_ACTOR"
    )  # If is_org is false, then we want to use the actor as the org

args = parser.parse_args()

### Environment Variables ###
# GH_TOKEN
_gh_token = os.getenv(
    "GH_TOKEN"
)  # Let's set this as a variable so we don't have to pass it in in clear text


if __name__ == "__main__":
    # Let's check to ensure that our token is set
    prerequisites(
        args=args
    )  # Check the prerequisites, ensure we have what we need to proceed
    check_gh_token(gh_token=_gh_token)  # Check the GitHub token

    # Let's get the repository dispatch org/repo
    # If the is_org flag is set to True, then we want to use the org argument
    repo_dispatch = get_repository_dispatch(args=args)

    if args.is_org:
        print(f"Organization: {args.org}")

    else:
        print(f"Actor: {os.getenv('GH_ACTOR')}")

        # Let's get our auth setup for the GitHub API
        auth = auth(gh_token=_gh_token)
        api = github(auth=auth)  # Connect to the GitHub API

        # Get the repos
        #repos = get_repos(api=api)

        workflow_data = get_workflow_data(repo=repo_dispatch) # Let's get a list of the workflows in the repos
        event_type_data = get_event_type_list_for_workflows(repo=repo_dispatch) # Let's get a list of the event types for the workflows
        filtered_events = {k: v for k, v in event_type_data.items() if args.eventType in v}

        if len(filtered_events) > 1:
            print(f"Found multiple workflows for the event type {args.eventType}")
            sys.exit(5)

        # This currently assumes there is ONLY 1 workflow for the event type
        # This is subject to change as we mature and add more workflows - new logic will be needed here to accomadate
        if len(filtered_events) == 1:
            workflow_name = list(filtered_events.keys())[0] # This will be used as the key to find the id number of the workflow
            workflow_id = get_workflow_id(_name=workflow_name)
            current_running_jobs = current_running_job_list(_name=workflow_name)
            filtered_jobs = filter_job_list(current_running_jobs)
            _workflow_job_id = filtered_jobs['databaseId']

            ic(f"Worflow Data: {workflow_data}")
            ic(f"Event Type Data: {event_type_data}")

            ic(f"Current Running Jobs: {current_running_jobs}")
            ic(f"Filtered Jobs: {filtered_jobs}")

            # Let's print the workflow name and id to the console
            print(f"Workflow Name: {workflow_name}")
            print(f"Workflow ID: {workflow_id}")
            print(f"Workflow Run ID: {_workflow_job_id}")

            # Let's follow the logs of the workflow and exit status
            follow_workflow_job(workflow_job_id=_workflow_job_id, interval=args.interval)

        else:
            print(f"Multiple event types {args.eventType} found -- SRE Code changes needed to facilitate.")
            sys.exit(5)

        # Close the connection
        api.close()
