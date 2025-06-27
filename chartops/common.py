import numpy as np
import xyzservices.providers as xyz
from typing import Any
from PIL import Image
from io import BytesIO
from base64 import b64encode


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


def encode_array(array: np.ndarray) -> str:
    array = np.moveaxis(array, 0, -1)
    nan_mask = ~np.isnan(array) * 1 
    nan_mask *= 255
    nan_mask = nan_mask.astype(np.uint8)
    array_max = np.nanmax(array)
    array_min = np.nanmin(array)

    array = np.nan_to_num(array)

    array = np.clip((array - array_min) / (array_max - array_min) * 255, 0, 255)
    array = array.astype(np.uint8)
    
    image = Image.fromarray(np.squeeze(np.stack([array, array, array, nan_mask], axis=-1)), mode="RGBA")
    
    #Convert the image to bytes and encode in the url
    s = BytesIO()
    image.save(s, 'png')
    data = b64encode(s.getvalue())
    data = data.decode('ascii')
    imgurl = 'data:image/png;base64,' + data

    return imgurl