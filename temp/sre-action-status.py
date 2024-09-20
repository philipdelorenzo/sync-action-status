"""This python script will return the deployment pipelines, and ids for the SRE Deployments Repo -- @manscaped-dev/manscaped-sre-deployments

# Author: @philipdelorenzo-manscaped<phil.delorenzo@manscaped.com>
"""
import os
import json
import yaml
import sys
import argparse

from icecream import ic
from shared import (
    get_workflow_data,
    get_workflow_id,
    get_event_type_list_for_workflows,
    current_running_job_list,
    filter_job_list,
    follow_workflow_job
)

BASE = os.path.dirname(os.path.abspath(__file__)) # Get the base directory of the script
WORKDIR = os.environ.get("WORKDIR") # Get the workflows directory

config = json.load(open(os.path.join(BASE, "config.json"))) # Load the config file
ic.disable() # Disable icecream by default

# Let's create an argument parser
parser = argparse.ArgumentParser()

parser.add_argument(
    '--eventType',
    # The event type to use to find the workflow name, we are using the camelCase naming convention so that we
    # can easily decipher the event type from the command line arg
    dest='eventType',
    type=str,
    required=True,
    help='The event type to use to find the workflow name.'
)
parser.add_argument(
    '--interval',
    dest='interval',
    type=str,
    help='The interval to poll the GHA (seconds).'
)
parser.add_argument(
    '--debug',
    # The debug flag to enable debugging
    dest='debug',
    action='store_true',
    help='Enable debugging.'
)

args = parser.parse_args() # Parse the arguments

if args.debug:
    ic.enable() # Enable icecream if the debug flag is set

if __name__ == "__main__":
    workflow_data = get_workflow_data() # Let's get a list of the workflows in the repos
    event_type_data = get_event_type_list_for_workflows()
    filtered_events = {k: v for k, v in event_type_data.items() if args.eventType in v}

    #print(get_event_type_list_for_workflows()) # Print the event triggers for the workflows
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
