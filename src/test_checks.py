import unittest
from helpers import Args
from checks import repo_owner_verification

class TestGithubOwnerMixmatch(unittest.TestCase):
    def test_github_owner_mixmatch(self):
        self.args = Args()
        assert repo_owner_verification(args=self.args) == True, "The owner of the current repository is NOT the same as the owner of the repo calling the repository_dispatch action."
