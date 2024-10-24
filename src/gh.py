import argparse
import json
import os
import subprocess  # We will use subprocess to run the gh command to get the deployment pipelines
import sys
import time
from datetime import datetime, timezone

import yaml

# Authentication is defined via github.Auth
from github import Auth, Github
from icecream import ic  # We will use icecream to print out the job information

from src.shared import get_workflow_data, get_workflow_id

BASE = os.path.dirname(
    os.path.abspath(__file__)
)  # Get the base directory of the script
WORKDIR = os.environ.get("WORKDIR")  # Get the workflows directory


# using an access token
def auth(gh_token: str) -> Auth.Token:
    return Auth.Token(gh_token)


# Public Web Github
def github(auth: Auth.Token) -> Github:
    return Github(auth=auth)


# Then play with your Github objects:
def get_repos(api: Github) -> list:
    repos = []
    for repo in api.get_user().get_repos():
        repos.append(repo)

    return repos


def get_repository_dispatch(args: argparse.ArgumentParser.parse_args) -> str:
    """This function will return the repository dispatch URL for the repository passed in as an argument.

    Args:
        args (argparse.ArgumentParser.parse_args): The arguments passed in as an argument.

    Returns:
        str: The repository dispatch URL for the repository passed in as an argument.
    """
    return f"https://github.com/{args.target_repo}"


def get_event_type_list_for_workflows(repo: str) -> dict[str, list[str]]:
    """This function will return the event triggers for the workflows.

    This function iterates through all of the github workflows in the repository
    and returns the event triggers for the workflows.

    Args:
        repo (str): The repository to get the event triggers for the workflows.
    Returns:
        dict[str, list[str]]: The event triggers for the workflows
    """
    event_triggers_for_workflows: dict = {}
    workflow_data = get_workflow_data(
        repo=repo
    )  # Let's get a list of the workflows in the repos

    ic(f"Worflow Data: {workflow_data}")

    for workflow in workflow_data:
        # Based on the workflow information - Let's get MORE data from the actual workflow definition file
        ic(f"Workdir --> {WORKDIR}")
        ic(f"Workflow Path: {workflow['path']}")
        _ymlfile = os.path.join(WORKDIR, workflow["path"])

        with open(_ymlfile, "r") as file:
            _data = yaml.safe_load(file)

        ic(f"Workflow Data: {_data}")

        if True in _data.keys():
            # This found the on: key in the workflow file
            if "repository_dispatch" in _data[True].keys():
                event_types = [et for et in _data[True]["repository_dispatch"]["types"]]
                event_triggers_for_workflows.update({workflow["name"]: event_types})

    return event_triggers_for_workflows


def current_running_job_list(repo: str, _name: str) -> list[dict]:
    """Get a list of current running jobs for the workflow id passed in as an argument.

    Args:
        repo (str): The repository to get the current running jobs for.
        workflow_name (str): The workflow name to get the current running jobs for.

    Returns:
        list: The current running jobs for the workflow id passed in as an argument.
    """
    # Let's get a JSON objects of the name, id of the workflows
    # gh run list --workflow <workflow-name> --repo <repo-url> --status=queued --status=in_progress --status=waiting --status=requested --json=databaseId,conclusion,createdAt,number,status,updatedAt,url,headBranch,headSha,name
    count = 0
    while count < 10:
        _cmd = [
            "gh",
            "run",
            "list",
            "--workflow",
            _name,
            "--repo",
            repo,
            f"--status=in_progress",
            "--json=databaseId,conclusion,createdAt,number,status,updatedAt,url,headBranch,headSha,name,displayTitle",
        ]

        r = json.loads(subprocess.check_output(_cmd).decode("utf-8").strip())

        if not r:
            time.sleep(5)
            count += 1
        else:
            break

    return r  # Return the current running job list, already loaded as a JSON object


def iso_to_epoch(iso_date):
    """Converts an ISO 8601 date string to an epoch timestamp (seconds since 1970-01-01T00:00:00Z)."""

    dt = datetime.fromisoformat(iso_date)
    return int(dt.replace(tzinfo=timezone.utc).timestamp())


def filter_job_list(current_running_job_list: list) -> list:
    """Filter out the current running job from the job list.

    This function will filter out the current running job list, to return
    the job with the smallest time delta to the current time (the closest job to the current time).

    Args:
        job_list (list): The list of jobs to filter.

    Returns:
        list: The filtered list of jobs.
    """
    current_time = datetime.now(timezone.utc)

    # To locate the closet job to this current time, we need to evaluate the epoch time of the created time, and compare to now
    _locate_job = {}  # This will create the empty dictionary to locate the job
    for job in current_running_job_list:
        ic(f"JOB: {job}")
        created_at = job["createdAt"]
        created_epoch = iso_to_epoch(created_at)

        now = current_time.strftime("%Y%m%dT%H%M%SZ")
        now_epoch = iso_to_epoch(now)

        # Let's convert the created time to a datetime object
        time_delta = now_epoch - created_epoch
        _locate_job.update({time_delta: current_running_job_list.index(job)})

    # Let's get the job with the smallest time delta
    deltas = list(_locate_job.keys())

    if len(deltas) > 1:
        smallest_delta = __builtins__.min(
            deltas
        )  # Get the smallest time delta = the closest job to the current time
    else:
        smallest_delta = deltas[0]
    job_index = _locate_job[
        smallest_delta
    ]  # Get the index of the job with the smallest time delta

    return current_running_job_list[
        job_index
    ]  # Return the job with the smallest time delta


def follow_workflow_job(workflow_job_id: int, interval: str, repo: str) -> None:
    """Follow the logs of the workflow job passed in as an argument.

    Args:
        workflow_job_id (int): The workflow job id to follow the logs for.
        interval (str): The interval to follow the logs at.
        repo (str): The repository to follow the logs for.
    """
    # Let's follow the logs of the workflow and exit status
    _cmd = [
        "gh",
        "run",
        "watch",
        str(workflow_job_id),
        "--repo",
        repo,
        "--interval",
        interval,
        "--exit-status",
    ]

    result = subprocess.run(
        _cmd, capture_output=True
    )  # Run the command to follow the logs of the workflow job
    if result.returncode != 0:
        print(f"Error following the logs of the workflow job {workflow_job_id}.")
        sys.exit(5)


# To close connections after use
def close(api: Github) -> None:
    api.close()
