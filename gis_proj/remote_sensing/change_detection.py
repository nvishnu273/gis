# Hurricane before and after change detection
# 1. TAKE 2 GEO-REGISTERED IMAGES and  images of the EXACT SAME AREA from TWO DIFF DATES and automatically identifying differences
# Take hurricane AFFECTED AREAS - Subtract IMAGE1 from IMAGE2 - VERY SIMPLISTIC, (((doesn't isolate the type of CHANGE)))
# Normally, you would use two identical band combinations, but these samples will work for our purposes

import os
#GDAL requires coordinate system so set the env path proj\proj.db, also point to GDAL data
os.environ['PROJ_LIB'] = '..\\Lib\\site-packages\\osgeo\\data\\proj'
os.environ['GDAL_DATA'] = '..\\Lib\\site-packages\\osgeo\\data'

from osgeo import gdal, gdal_array, osr, ogr
import numpy as np

# "Before" image
im1 = "..\\..\\RawFiles\\hurricane_change\\before\\before.tif"
# "After" image
im2 = "..\\..\\RawFiles\\hurricane_change\\after\\after.tif"

# Load before and after into arrays
ar1 = gdal_array.LoadFile(im1).astype(np.int8)
ar2 = gdal_array.LoadFile(im2)[1].astype(np.int8)

# Perform a simple array difference on the images
diff = ar2 - ar1

# DIVIDE THE DIFFERENCE INTO 5 CLASSES
# Set up our classification scheme to try
# and isolate significant changes
classes = np.histogram(diff, bins=5)[1]


# we set our color table to use black to mask the lower classes
# We do this to filter water and roads because they are darker in the image
# The color black is repeated to mask insignificant changes
lut = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 255, 0], [255, 0, 0]]

# Assign colors to remaining classes
# Starting value for classification
start = 1
# Set up the output image
rgb = np.zeros((3, diff.shape[0], diff.shape[1], ), np.int8)
# Process all classes and assign colors
for i in range(len(classes)):
    mask = np.logical_and(start <= diff, diff <= classes[i])
    for j in range(len(lut[i])):
        rgb[j] = np.choose(mask, (rgb[j], lut[i][j]))
    start = classes[i]+1    

# Save the output image
output = gdal_array.SaveArray(rgb, "..\\..\\ProcessedFiles\\change.tif", format="GTiff", prototype=im2)
output = None
