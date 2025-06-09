#!/usr/bin/env python
import unittest
from ipyleaflet import basemaps, TileLayer
from chartops import common

class TestTileProviderToTileLayer(unittest.TestCase):
    
    def test_simple_tileprovider_to_tilelayer_conversion(self) -> None:
       tile_provider = getattr(basemaps, 'OpenTopoMap')
       tile_layer = common.tileprovider_to_tilelayer(tile_provider)
       self.assertIsInstance(tile_layer, TileLayer)
    
    def test_simple_tileprovider_to_tilelayer_conversion_with_kwargs(self) -> None:
       tile_provider = getattr(basemaps, 'OpenTopoMap')
       
       tile_layer = common.tileprovider_to_tilelayer(tile_provider)
       self.assertEqual(tile_layer.tile_size, 256)
             
       kwargs = {'tile_size': 512}
       tile_layer = common.tileprovider_to_tilelayer(tile_provider, **kwargs)
       self.assertEqual(tile_layer.tile_size, 512)

