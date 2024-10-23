import unittest
import requests

from icecream import ic  # We will use icecream to print out the job information
from helpers import Args  # helpers are or testing only
from gh_api import GithubAPI


class TestAPI(unittest.TestCase):
    args = Args()

    ### Let's set debugging on if the flag is past
    try:
        args.debug
    except AttributeError:
        args.debug = False

    if args.debug:
        ic.enable()
    else:
        ic.disable()

    def test_action_runs(self):
        self.args.is_org = False
        self.api = GithubAPI(
            token="ghp_1234567890",
            api_data="repos/philipdelorenzo/test-sync-action-status",
        )
        assert isinstance(
            self.api.repo_actions_url, str
        ), f"This is not a string -- {self.api.repo_actions_url}"
        assert (
            self.api.repo_actions_url
            == "https://api.github.com/repos/philipdelorenzo/test-sync-action-status/actions/runs"
        ), f"The action runs URL -- {self.api.repo_actions_data} is incorrect."

        self.args.is_org = True
        self.api = GithubAPI(
            token="ghp_1234567890",
            api_data="orgs/philipdelorenzo/test-sync-action-status",
        )
        assert isinstance(
            self.api.repo_actions_url, str
        ), f"This is not a string -- {self.api.repo_actions_url}"
        assert (
            self.api.repo_actions_url
            == "https://api.github.com/orgs/philipdelorenzo/test-sync-action-status/actions/runs"
        ), f"The action runs URL -- {self.api.repo_actions_data} is incorrect."
