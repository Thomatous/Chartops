import folium
from chartops import common
from pathlib import Path
import geopandas as gpd

class Map(folium.Map):
    def add_basemap(self, basemap_name: str, **kwargs) -> None:
        basemap = common.resolve_basemap_name(basemap_name)
        folium.TileLayer(
            tiles=basemap.url,
            attr=basemap.attribution,
            name=basemap_name,
            **kwargs
        ).add_to(self)

    def add_layer_control(self) -> None:
        folium.LayerControl().add_to(self)

    def add_vector(self, filepath: Path | str, name: str, **kwargs) -> None:
        color = kwargs.get("color", "blue")
        weight = kwargs.get("weight", 2)
        fill_opacity = kwargs.get("fillOpacity", 0.1)

        try:
            if isinstance(filepath, str) and filepath.startswith("http"):
                folium.GeoJson(
                    filepath,
                    name=name,
                    style_function=lambda feature: {
                        "color": color,
                        "weight": weight,
                        "fillOpacity": fill_opacity
                    }
                ).add_to(self)

            else:
                path = Path(filepath)
                if not path.exists():
                    raise FileNotFoundError(f"File not found: {filepath}")
                gdf = gpd.read_file(path)
                folium.GeoJson(
                    gdf,
                    name=name,
                    style_function=lambda feature: {
                        "color": color,
                        "weight": weight,
                        "fillOpacity": fill_opacity
                    }
                ).add_to(self)
        except Exception as e:
            raise ValueError(f"Failed to add vector layer from {filepath}: {e}")
