from typing import Any
from ipyleaflet import TileLayer
from xyzservices import TileProvider

def resolve_basemap_name(basemap_name: str) -> Any:
    from ipyleaflet import basemaps

    basemaps_obj = basemaps
    for basemap_name_part in basemap_name.split('.'):
        if hasattr(basemaps_obj, basemap_name_part):
            basemaps_obj = getattr(basemaps_obj, basemap_name_part)
        else:
            raise AttributeError(f"Unsupported basemap: {basemap_name}")    
    return basemaps_obj

def tileprovider_to_tilelayer(tile_provider: TileProvider, **kwargs) -> TileLayer:
    return TileLayer(
        url=tile_provider.build_url(),
        name=tile_provider.name,
        max_zoom=tile_provider["max_zoom"] if "max_zoom" in tile_provider.keys() else 22,
        visible=True,
        **kwargs
    )
