#!/usr/bin/env python3
"""Unit tests for GithubOrgClient class in client.py."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class."""

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
        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct URL from org payload."""
        test_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, test_payload["repos_url"])


if __name__ == "__main__":
    unittest.main()


