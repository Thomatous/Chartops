import xyzservices.providers as xyz
from typing import Union, Any
from matplotlib.colors import LinearSegmentedColormap


def resolve_basemap_name(basemap_name: str) -> Any:
    """
    Resolve a basemap name into an xyzservices object.

    Args:
    basemap_name (str): Dot-separated name of the basemap (e.g., 'Esri.WorldImagery').

    Returns:
        Any: An xyzservices object, compatible with both folium and ipyleaflet.

    Raises:
        AttributeError: If the basemap name is not valid.
    """
    provider = xyz
    for part in basemap_name.split("."):
        if hasattr(provider, part):
            provider = getattr(provider, part)
        else:
            raise AttributeError(f"Unsupported basemap: {basemap_name}")
    return provider


def resolve_colormap(colormap: Union[str, dict, None]) -> Any:
    """
    Resolve a colormap input to a matplotlib colormap object or string name
    usable by localtileserver.

    Args:
        colormap (str or dict or matplotlib.colors.Colormap or None): The input colormap.
            - If dict, creates and returns a LinearSegmentedColormap.
            - If str, returns as is (assumed built-in matplotlib colormap name).
            - If None, returns None.

    Returns:
        matplotlib.colors.Colormap or str or None: The resolved colormap suitable
        for passing to localtileserver.

    Raises:
        ValueError: If colormap dict is invalid or unknown type is passed.
    """
    if colormap is None:
        return None
    if isinstance(colormap, dict):
        return LinearSegmentedColormap("custom", colormap)
    if isinstance(colormap, str):
        return colormap
    raise ValueError(f"Invalid colormap argument: expected str, dict, or matplotlib.colors.Colormap, got {type(colormap)}")