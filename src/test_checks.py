import unittest
from helpers import Args # helpers are or testing only
from checks import repo_owner_verification, prerequisites
from src.exceptions import GHTokenError, RepoError

class TestGithubOwnerMixmatch(unittest.TestCase):
    def test_github_owner_mixmatch(self):
        self.args = Args()
        assert repo_owner_verification(args=self.args) == True, "The owner of the current repository is NOT the same as the owner of the repo calling the repository_dispatch action."


class TestRepo(unittest.TestCase):
    def test_repo(self):
        self.args = Args()
        assert self.args.target_repo == "philipdelorenzo/test-sync-action-status", "The target repository is not set."

    def test_prerequisites(self):
        self.args = Args()
        assert prerequisites(args=self.args) == True, "The --target_repo argument is not set."
        
        self.args.target_repo = ""
        with self.assertRaises(RepoError):
            prerequisites(args=self.args)

        self.args.target_repo = None
        with self.assertRaises(RepoError):
            prerequisites(args=self.args)


    