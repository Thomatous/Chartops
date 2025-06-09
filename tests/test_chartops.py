#!/usr/bin/env python

"""Tests for `chartops` package."""


import unittest

from chartops import chartops

class TestChartops(unittest.TestCase):
    """Tests for `chartops` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.map = chartops.Map()

    def tearDown(self):
        """Tear down test fixtures, if any."""
    
    def test_add_basemap(self) -> None:
        basemap_name = "OpenTopoMap"
        self.map.add_basemap(basemap_name)
