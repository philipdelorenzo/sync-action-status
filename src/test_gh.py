import unittest

import requests

from gh import get_repository_dispatch
from helpers import Args  # helpers are or testing only


class TestRepoDispatch(unittest.TestCase):
    def test_repo_dispatch(self):
        self.args = Args()
        self.args.is_org = False
        assert (
            get_repository_dispatch(args=self.args)
            == "https://github.com/philipdelorenzo/test-sync-action-status"
        ), "The repository dispatch URL is incorrect."
