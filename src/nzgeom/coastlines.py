from importlib.resources import files
import geopandas as gpd

# EPSG:4326 - WGS 84, latitude/longitude coordinate system based on the Earth's
# center of mass, used by the Global Positioning System among others.
LATLON = "EPSG:4326"  # https://epsg.io/4326


def _geopackage_to_gpd_geodataframe(fname: str) -> gpd.GeoDataFrame:
    """return a geopandas GeoDataFrame containing the NZ coastline

    helper function for get_NZ_coastlines()
    """
    gdf = gpd.read_file(fname).to_crs(LATLON)
    return gdf


def get_NZ_coastlines(
    include_chatham_islands: bool = False, include_kermadec_islands: bool = False
) -> gpd.GeoDataFrame:
    """return a geopandas.GeoDataFrame containing the NZ coastline.

    ARGS:
        include_chatham_islands: if true, include the coastline of the Chatham
            Islands in the returned geodataframe.
        include_kermadec_islands: if true, include the coastline of the Kermadec
            Islands in the returned geodataframe.

    RETURNS:
        a `geopandas.GeoDataFrame
        <https://geopandas.org/en/stable/docs/user_guide/data_structures.html#geodataframe>`_
        object containing multipolygons representing New Zealand's coastlines.

    NOTES:

    The Chatham Islands and the Kermadec Islands are east of 180 degress
    longitude. Including these islands in a plot of New Zealand causes the
    plot's horizontal axis to span roughly -177 deg E to 177 deg E, that is, the
    whole world.

    """
    fname = files("nzgeom.data").joinpath(
        "coastlines/nz-coastlines-and-islands-polygons-topo-150k.gpkg"
    )
    gdf = _geopackage_to_gpd_geodataframe(fname)
    if not include_kermadec_islands:
        gdf = gdf.loc["Kermadec" not in gdf["grp_name"]]
    if not include_chatham_islands_islands:
        gdf = gdf.loc["Chatham" not in gdf["grp_name"]]
    return gdf
