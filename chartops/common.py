from typing import Any


def resolve_basemap_name(basemap_name: str) -> Any:
    from ipyleaflet import basemaps

    basemaps_obj = basemaps
    for basemap_name_part in basemap_name.split("."):
        if hasattr(basemaps_obj, basemap_name_part):
            basemaps_obj = getattr(basemaps_obj, basemap_name_part)
        else:
            raise AttributeError(f"Unsupported basemap: {basemap_name}")
    return basemaps_obj
