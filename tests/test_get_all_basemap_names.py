#!/usr/bin/env python
import unittest
from unittest.mock import patch
from chartops import common


class TestGetAllBasemapNames(unittest.TestCase):

    def test_simple_map_provider_in_basemaps(self):
        names = common.get_all_basemap_names()
        self.assertIn('OpenTopoMap', names)
    
    def test_nested_map_provider_in_basemaps(self):
        names = common.get_all_basemap_names()
        self.assertIn('Esri.WorldImagery', names)

    def test_all_map_names_are_strings(self):
        names = common.get_all_basemap_names()
        self.assertTrue(all(isinstance(name, str) for name in names))

    def test_no_duplicate_map_names(self):
        names = common.get_all_basemap_names()
        self.assertEqual(len(names), len(set(names)))


    def test_expected_map_names_from_mocked_xyz(self):
        mock_xyz = {
            'SimpleMap': {'url': '...'},
            'NestedMap': {
                'SubA': {'url': '...'},
                'SubB': {'url': '...'}
            }
        }
        with patch('chartops.common.xyz', mock_xyz):
            names = common.get_all_basemap_names()
            self.assertCountEqual(names, ['SimpleMap', 'NestedMap.SubA', 'NestedMap.SubB'])

    def test_empty_xyz_returns_empty_list(self):
        with patch('chartops.common.xyz', {}):
            names = common.get_all_basemap_names()
            self.assertEqual(names, [])