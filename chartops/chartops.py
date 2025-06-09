from chartops import common
from ipyleaflet import Map as iPyLeafletMap
from ipyleaflet import LayersControl, basemap_to_tiles

class Map(iPyLeafletMap):
    def add_basemap(self, basemap_name: str, **kwargs) -> None:
        basemap = common.resolve_basemap_name(basemap_name)
        basemap_tiles = basemap_to_tiles(basemap, **kwargs)
        basemap_tiles.base = True
        basemap_tiles.name = basemap_name
        self.add(basemap_tiles)
      
    def add_layer_control(self):
        self.add(LayersControl(position='topright'))

    def add_vector(self):
        pass