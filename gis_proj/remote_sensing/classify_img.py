# SIMPLE UNSUPERVISED CLASSIFICATION using histogram to group pixels
# uses numpy to return the arrays of frequencies and range of bin values.
# use lut (LOOK UP TABLE) an arbitrary color pallette that's used to assign colors to the 20 unsupervised classes.

import os
#GDAL requires coordinate system so set the env path proj\proj.db, also point to GDAL data
os.environ['PROJ_LIB'] = '..\\Lib\\site-packages\\osgeo\\data\\proj'
os.environ['GDAL_DATA'] = '..\\Lib\\site-packages\\osgeo\\data'

from osgeo import gdal, gdal_array, osr




# Input file name (thermal image)
src = "..\\..\\RawFiles\\thermal.tif"
# Output file name
tgt = "..\\..\\ProcessedFiles\\classified.jpg"

#Load the image to numpy array
srcArr = gdal_array.LoadFile(src)

#create histogram for our image to put in 20 bins (lut)
classes = gdal_array.numpy.histogram(srcArr, bins=20)[1]
# print(classes)

# Color look-up table (LUT) Arbitrary - must be len(classes)+1. Use these LUT color ranges to visualize
# Specified as R, G, B tuples
lut = [[255, 0, 0], [191, 48, 48], [166, 0, 0], [255, 64, 64], [255, 115, 115], [255, 116, 0], [191, 113, 48], [255, 178, 115], [0, 153, 153], [29, 115, 115],
       [0, 99, 99], [166, 75, 0], [0, 204, 0], [51, 204, 204], [255, 150, 64], [92, 204, 204], [38, 153, 38], [0, 133, 0], [57, 230, 57], [103, 230, 103], 
       [184, 138, 0]]

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

output = gdal_array.SaveArray(rgb.astype(gdal_array.numpy.uint8), tgt, format="JPEG")
output = None
