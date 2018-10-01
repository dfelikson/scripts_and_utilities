import os

#import osgeo.ogr, osgeo.osr
from osgeo import ogr, osr
import shapefile as shp

def write_shapefile_line(x, y, epsg, shp_filename, field_name=None, field_values=None):
   spatialReference = osr.SpatialReference() #will create a spatial reference locally to tell the system what the reference will be
   spatialReference.ImportFromEPSG(int(epsg)) #here we define this reference to be the EPSG code

   driver = ogr.GetDriverByName('ESRI Shapefile') # will select the driver for our shp-file creation.
   if os.path.exists(shp_filename):
      driver.DeleteDataSource(shp_filename)

   shapeData = driver.CreateDataSource(shp_filename) #so there we will store our data
   layer = shapeData.CreateLayer('layer', spatialReference, ogr.wkbLineString) #this will create a corresponding layer for our data with given spatial information.

   # create ogr geometry
   linelyr = ogr.Geometry(ogr.wkbLineString)

   # # create the field
   # layer.CreateField(ogr.FieldDefn(field_name, ogr.OFTReal))

   for i,_ in enumerate(x):
      linelyr.AddPoint(x[i], y[i])

   # Create the feature and set values
   defn = layer.GetLayerDefn()
   feat = ogr.Feature(defn)
   # feat.SetField(field_name, 9999)
   feat.SetGeometry(linelyr)
   layer.CreateFeature(feat)

   shapeData.Destroy() #lets close the shapefile

def write_shapefile_point(x, y, epsg, shp_filename, field_name=None, field_values=None):
   spatialReference = osr.SpatialReference()
   spatialReference.ImportFromEPSG(int(epsg))

   driver = ogr.GetDriverByName('ESRI Shapefile')
   if os.path.exists(shp_filename):
      driver.DeleteDataSource(shp_filename)

   shapeData = driver.CreateDataSource(shp_filename)
   layer = shapeData.CreateLayer('layer', spatialReference, ogr.wkbPoint)
   point = ogr.Geometry(ogr.wkbPoint)

   if field_name is not None and field_values is not None:
      # Add the fields we're interested in
      layer.CreateField(ogr.FieldDefn(field_name, ogr.OFTReal))

   for i,_ in enumerate(x):
      point.AddPoint(x[i], y[i])

      # Create the feature
      defn = layer.GetLayerDefn()
      feat = ogr.Feature(defn)

      if field_name is not None and field_values is not None:
         # Set the attributes using specified values
         feat.SetField(field_name, field_values[i])

      # Set the feature geometry using the point
      feat.SetGeometry(point)
      # Create the feature in the layer (shapefile)
      layer.CreateFeature(feat)
      # Dereference the feature
      feat = None

   # Save and close the data source
   shapeData.Destroy()

