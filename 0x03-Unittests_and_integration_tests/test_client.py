#!/usr/bin/env python3
"""Unit tests for GithubOrgClient class in client.py."""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for the GithubOrgClient.org property."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns expected data."""
        expected = {"login": org_name, "id": 123}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        result = client.org  #Access as a property

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
