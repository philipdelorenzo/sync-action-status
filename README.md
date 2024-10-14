# sync-action-status

[![Unit Tests](https://github.com/philipdelorenzo/sync-action-status/actions/workflows/run_tests.yml/badge.svg)](https://github.com/philipdelorenzo/sync-action-status/actions/workflows/run_tests.yml)

A GitHub Action to follow `repository_dispatch` runs in your local repo...

This Github Action currently only works with repos that you own. If you are calling a repo that is in the same org or owned by the same
Github User, this Action will sync the Workflow Status of a `repository_dispatch`.

Please see [Repository Dispatch](https://github.com/marketplace/actions/repository-dispatch) and read up on what a repository dispatch is and what it does.

## Usage

To use this Action, there are multiple parts to setup within your Github Action. The process can seem somewhat difficult, as there are multiple repos involved and calling another repo to run an action can be somewhat confusing. The reason for this action is mainly for SRE/Platform/DevOps Engineers. There are times when we want to keep Actions in one place - for a number of reasons:

1. Security _(are there any reasons why you would want to keep the functionality of the action secret, this can help)_
2. SRE can engage with Dev teams with minimal interuptions
    - Let's face it, Development is tough, and developers are busy. Putting all of the Actions in a Repo to run from allows the SRE team to iterate, build, augment Actions without interupting developer's with constant PR requests and extra code bloat in their repo_(s)_.
3. My personal favorite, allows us to remain in Github - 
    - In some cases, there are needs for other services like CircleCI, Buildkite, etc. but if we can remain in Github, this is always a plus.

## Prerequisites

In order to accomplish this, you will need to create a new repo that will house your `dispatch_receivers`. These are the Github Actions that are triggered from other repos by using `event_types`. When an event type is sent to the repo, the receiver is triggered, and the Action is deployed.

- `GITHUB_TOKEN` - It is imperative that you setup a Github Token _(PAT)_ for making the calls in between repos, etc.
    - NOTE: Make sure to add this token to the Action Secrets. You will call the GH_TOKEN using `${{ secrets.GH_TOKEN }}`.
