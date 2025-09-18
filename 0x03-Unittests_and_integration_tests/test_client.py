#!/usr/bin/env python3
"""Unittests for client.py (GithubOrgClient)
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient.org"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""
        # Arrange
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)

        # Act
        result = client.org

        # Assert
        self.assertEqual(result, {"login": org_name})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns expected URL from org payload"""
        with patch("client.GithubOrgClient.org", new_callable=unittest.mock.PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/test/repos"}
            client = GithubOrgClient("test")

            result = client._public_repos_url

            self.assertEqual(result, "https://api.github.com/orgs/test/repos")


if __name__ == "__main__":
    unittest.main()
