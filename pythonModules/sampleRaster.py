#!/usr/bin/env python

import numpy as np
from osgeo import gdal, ogr

from bilinear_interpolate import *
from scipy.interpolate import interp1d

def read_line(lineFilename, reverse=False, resampleDistance=None):
   ds = ogr.Open(lineFilename)
   lyr = ds.GetLayer()
   feat = lyr.GetFeature(0)
   geom = feat.GetGeometryRef()
   
   x = np.array([])
   y = np.array([])
   for i, pointxy in enumerate(geom.GetPoints()):
      xtmp, ytmp = pointxy
      x  = np.append(x,  xtmp)
      y  = np.append(y,  ytmp)
   
   # Reverse the centerline
   if reverse:
      x = x[::-1]
      y = y[::-1]

   for i, val in enumerate(x):
      if i > 0:
         d = np.append(d, np.sqrt( (x[i]-x[i-1])**2 + (y[i]-y[i-1])**2 ))
      else:
         d = np.array(0)

   d = np.cumsum(d)

   # Resample
   if resampleDistance is not None:
      fx = interp1d(d, x)
      fy = interp1d(d, y)

      d = np.arange(0, d[-1], resampleDistance)
      x = fx(d)
      y = fy(d)

   return x, y, d

def raster_along_line(rasterfilename, line, nodataValue, lineType='shp', method='bilinear'):
   # Read raster
   ds = gdal.Open(rasterfilename)
   rb = ds.GetRasterBand(1)
   gt = ds.GetGeoTransform()
   zarray = rb.ReadAsArray()

   # Read line
   if lineType == 'shp':
      linex, liney, lined = read_line(lineFilename, resampleDistance=50.0) # TBD: resample distance hardcoded at 50.0 m along-flow
   if lineType == 'dict':
      linex = line['x']
      liney = line['y']

      lined = np.array([0.0])
      for i in range(1,len(linex),1):
         lined = np.append(lined, lined[i-1] + np.sqrt( (linex[i]-linex[i-1])**2 + (liney[i]-liney[i-1])**2 ))

   zsample = np.empty(linex.shape)

   imagexs = (linex - gt[0]) / gt[1]
   imageys = (liney - gt[3]) / gt[5]
   
   for i, imagex in enumerate(imagexs):
      imagey = imageys[i]

      if (imagex >= 0) and (imagey >= 0) and (imagex < ds.RasterXSize) and (imagey < ds.RasterYSize):

         if method == 'nearest':
            zsample[i] = zarray[int(np.floor(imagey)), int(np.floor(imagex))]
            if zsample[i] == nodataValue:
               zsample[i] = np.nan
         elif method == 'bilinear':
            zsample[i] = bilinear_interpolate(zarray, imagex, imagey, nodataValue=nodataValue)
         else:
            zsample[i] = bilinear_interpolate(zarray, imagex, imagey, nodataValue=nodataValue)
         
      else:
         zsample[i] = np.nan


   return linex, liney, zsample, lined

