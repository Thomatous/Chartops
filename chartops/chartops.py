import rasterio
import numpy as np
import geopandas as gpd
from typing import Union
from pathlib import Path
from ipyleaflet import Map as iPyLeafletMap
from ipyleaflet import LayersControl, basemap_to_tiles, GeoJSON, ImageOverlay
from chartops import common
from rasterio.warp import transform_bounds
import base64
import io
from PIL import Image


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

    def add_raster(self, url: Union[str, Path], opacity: float = 1.0, name: str = '', colormap: Union[dict, str] = {}, **kwargs) -> None:
        with rasterio.open(url) as src:
                array = src.read()
                bounds = src.bounds

                # Convert bounds to lat/lon if necessary
                if src.crs != "EPSG:4326":
                    bounds_ll = transform_bounds(src.crs, "EPSG:4326", *bounds)
                else:
                    bounds_ll = bounds

                # Prepare image
                if array.shape[0] == 1:
                    band = array[0].astype(np.float32)
                    band_min, band_max = np.percentile(band[band != src.nodata], (2, 98))
                    norm = np.clip((band - band_min) / (band_max - band_min), 0, 1)
                    img_data = (norm * 255).astype(np.uint8)

                    if colormap:
                        import matplotlib.cm as cm
                        if isinstance(colormap, str):
                            cmap = cm.get_cmap(colormap)
                        else:
                            from matplotlib.colors import LinearSegmentedColormap
                            cmap = LinearSegmentedColormap.from_list("custom", list(colormap.values()))
                        rgba = cmap(img_data / 255.0, bytes=True)
                        img = Image.fromarray(rgba, 'RGBA')
                    else:
                        img = Image.fromarray(img_data, 'L').convert("RGBA")

                elif array.shape[0] >= 3:
                    rgb = array[:3].astype(np.float32)
                    for i in range(3):
                        b = rgb[i]
                        b_min, b_max = np.percentile(b[b != src.nodata], (2, 98))
                        rgb[i] = np.clip((b - b_min) / (b_max - b_min), 0, 1)
                    img = np.transpose((rgb * 255).astype(np.uint8), (1, 2, 0))
                    img = Image.fromarray(img, 'RGB').convert("RGBA")
                else:
                    raise ValueError("Unsupported raster format")

                # Convert image to base64 PNG
                buffer = io.BytesIO()
                img.save(buffer, format="PNG")
                data_uri = "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()

                image_bounds = [(bounds_ll[1], bounds_ll[0]), (bounds_ll[3], bounds_ll[2])]
                overlay = ImageOverlay(url=data_uri, bounds=image_bounds, opacity=opacity, name=name or Path(url).stem)
                self.add(overlay)

                # Fit map to the raster bounds
                self.fit_bounds(image_bounds)