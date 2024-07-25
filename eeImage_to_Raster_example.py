# Import libraries
import os
import ee
import geemap
import rasterio
from pyproj import CRS
from rasterio.warp import transform_bounds

# Initialize a class for GEE image acquistion
class GEE_Image_Download():

    def getRasterData(self, reference_raster):
        raster = rasterio.open(reference_raster)
        return raster

    def get_eeGeometry(self, raster):
        # Bounds
        bounds = raster.bounds
        # Projections
        my_proj = raster.crs
        wgs84_proj = CRS.from_epsg(4326) 
        # Convert raster bounds to WGS84 
        minx, miny, maxx, maxy = transform_bounds(my_proj, wgs84_proj, *bounds)
        poly = ee.Geometry.Rectangle(minx, miny, maxx, maxy)
        return poly

    def get_eeProjection(self, raster):
        crs = raster.crs.to_wkt()
        transform = raster.transform.to_gdal()
        ee_proj = ee.Projection(crs, transform)
        return ee_proj

    def download_eeImg_from_GEE(self, ee_geometry, ee_Image, ee_proj, resolution, resampling_type, output_filename):
        geemap.download_ee_image(image=ee_Image, filename=output_filename, region=ee_geometry, crs=ee_proj, scale=resolution, resampling=resampling_type)

    def MainProcess(self, reference_raster, ee_Image, resolution, resampling_type, output_filename):
        raster = self.getRasterData(reference_raster)
        ee_geometry = self.get_eeGeometry(raster)
        ee_proj = self.get_eeProjection(raster)
        self.download_eeImg_from_GEE(ee_geometry, ee_Image, ee_proj, resolution, resampling_type, output_filename)


# Initialize the GEE_Image_Download class
GEE_Processing_Engine = GEE_Image_Download()

# Initialize Earth Engine
#ee.Authenticate()
ee.Initialize(opt_url='https://earthengine-highvolume.googleapis.com')

# Inputs
reference_raster = "D:/Pass/Verra/Jurisdictions/Acre/Modeling/TIF/Acre_Mask.tif" #binary image
ee_Image = ee.Image("NASA/NASADEM_HGT/001").select('elevation')
resolution = 30
resampling_type = "bicubic" # choose from: 'near', 'bilinear', 'bicubic' or 'average'
output_filename = "D:/Pass/Verra/Jurisdictions/Acre/ee/Acre_Elevation.tif"

# Execute Main Code Block
GEE_Processing_Engine.MainProcess(reference_raster, ee_Image, resolution, resampling_type, output_filename)

