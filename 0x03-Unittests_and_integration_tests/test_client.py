#!/usr/bin/env python3
"""Integration test for GithubOrgClient"""

import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures by patching requests.get."""
        cls.get_patcher = patch("requests.get")

        mock_get = cls.get_patcher.start()
        # Side effect to return different JSONs depending on the call
        mock_get.side_effect = [
            MagicMock(json=lambda: cls.org_payload),
            MagicMock(json=lambda: cls.repos_payload),
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher after tests."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repos."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos returns only apache2 licensed repos."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )

