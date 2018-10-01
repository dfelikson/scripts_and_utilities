from osgeo import gdal,ogr
import struct

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('rasterfilename', type=str, nargs=1, help='raster filename')
parser.add_argument('pixelsfilename', type=str, nargs=1, help='pixels filename')

args = parser.parse_args()
src_filename = args.rasterfilename[0]
pix_filename = args.pixelsfilename[0]

src_ds = gdal.Open(src_filename) 
gt = src_ds.GetGeoTransform()
rb = src_ds.GetRasterBand(1)

f = open(pix_filename, 'r')
for line in f:
   px = int(float(line.split()[0]))
   py = int(float(line.split()[1]))

   if (px >= 0) and (py >= 0) and (px < src_ds.RasterXSize) and (py < src_ds.RasterYSize):
      data = rb.ReadAsArray(px,py,1,1)
   else:
      data = [[-9999]]
       
   print px, py, data[0][0]

