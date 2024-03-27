# For this example, we'll take a subset of our Landsat 8 thermal image to isolate a group of barrier islands in the Gulf of Mexico.
# The islands appear white as the sand is hot and the cooler water appears black

# GOAL IS TO """AUTOMATICALLY EXTRACT 3 ISLANDS IN THE IMAGE AS SHAPEFILE""".

# For example, the water has a wide range of pixel values, as do the islands themselves. If we just want to extract the islands themselves, 
# we need to push all the pixel values into just two bins to make the image black and white. This technique is called thresholding.

import os
#GDAL requires coordinate system so set the env path proj\proj.db, also point to GDAL data
os.environ['PROJ_LIB'] = '..\\Lib\\site-packages\\osgeo\\data\\proj'
os.environ['GDAL_DATA'] = '..\\Lib\\site-packages\\osgeo\\data'

from osgeo import gdal, gdal_array, osr, ogr

# Input file name (thermal image)
src = "..\\..\\RawFiles\\islands_thermal.tif"
# Output file name
tgt = "..\\..\\ProcessedFiles\\islands_classified.tiff"

#Load the image to numpy array
srcArr = gdal_array.LoadFile(src)

#create histogram for our image to put in 20 bins (lut)
classes = gdal_array.numpy.histogram(srcArr, bins=2)[1]
# print(classes)

# Color look-up table (LUT) Arbitrary - must be len(classes)+1. Use these LUT color ranges to visualize
# Specified as R, G, B tuples
lut = [[255, 0, 0], [0, 0, 0], [255, 255, 255]]

# Starting value for classification
start = 1
# return a new array of given shape and type, filled with zeros
rgb = gdal_array.numpy.zeros((3, srcArr.shape[0], srcArr.shape[1], ), gdal_array.numpy.float32)
# print(srcArr.shape[0])
# print(srcArr.shape[1])

# Process all classes and assign colors
for i in range(len(classes)):
    mask = gdal_array.numpy.logical_and(start <= srcArr, srcArr <= classes[i])
    for j in range(len(lut[i])):
        rgb[j] = gdal_array.numpy.choose(mask, (rgb[j], lut[i][j]))
    start = classes[i]+1

gdal_array.SaveArray(rgb.astype(gdal_array.numpy.uint8), tgt, format="GTIFF", prototype=src) 
output = None

