import os

#import osgeo.ogr, osgeo.osr
#from osgeo import ogr, osr
import shapefile as shp

def write_shapefile_line(x, y, epsg, shp_filename, field_name=None, field_values=None):

   w = shp.Writer(shp.POLYLINEM)
   #w = shp.Writer(shp.POINT)
   w.autoBalance = 1 #ensures gemoetry and attributes match
   #w.field('X','F',10,8)
   #w.field('Y','F',10,8)
   w.field(field_name,'F',10,8)

   for i,_ in enumerate(x):
      w.point(x[i], y[i])
      w.record(field_values[i])

   w.save(shp_filename)

