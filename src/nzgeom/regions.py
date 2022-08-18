"""access polygons describing New Zealand council regions
"""

from importlib.resources import files
from pathlib import Path
import geopandas as gpd


class NZRegions(object):
    """container class for NZ region polygons"""

    def __init__(self):
        fname = files("nzgeom.data").joinpath(
            "regions/regional-council-2018-generalised.gpkg"
        )
        if not Path(fname).exists:
            raise FileNotFoundError(f"{fname} does not exist")
        self.gdf = gpd.read_file(fname)

    def list_regions(self):
        """print the available region names"""
        print(self.gdf.REGC2018_V1_00_NAME.to_string(index=False))

    def get_region_geodataframe(self, region_name):
        """produce GeoDataFrame containing a polygon representing a specified region of NZ
        """
        if not self.gdf.REGC2018_V1_00_NAME.str.contains(region_name).any():
            raise ValueError(
                f"{region_name} not available. Use list_regions() method to show list"
                " of available regions."
            )
        return self.gdf.loc[self.gdf.REGC2018_V1_00_NAME == region_name]

    def get_region_polygon(self, region_name):
        """return a shapely polygon representing a specified region of NZ"""
        reg_gdf = self.get_region_geodataframe(region_name)
        assert reg_gdf.shape[0] == 1
        return reg_gdf.geometry.iloc[0]
