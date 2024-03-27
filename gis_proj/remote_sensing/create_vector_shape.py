
# islands are isolated and our script will be able to identify them as polygons and save them as shapefile.
# GDAL has a method called Polygonize() that does that. It groups all sets of isolated pixels in an image and saves them as a feature dataset.
# IMAGE INPUT MASK: Remove all Water (BLACK) and only take the white
# Another area to note in the script is that we copy the georeferencing information from our source image to our shapefile to geolocate it properly

import os
#GDAL requires coordinate system so set the env path proj\proj.db, also point to GDAL data
os.environ['PROJ_LIB'] = '..\\Lib\\site-packages\\osgeo\\data\\proj'
os.environ['GDAL_DATA'] = '..\\Lib\\site-packages\\osgeo\\data'

from osgeo import gdal, gdal_array, osr, ogr

# Input file name (thermal image)
src = "..\\..\\ProcessedFiles\\islands_classified.tiff"
# Output file name
tgt = "..\\..\\ProcessedFiles\\island_layer\\island_layer.shp"
# OGR layer name
tgtLayer = "island_layer"

# Open the input raster
srcDS = gdal.Open(src)
# Grab the first band
band = srcDS.GetRasterBand(1) # GetRasterBand??? Water?? Black??
# Force gdal to use the band as a mask
mask = band

# Set up the output shapefile
driver = ogr.GetDriverByName("ESRI Shapefile")
shp = driver.CreateDataSource(tgt)

# copy the spatial reference file from the source image to shapefile, to locate it in Earth
# Copy the spatial reference
srs = osr.SpatialReference()
srs.ImportFromWkt(srcDS.GetProjectionRef())
layer = shp.CreateLayer(tgtLayer, srs=srs)

# Set up the dbf file (ShareFile Attributes)
fd = ogr.FieldDefn("DN", ogr.OFTInteger)
layer.CreateField(fd)
dst_field = 0

#Finally extract Polygons
extract = gdal.Polygonize(band, mask, layer, dst_field, [], None) 