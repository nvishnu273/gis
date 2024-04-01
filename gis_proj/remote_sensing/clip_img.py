# Rasterize the shapefile. Convert from raster to vector (of the shapefile of the area that we want to clip)
# Turn the shapefile image into a binary mask or filter to only grab the image pixels we want within the shapefile boundary.
# Filter the satellite image through the mask.
# Discard satellite image data outside the mask.
# Save the clipped satellite image as clip.tif.


import os
#GDAL requires coordinate system so set the env path proj\proj.db, also point to GDAL data
os.environ['PROJ_LIB'] = '..\\Lib\\site-packages\\osgeo\\data\\proj'
os.environ['GDAL_DATA'] = '..\\Lib\\site-packages\\osgeo\\data'

import operator
from osgeo import gdal, gdal_array, osr
import shapefile
from PIL import Image, ImageDraw

# try:
#     import Image
#     import ImageDraw
# except:
#     from PIL import Image, ImageDraw

def imageToArray(i):
    """
    Converts a Python Imaging Library array to a gdal_array image.
    """
    # a = gdal_array.numpy.fromstring(i.tobytes(), 'b')
    a = gdal_array.numpy.frombuffer(i.tobytes(), 'b')
    
    a.shape = i.im.size[1], i.im.size[0]
    return a

def world2Pixel(geoMatrix, x, y):
    """
    Uses a gdal geomatrix (gdal.GetGeoTransform()) to calculate the pixel location of a geospatial coordinate
    """
    ulX = geoMatrix[0]
    ulY = geoMatrix[3]
    xDist = geoMatrix[1]
    yDist = geoMatrix[5]
    rtnX = geoMatrix[2]
    rtnY = geoMatrix[4]
    pixel = int((x - ulX) / xDist)
    line = int((ulY - y) / abs(yDist))
    return (pixel, line)

# raster image to clip
raster = "..\\..\\ProcessedFiles\\stretched.tif"
# Polygon shapefile used to clip
shp = "hancock"
# Name of clipped raster file(s)
output = "clipped"
# Load the source data as a gdal_array numpy array
srcArray = gdal_array.LoadFile(raster)

# Also load the image as GDAL image (because GDAL Array does not do geotransformation) and then convert it into coordinate pixels
srcImage = gdal.Open(raster)
geoTrans = srcImage.GetGeoTransform()

# Use pyshp to open the shapefile
r = shapefile.Reader("..\\..\\ShapeFiles\\hancock\\{}.shp".format(shp))

# convert shapefile bounding box coordinates to image coordinates based on our source image
minX, minY, maxX, maxY = r.bbox
ulX, ulY = world2Pixel(geoTrans, minX, maxY)
lrX, lrY = world2Pixel(geoTrans, maxX, minY)

# calculate the size of our output image based on the extents of the shapefile and take just that part of the source image:
# Calculate the pixel size of the new image
pxWidth = int(lrX - ulX)
pxHeight = int(lrY - ulY)
clip = srcArray[:, ulY:lrY, ulX:lrX]

# create a new geomatrix for the image to contain georeferencing data
geoTrans = list(geoTrans)
geoTrans[0] = minX
geoTrans[3] = maxY

# create a simple black-and-white mask image from the shapefile that will define the pixels we want to extract from the source image
# Map points to pixels for drawing the county boundary on a blank 8-bit, black and white, mask image.
pixels = []
for p in r.shape(0).points:
    pixels.append(world2Pixel(geoTrans, p[0], p[1]))

rasterPoly = Image.new("L", (pxWidth, pxHeight), 1)
# Create a blank image in PIL to draw the polygon.
rasterize = ImageDraw.Draw(rasterPoly)
rasterize.polygon(pixels, 0)

# Convert the PIL image to a NumPy array
mask = imageToArray(rasterPoly)

# Clip the image using the mask
clip = gdal_array.numpy.choose(mask, (clip, 0)).astype(gdal_array.numpy.uint8)

# Save ndvi as tiff
gdal_array.SaveArray(clip, "..\\..\\ProcessedFiles\\{}.tif".format(output), format="GTiff", prototype=raster)