from math import *
import numpy as np
from osgeo import gdal,ogr
import struct

from scipy.interpolate import interp1d

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('shapefile', type=str, help='shapefile filename')
parser.add_argument('spacing', type=float, help='spacing in map coordinates')

args = parser.parse_args()
shp_filename = args.shapefile
spacing = args.spacing

ds = ogr.Open(shp_filename)
lyr = ds.GetLayer()

# Read in all points from polyline in shapefile
mxy = np.array([0,0])
for i in range(lyr.GetFeatureCount()):
   feat = lyr.GetFeature(i)
   geom = feat.GetGeometryRef()
   for iPoint in range(geom.GetPointCount()):
      mx,my = geom.GetX(iPoint), geom.GetY(iPoint)  #coord in map units
      mxy = np.vstack((mxy, [mx, my]))

# Delete first row (initialized as [0,0])
mxy = np.delete(mxy, (0), axis=0)

# Calculate distance along line
d = np.array([0])
for i, xy in enumerate(mxy):
   if i > 0:
      d = np.append( d, sqrt( (mxy[i,0]-mxy[i-1,0])**2 + (mxy[i,1]-mxy[i-1,1])**2 ) )

d = np.cumsum(d)

# Resample
fx = interp1d(d, mxy[:,0])
fy = interp1d(d, mxy[:,1])

dnew = np.arange(0, d[-1], spacing)
xnew = fx(dnew)
ynew = fy(dnew)

# Output
for i, x in enumerate(xnew):
   print x, ynew[i]

