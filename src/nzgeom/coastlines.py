from importlib.resources import files
import geopandas as gpd

# EPSG:4326 - WGS 84, latitude/longitude coordinate system based on the Earth's
# center of mass, used by the Global Positioning System among others.
LATLON = "EPSG:4326"  # https://epsg.io/4326


def _geopackage_to_gpd_geodataframe(fname):
    """return a geopandas GeoDataFrame containing the NZ coastline"""
    gdf = gpd.read_file(fname).to_crs(LATLON)
    return gdf


def get_NZ_coastlines():
    """return a geopandas.GeoDataFrame containing the NZ coastline"""
    fname = files("nzgeom.data").joinpath(
        "coastlines/nz-coastlines-and-islands-polygons-topo-150k.gpkg"
    )
    return _geopackage_to_gpd_geodataframe(fname)
