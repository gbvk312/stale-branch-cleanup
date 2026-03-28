import unittest
from unittest.mock import patch
from stale_branch_cleanup import get_default_branch, get_merged_branches

class TestStaleBranchCleanup(unittest.TestCase):
    @patch('stale_branch_cleanup.run_cmd')
    def test_get_default_branch(self, mock_run_cmd):
        mock_run_cmd.return_value = "  HEAD branch: main\n  Remote branch: main"
        self.assertEqual(get_default_branch(), "main")

    @patch('stale_branch_cleanup.run_cmd')
    def test_get_merged_branches(self, mock_run_cmd):
        mock_run_cmd.return_value = "  feature/a\n* main\n  bugfix/b\n  main"
        branches = get_merged_branches("main")
        self.assertIn("feature/a", branches)
        self.assertIn("bugfix/b", branches)
        self.assertNotIn("main", branches)

if __name__ == '__main__':
    unittest.main()
