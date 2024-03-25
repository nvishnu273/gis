# Redistributes the pixel values across whole scale so that it is now brighter. So that instead of the range between 0-125 (when it looks darker)
# it stretches it to 0-255 so that it is now brighter.

import os
#GDAL requires coordinate system so set the env path proj\proj.db, also point to GDAL data
os.environ['PROJ_LIB'] = '..\\Lib\\site-packages\\osgeo\\data\\proj'
os.environ['GDAL_DATA'] = '..\\Lib\\site-packages\\osgeo\\data'

from osgeo import gdal, gdal_array
import operator
from functools import reduce


# create histogram
def histogram(a, bins=list(range(0, 256))):
    """
    Histogram function for multi-dimensional array.
    a = array
    bins = range of numbers to match
    """
    fa = a.flat
    n = gdal_array.numpy.searchsorted(gdal_array.numpy.sort(fa), bins)
    n = gdal_array.numpy.concatenate([n, [len(fa)]])
    hist = n[1:]-n[:-1]
    return hist

def stretch(a):
    """
    Performs a histogram stretch on gdal_array image
    """
    hist = histogram(a)
    lut = []
    for b in range(0, len(hist), 256):
        # step size
        step = reduce(operator.add, hist[b:b+256]) / 255
        # create equalization lookup table
        n = 0
        for i in range(256):
            lut.append(n / step)
            n = n + hist[i+b]
    gdal_array.numpy.take(lut, a, out=a)
    return a

src = "..\\..\\RawFiles\\swapped_band_files\\swap.tif"
arr = gdal_array.LoadFile(src)
stretched = stretch(arr)
output = gdal_array.SaveArray(arr, "..\\..\\RawFiles\\swapped_band_files\\stretched.tif", format="GTiff", prototype=src)
output = None

