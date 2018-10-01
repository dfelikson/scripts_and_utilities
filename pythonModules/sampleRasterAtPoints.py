#!/usr/bin/env python

from osgeo import gdal,ogr
import struct
import numpy as np

from bilinear_interpolate import *

def sampleRasterAtPoint(src_ds, point, method='nearest'):
   gt = src_ds.GetGeoTransform()
   rb = src_ds.GetRasterBand(1)

   mx = point[0]
   my = point[1]
   px = int((mx - gt[0]) / gt[1])
   py = int((my - gt[3]) / gt[5])
   
   if (px >= 0) and (py >= 0) and (px < src_ds.RasterXSize) and (py < src_ds.RasterYSize):
      if method == 'nearest':
         data = rb.ReadAsArray(px,py,1,1)[0][0]
      elif method == 'bilinear':
         data = bilinear_interpolate(rb.ReadAsArray(), px, py, nodatavalues=-9999)
      else:
         data = -9999
   else:
      data = -9999

   return data

def sampleRasterAtXY(src_filename, xy_list, method='nearest'):
   src_ds = gdal.Open(src_filename)
   
   data = list()
   for xy in xy_list:
      data.append(sampleRasterAtPoint(src_ds, xy, method=method))

   return data
   
def sampleRasterAtPoints(src_filename, shp_filename):
   src_ds = gdal.Open(src_filename)
   gt = src_ds.GetGeoTransform()
   rb = src_ds.GetRasterBand(1)

   # Output
   mx_list = list()
   my_list = list()
   data_list = list()

   if shp_filename.endswith('.shp'):
      ds = ogr.Open(shp_filename)
      lyr = ds.GetLayer()
      for feat in lyr:
         geom = feat.GetGeometryRef()
         points = geom.GetPoints()
         for point in points:
            mx = point[0]
            my = point[1]

            #Convert from map to pixel coordinates.
            #Only works for geotransforms with no rotation.
            #If raster is rotated, see http://code.google.com/p/metageta/source/browse/trunk/metageta/geometry.py#493
            px = int((mx - gt[0]) / gt[1]) #x pixel
            py = int((my - gt[3]) / gt[5]) #y pixel

            #structval=rb.ReadRaster(px,py,1,1,buf_type=gdal.GDT_Float32) #Assumes 16 bit int aka 'short'
            #intval = struct.unpack('h' , structval) #use the 'short' format code (2 bytes) not int (4 bytes)

            if (px >= 0) and (py >= 0) and (px < src_ds.RasterXSize) and (py < src_ds.RasterYSize):
               data = rb.ReadAsArray(px,py,1,1)
            else:
               data = [[-9999]]

            mx_list.append(mx)
            my_list.append(my)
            data_list.append(data[0][0])

   else:
      f = open(shp_filename, 'r')
      for line in f:
         mx = float(line.split()[0])
         my = float(line.split()[1])

         #Convert from map to pixel coordinates.
         #Only works for geotransforms with no rotation.
         #If raster is rotated, see http://code.google.com/p/metageta/source/browse/trunk/metageta/geometry.py#493
         px = int((mx - gt[0]) / gt[1]) #x pixel
         py = int((my - gt[3]) / gt[5]) #y pixel

         #structval=rb.ReadRaster(px,py,1,1,buf_type=gdal.GDT_Float32) #Assumes 16 bit int aka 'short'
         #intval = struct.unpack('h' , structval) #use the 'short' format code (2 bytes) not int (4 bytes)

         if (px >= 0) and (py >= 0) and (px < src_ds.RasterXSize) and (py < src_ds.RasterYSize):
            data = rb.ReadAsArray(px,py,1,1)
         else:
            data = [[-9999]]

         mx_list.append(mx)
         my_list.append(my)
         data_list.append(data[0][0])

   return (mx_list, my_list, data_list)
      
if __name__ == "__main__":
   import argparse

   parser = argparse.ArgumentParser()
   parser.add_argument('rasterfilename', type=str, help='raster filename')
   parser.add_argument('shapefilefilename', type=str, help='shapefile filename')
   parser.add_argument('--type', type=str, choices=['shapefile','ascii'], default='shapefile')

   args = parser.parse_args()
   src_filename = args.rasterfilename
   shp_filename = args.shapefilefilename

   (mx, my, data) = sampleRasterAtPoints(src_filename, shp_filename)
   for i in range(len(mx)):
      print mx[i], my[i], data[i]

