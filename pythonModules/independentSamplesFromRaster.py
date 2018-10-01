import numpy as np
from osgeo import gdal,ogr
import struct

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('rasterfilename', type=str, nargs=1, help='raster filename')
parser.add_argument('shapefilefilename', type=str, nargs=1, help='shapefile filename')

args = parser.parse_args()
src_filename = args.rasterfilename[0]
shp_filename = args.shapefilefilename[0]

src_ds = gdal.Open(src_filename) 
gt = src_ds.GetGeoTransform()
rb = src_ds.GetRasterBand(1)

ds = ogr.Open(shp_filename)
lyr = ds.GetLayer()

# Find pixels in raster
px = np.array([])
py = np.array([])
mxy = np.array([0,0])
for feat in lyr:
   geom = feat.GetGeometryRef()
   mx,my = geom.GetX(), geom.GetY()  #coord in map units

   #Convert from map to pixel coordinates.
   #Only works for geotransforms with no rotation.
   #If raster is rotated, see http://code.google.com/p/metageta/source/browse/trunk/metageta/geometry.py#493
   px = np.append(px, int((mx - gt[0]) / gt[1])) #x pixel
   py = np.append(py, int((my - gt[3]) / gt[5])) #y pixel

   mxy = np.vstack((mxy, [mx, my]))

# Delete first row (initialized as [0,0])
mxy = np.delete(mxy, (0), axis=0)

# Select unique pixels
pxy = np.transpose(np.vstack([px,py]))
b = np.ascontiguousarray(pxy).view(np.dtype((np.void, pxy.dtype.itemsize * pxy.shape[1])))
_, idx = np.unique(b, return_index=True)
idxsort = np.sort(idx)

mxyunique = mxy[idxsort]
mxunique = mxyunique[:,0]
myunique = mxyunique[:,1]

# Output
for i, x in enumerate(mxunique):
   print x, myunique[i]

