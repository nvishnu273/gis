import os
#GDAL requires coordinate system so set the env path proj\proj.db, also point to GDAL data
os.environ['PROJ_LIB'] = '..\\Lib\\site-packages\\osgeo\\data\\proj'
os.environ['GDAL_DATA'] = '..\\Lib\\site-packages\\osgeo\\data'

from osgeo import gdal, gdal_array

src = "..\\..\\RawFiles\\FalseColor\\FalseColor.tif"

# load the source image into an array
arr = gdal_array.LoadFile(src)

#swap bands 1 and 2 for natural color image
# prototype parameter: To copy spatial referential information.
# Without this argument, we'd end up with an image without georeferencing information, which could not be used in a GIS
# In this case, we specify our input image file name because the images are identical, except for the band order
output = gdal_array.SaveArray(arr[[1, 0, 2], :], "..\\..\\RawFiles\\swapped_band_files\\swap.tif", format="GTiff", prototype=src)

# Dereference output to avoid corrupted file on some platforms.
output = None