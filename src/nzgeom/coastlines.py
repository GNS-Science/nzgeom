from importlib.resources import files
import geopandas as gpd
import spatialpandas as spd

# EPSG:4326 - WGS 84, latitude/longitude coordinate system based on the Earth's
# center of mass, used by the Global Positioning System among others.
LATLON = "EPSG:4326"  # https://epsg.io/4326


def _geopackage_to_gpd_geodataframe(fname):
    """return a geopandas GeoDataFrame containing the NZ coastline"""
    gdf = gpd.read_file(fname).to_crs(LATLON)
    return gdf


def _geopackage_to_spd_geodataframe(fname):
    """return a spatialpandas GeoDataFrame containing the NZ coastline

    `spatialpandas <https://github.com/holoviz/spatialpandas>`_ is designed to
    work nicely with `holoviz <https://holoviz.org/>`_.

    """
    gdf = _geopackage_to_gpd_geodataframe(fname)

    # filter out shapely deprecation warning triggered by spatialpandas
    # https://shapely.readthedocs.io/en/stable/migration.html#creating-numpy-arrays-of-geometry-objects
    import warnings
    from shapely.errors import ShapelyDeprecationWarning

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)
        return spd.GeoDataFrame(gdf)


def get_NZ_coastlines(fmt: str = "geopandas"):
    """return a GeoDataFrame containing the NZ coastline

    The format of the GeoDataFrame can be either `geopandas
    <https://geopandas.org/>`_ (default) or `spatialpandas
    <https://github.com/holoviz/spatialpandas>`_.

    ARGS:
    fmt: string: {"geopandas"} | "spatialpandas"
    """
    fname = files("nzgeom.data").joinpath(
        "coastlines/nz-coastlines-and-islands-polygons-topo-150k.gpkg"
    )
    if fmt == "geopandas":
        return _geopackage_to_gpd_geodataframe(fname)
    elif fmt == "spatialpandas":
        return _geopackage_to_spd_geodataframe(fname)
    else:
        raise ValueError('fmt must be on of ["geopandas", "spatialpandas"]')
