"""access polygons describing New Zealand coastlines.
"""

from typing import Tuple
from importlib.resources import files
import geopandas as gpd
from shapely.geometry import Polygon
import numpy as np

# EPSG:4326 - WGS 84, latitude/longitude coordinate system based on the Earth's
# center of mass, used by the Global Positioning System among others.
LATLON = "EPSG:4326"  # https://epsg.io/4326


def _geopackage_to_gpd_geodataframe(fname: str) -> gpd.GeoDataFrame:
    """return a geopandas GeoDataFrame containing the NZ coastline

    helper function for get_NZ_coastlines()
    """
    gdf = gpd.read_file(fname).to_crs(LATLON)
    return gdf


def _clip_to_bbox(
    gdf: gpd.GeoDataFrame, bbox: Tuple[float, float, float, float]
) -> gpd.GeoDataFrame:
    """clip a geopandas.geodataframe to a bounding box

    ARGS:
        gdf: the geopandas.GeoDataFrame to be clipped
        bbox: optional 4-tuple of floats specifying a bounding box. If
            specified, the coastlines will be clipped to the bounding box. The
            box is specified in form [LL lon, LL lat, UR lon, UR lat ]. LL =
            lower left, UR = upper right.

    RETURNS:
        gdf, clipped to the rectangle specified by bbox
    """
    bboxx = [bbox[0], bbox[2]]
    bboxy = [bbox[1], bbox[3]]
    bbox = Polygon(
        [
            (bboxx[0], bboxy[0]),
            (bboxx[0], bboxy[1]),
            (bboxx[1], bboxy[1]),
            (bboxx[1], bboxy[0]),
            (bboxx[0], bboxy[0]),
        ]
    )
    gdf_bbox = gpd.GeoDataFrame({"geometry": [bbox]}, crs=LATLON)
    gdf_cropped = gpd.clip(gdf, gdf_bbox)
    return gdf_cropped


def get_NZ_coastlines(
    include_chatham_islands: bool = False,
    include_kermadec_islands: bool = False,
    bbox: Tuple[float, float, float, float] = (None, None, None, None),
) -> gpd.GeoDataFrame:
    """return a geopandas.GeoDataFrame containing the NZ coastline.

    The Chatham Islands and the Kermadec Islands are east of 180 degress
    longitude. In many plotting packages (e.g. matplotlib) with default options
    including these islands in a plot of New Zealand causes the plot's
    horizontal axis to span roughly -177 deg E to 177 deg E, that is, the whole
    world.

    ARGS:
        include_chatham_islands: if true, include the coastline of the Chatham
            Islands in the returned geodataframe.
        include_kermadec_islands: if true, include the coastline of the Kermadec
            Islands in the returned geodataframe.
        bbox: optional 4-tuple of floats specifying a bounding box. If
            specified, the coastlines will be clipped to the bounding box. The
            box is specified in form [LL lon, LL lat, UR lon, UR lat ]. LL =
            lower left, UR = upper right.

    RETURNS:
        a `geopandas.GeoDataFrame
        <https://geopandas.org/en/stable/docs/user_guide/data_structures.html#geodataframe>`_
        object containing multipolygons representing New Zealand's coastlines.

    """
    fname = files("nzgeom.data").joinpath(
        "coastlines/nz-coastlines-and-islands-polygons-topo-150k.gpkg"
    )
    gdf = _geopackage_to_gpd_geodataframe(fname)
    if not include_kermadec_islands:
        # testing for "!= True" (rather than "== False") gets both False
        # (grp_name does not contain Kermadec) and None (grp_name was not set at
        # all)
        gdf = gdf.loc[gdf["grp_name"].str.contains("Kermadec") != True]
    if not include_chatham_islands:
        gdf = gdf.loc[gdf["grp_name"].str.contains("Chatham") != True]
    if np.all([val is not None for val in bbox]):
        print(f"clipping to bounding box {bbox}")
        gdf = _clip_to_bbox(gdf, bbox)
    return gdf
