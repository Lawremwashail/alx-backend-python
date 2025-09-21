#!/usr/bin/env python3
"""Unit tests and integration tests for client.GithubOrgClient."""
import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value."""
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)

        result = client.org

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, {"login": org_name})

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that GithubOrgClient.public_repos returns list of repos."""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        mock_get_json.return_value = test_payload

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
        ) as m_url:
            m_url.return_value = "https://api.github.com/orgs/test-org/repos"
            client = GithubOrgClient("test-org")

            result = client.public_repos()

            expected = ["repo1", "repo2"]
            self.assertEqual(result, expected)

            m_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test-org/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license returns correct boolean."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": payload[0],
        "repos_payload": payload[1],
        "expected_repos": [repo["name"] for repo in payload[1]],
        "apache2_repos": [
            repo["name"] for repo in payload[1]
            if repo.get("license", {}).get("key") == "apache-2.0"
        ],
    }
    for payload in TEST_PAYLOAD
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient using fixtures."""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get with side_effect."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            mock_resp = Mock()
            if url.endswith("/orgs/google"):
                mock_resp.json.return_value = cls.org_payload
            elif url.endswith("/orgs/google/repos"):
                mock_resp.json.return_value = cls.repos_payload
            return mock_resp

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test: public_repos returns expected_repos from fixtures."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test: public_repos(license='apache-2.0') returns apache2_repos."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos,
        )


if __name__ == "__main__":
    unittest.main()
