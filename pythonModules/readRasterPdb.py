#!/bin/env python

from osgeo import gdal, osr
from osgeo import gdalconst
import numpy

import sys

filename = sys.argv[1]

raster = gdal.Open(filename, gdalconst.GA_ReadOnly)
rasterBand = raster.GetRasterBand(1)
rasterBandArray = rasterBand.ReadAsArray(0, 0, raster.RasterXSize, raster.RasterYSize)
import pdb; pdb.set_trace()

# Other stuff
rasterBandNoDataValue = rasterBand.GetNoDataValue()

