import geopandas as gpd
from typing import Union
from pathlib import Path
from ipyleaflet import Map as iPyLeafletMap
from ipyleaflet import LayersControl, basemap_to_tiles, GeoJSON, ImageOverlay
from chartops import common


class Map(iPyLeafletMap):
    def add_basemap(self, basemap_name: str, **kwargs) -> None:
        """
        Add a basemap to the ipyleaflet map.

        Args:
            basemap_name (str): Name of the basemap to add. Resolved with xyzservices.
            **kwargs (dict): Extra kwargs to pass to basemap_to_tiles.

        Returns:
            None
        """
        basemap = common.resolve_basemap_name(basemap_name)
        basemap_tiles = basemap_to_tiles(basemap, **kwargs)
        basemap_tiles.base = True
        basemap_tiles.name = basemap_name
        self.add(basemap_tiles)

    def add_layer_control(self, position: str = "topright") -> None:
        """
        Add a layer control to the map.

        Args:
            position (str, optional): Position of the layer control. Valid positions are "topright", "topleft", "bottomright", "bottomleft". Default is "topright".

        Returns:
            None

        Raises:
            ValueError: If the position is not valid.
        """
        valid_positions = ["topright", "topleft", "bottomright", "bottomleft"]
        if position not in valid_positions:
            raise ValueError(
                f"Invalid position '{position}'. Valid positions are: {valid_positions}"
            )
        self.add(LayersControl(position=position))

    def add_vector(self, filepath: Union[Path, str], name: str = "", **kwargs) -> None:
        """
        Add a vector layer to the map.

        Args:
            filepath (Path or str): Path to the vector dataset or URL to a remote file.
            name (str): Name of the layer. Defaults to ''..
            **kwargs (dict): Additional styling options for the layer. Valid options include:
                - color: str (default: 'blue')
                - weight: int (default: 2)
                - fillOpacity: float (default: 0.1)

        Returns:
            None

        Raises:
            FileNotFoundError: If the local filepath does not exist.
            ValueError: If the vector data cannot be read or converted to GeoJSON, or if styling options are invalid.
        """
        if isinstance(filepath, Path) and not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        color = kwargs.get("color", "blue")
        if not isinstance(color, str):
            raise ValueError(f"color must be a string, got {type(color)}")

        weight = kwargs.get("weight", 2)
        if not isinstance(weight, int):
            raise ValueError(f"weight must be an integer, got {type(weight)}")

        fillOpacity = kwargs.get("fillOpacity", 0.1)
        if not isinstance(fillOpacity, (int, float)) or not (0 <= fillOpacity <= 1):
            raise ValueError("fillOpacity must be a float between 0 and 1")

        try:
            gdf = gpd.read_file(filepath)
            geojson = gdf.__geo_interface__
            layer = GeoJSON(
                data=geojson,
                name=name,
                style={"color": color, "weight": weight, "fillOpacity": fillOpacity},
            )
            self.add(layer)
        except Exception as e:
            raise ValueError(f"Failed to add vector layer from {filepath}: {e}")

    def add_raster(
            self,
            url: Union[str, Path],
            name: str = "",
            opacity: float = 1.0,
            colormap: Union[str, dict] = None,
            indexes: Union[int, list[int]] = None,
            vmin: float = None,
            vmax: float = None,
            nodata: Union[int, float] = None,
            **kwargs
        ) -> None:
        
        from localtileserver import TileClient, get_leaflet_tile_layer
        client = TileClient(str(url))
        
        self.center = client.center()
        self.zoom = client.default_zoom

        tile_layer = get_leaflet_tile_layer(
            client,
            indexes=indexes,
            colormap=colormap,
            vmin=vmin,
            vmax=vmax,
            nodata=nodata,
            opacity=opacity,
            **kwargs
        )
        tile_layer.name = name or Path(url).stem
        self.add(tile_layer)
