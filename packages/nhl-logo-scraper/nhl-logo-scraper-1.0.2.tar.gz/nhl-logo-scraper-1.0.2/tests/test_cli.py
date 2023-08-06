"""Tests for the main nhlscraper CLI module"""

from subprocess import PIPE, getoutput
from unittest import TestCase

from nhl_logo_scraper import __version__ as VERSION

class TestHelp(TestCase):
    def test_returns_usage_information(self):
        output = getoutput("nhlscraper -h")
        self.assertTrue('Usage:' in output)

        output = getoutput("nhlscraper --help")
        self.assertTrue('Usage:' in output)

class TestVersion(TestCase):
    def test_returns_version_information(self):
        output = getoutput('nhlscraper --version')
        self.assertEqual(output.strip(), VERSION);
