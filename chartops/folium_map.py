import folium
from chartops import common
from pathlib import Path

class Map(folium.Map):
    def add_basemap(self, basemap_name: str, **kwargs) -> None:
        basemap = common.resolve_basemap_name(basemap_name)
        folium.TileLayer(
            tiles=basemap.url,
            attr=basemap.attribution,
            name=basemap_name,
            **kwargs
        ).add_to(self)


    def add_layer_control(self, position: str = "topright") -> None:
        folium.LayerControl().add_to(self)

    def add_vector(self, filepath: Path | str, name: str = "", **kwargs) -> None:
        """
        Add a vector layer to the map.

        Parameters
        ----------
        filepath : Path or str
                Path to the vector dataset or URL to a remote file.
        name : str (default: '')
            Name of the layer.
        **kwargs : dict
            Additional styling options for the layer. Valid options include:
            - color: str (default: 'blue')
            - weight: int (default: 2)
            - fillOpacity: float (default: 0.1)

        Returns
        -------
        None

        Raises
        ------
        FileNotFoundError
            If the local filepath does not exist.
        ValueError
            If the vector data cannot be read or converted to GeoJSON, or if styling options are invalid.
        """
        pass