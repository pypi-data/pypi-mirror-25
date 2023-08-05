#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `xml_delta` package."""


import unittest
from click.testing import CliRunner

from xml_delta import delta_task
from xml_delta import cli


class Testgiaola_xml_delta(unittest.TestCase):
    """Tests for `xml_delta` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'xml_delta.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
