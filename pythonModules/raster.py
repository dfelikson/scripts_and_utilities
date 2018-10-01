#!/bin/env python

from osgeo import gdal, osr
from osgeo import gdalconst
import numpy

import matplotlib.pyplot as plt
from matplotlib import cm, colors

from bilinear_interpolate import *


def map2pixel(mx, my, gt):
   px = ((mx - gt[0]) / gt[1]).astype(int)
   py = ((my - gt[3]) / gt[5]).astype(int)
   return px, py

def getCoordinates(filename, bandnum):
   raster = gdal.Open(filename, gdalconst.GA_ReadOnly)
   coordinates = raster.GetGeoTransform()

   return coordinates

def readRasterBandAsArray(filename, bandnum):
   raster = gdal.Open(filename, gdalconst.GA_ReadOnly)
   rasterBand = raster.GetRasterBand(bandnum)
   rasterBandArray = rasterBand.ReadAsArray(0, 0, raster.RasterXSize, raster.RasterYSize).astype(numpy.float)
   
   rasterBandNoDataValue = rasterBand.GetNoDataValue()
   if rasterBandNoDataValue is not None:
      rasterBandArray[rasterBandArray - rasterBandNoDataValue < np.finfo(float).eps] = numpy.nan

   return rasterBandArray

def writeArrayAsRasterBand(filename,geoTransform,array,noDataValue,metadataDict=None):
   cols = array.shape[1]
   rows = array.shape[0]

   driver = gdal.GetDriverByName('GTiff')
   outRaster = driver.Create(filename, cols, rows, 1, gdal.GDT_Float32)
   outRaster.SetGeoTransform(geoTransform)
   if metadataDict is not None:
      outRaster.SetMetadata( metadataDict )
   outBand = outRaster.GetRasterBand(1)

   arrayout = numpy.where(~numpy.isnan(array), array, noDataValue)

   outBand.WriteArray(arrayout)
   outBand.SetNoDataValue(noDataValue)
   outRasterSRS = osr.SpatialReference()
   outRasterSRS.ImportFromEPSG(3413)
   outRaster.SetProjection(outRasterSRS.ExportToWkt())
   outBand.FlushCache()

def sampleRasterAtPoint(rasterArray,geoTransform,x,y,method='bilinear',nodataValue=np.nan):
   z = np.nan

   imagex = (x - geoTransform[0]) / geoTransform[1]
   imagey = (y - geoTransform[3]) / geoTransform[5]

   if (imagex >= 0) and (imagey >= 0) and (imagex < rasterArray.shape[1]) and (imagey < rasterArray.shape[0]):
      if method == 'nearest':
         z = rasterArray[int(np.floor(imagey)), int(np.floor(imagex))]
      if method == 'bilinear':
         z = bilinear_interpolate(rasterArray, imagex, imagey, nodataValue=nodataValue)

      if z == nodataValue:
         z = np.nan

   return z

def plotRaster(rasterArray,zMin,zMax,plotFilename):
   fig, ax = plt.subplots()
   cax = ax.imshow(rasterArray, cmap=cm.jet, norm=colors.Normalize(vmin=zMin, vmax=zMax))
   cbar = fig.colorbar(cax)
   plt.axes()
   plt.savefig(plotFilename)
   plt.close()

def plotRasterAndScatter(rasterArray,scatterArray,zMin,zMax,plotFilename):
   x = scatterArray[1]
   y = scatterArray[0]

   fig, ax = plt.subplots()
   cax = ax.imshow(rasterArray, cmap=cm.jet, norm=colors.Normalize(vmin=zMin, vmax=zMax))
   cbar = fig.colorbar(cax)
   plt.axes()
   plt.plot(x,y,'ro')
   plt.savefig(plotFilename)
   plt.close()

def reprojectDataset ( dataset, pixel_spacing=5000., epsg_from=4326, epsg_to=27700, ul_lr=None ):
   """
   A sample function to reproject and resample a GDAL dataset from within 
   Python. The idea here is to reproject from one system to another, as well
   as to change the pixel size. The procedure is slightly long-winded, but
   goes like this:
   
   1. Set up the two Spatial Reference systems.
   2. Open the original dataset, and get the geotransform
   3. Calculate bounds of new geotransform by projecting the UL corners 
   4. Calculate the number of pixels with the new projection & spacing
   5. Create an in-memory raster dataset
   6. Perform the projection
   """
   # Define the UK OSNG, see <http://spatialreference.org/ref/epsg/27700/>
   osng = osr.SpatialReference ()
   osng.ImportFromEPSG ( epsg_to )
   wgs84 = osr.SpatialReference ()
   wgs84.ImportFromEPSG ( epsg_from )
   tx = osr.CoordinateTransformation ( wgs84, osng )
   # Up to here, all  the projection have been defined, as well as a 
   # transformation from the from to the  to :)
   # We now open the dataset
   g = gdal.Open ( dataset )
   # Get the Geotransform vector
   geo_t = g.GetGeoTransform ()
   x_size = g.RasterXSize # Raster xsize
   y_size = g.RasterYSize # Raster ysize
   # Work out the boundaries of the new dataset in the target projection
   if ul_lr is not None:
      ulx = ul_lr[0]; uly = ul_lr[1]; lrx = ul_lr[2]; lry = ul_lr[3]
   else:
      (ulx, uly, ulz ) = tx.TransformPoint( geo_t[0], geo_t[3])
      (lrx, lry, lrz ) = tx.TransformPoint( geo_t[0] + geo_t[1]*x_size, \
                                            geo_t[3] + geo_t[5]*y_size )
   # See how using 27700 and WGS84 introduces a z-value!
   # Now, we create an in-memory raster
   mem_drv = gdal.GetDriverByName( 'MEM' )
   # The size of the raster is given the new projection and pixel spacing
   # Using the values we calculated above. Also, setting it to store one band
   # and to use Float32 data type.
   dest = mem_drv.Create('', int((lrx - ulx)/pixel_spacing), \
                             int((uly - lry)/pixel_spacing), 1, gdal.GDT_Float32)
   # Calculate the new geotransform
   new_geo = ( ulx, pixel_spacing, geo_t[2], \
               uly, geo_t[4], -pixel_spacing )
   # Set the geotransform
   dest.SetGeoTransform( new_geo )
   dest.SetProjection ( osng.ExportToWkt() )
   # Perform the projection/resampling 
   res = gdal.ReprojectImage( g, dest, \
               wgs84.ExportToWkt(), osng.ExportToWkt(), \
               gdal.GRA_Bilinear )
   return dest

