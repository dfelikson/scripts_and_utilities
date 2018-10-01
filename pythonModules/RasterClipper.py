#!/bin/env python
# --------------
# Import modules
# --------------
import os, sys, argparse, datetime
import numpy as np

sys.path.append('/home/student/denis/ScriptsAndUtilities/pythonModules')
from RasterClipperFunctions import *
#sys.path.append('/Users/denisfelikson/Google Drive/Research/Projects/CentralWestGrISGlaciers/Analysis/climate/RACMO')
#from RACMOutilities import *

import raster


# ----------------------
# Command line arguments
# ----------------------
parser = argparse.ArgumentParser()
parser.add_argument('raster', type=str)
parser.add_argument('clipfile', type=str, default='')
parser.add_argument('outputfile', type=str)
parser.add_argument('--basin', type=float)
parser.add_argument('--feature', type=int)
parser.add_argument('--cropraster', action='store_true')

args = parser.parse_args()


# ----------
# Processing
# ----------
# Read raster
rasterArray = raster.readRasterBandAsArray(args.raster, 1)
geotransform = raster.getCoordinates(args.raster, 1)

# Clip raster using the basin field
if args.basin is not None:
   (xClip, yClip) = basinUnionPolygon(args.clipfile, args.basin)
if args.feature is not None:
   (xClip, yClip) = selectFeature(args.clipfile, args.feature)

rasterClipped = clipImage(rasterArray, xClip, yClip, geotransform)

# Crop the raster down to valid values only (not the original size of the raster)
if args.cropraster:
   validrows, validcols = np.where(~np.isnan(rasterClipped))
   firstvalidrow = np.min(validrows)
   lastvalidrow  = np.max(validrows)
   firstvalidcol = np.min(validcols)
   lastvalidcol  = np.max(validcols)

   rasterClipped = rasterClipped[firstvalidrow:lastvalidrow, firstvalidcol:lastvalidcol]
   geotransform = (geotransform[0] + firstvalidcol*geotransform[1], geotransform[1], geotransform[2], geotransform[3] + firstvalidrow*geotransform[5], geotransform[4], geotransform[5])

# Write clipped raster
raster.writeArrayAsRasterBand(args.outputfile,geotransform,rasterClipped,-9999)

