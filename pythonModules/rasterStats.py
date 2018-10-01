#!/bin/env python

import sys

from osgeo import gdal, osr
from osgeo import gdalconst
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm, colors

from bilinear_interpolate import *

import raster


rasterArray = raster.readRasterBandAsArray(sys.argv[1], 1)

min  = np.nanmin(rasterArray)
max  = np.nanmax(rasterArray)
mean = np.nanmean(rasterArray)
medn = np.nanmedian(rasterArray)
std  = np.nanstd(rasterArray)

print('{: 8.2f} {: 8.2f} {: 8.2f} {: 8.2f} {: 8.2f}'.format(min, max, mean, medn, std))

