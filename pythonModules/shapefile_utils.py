
import os
import ogr
import numpy as np

def createBuffer(inputfn, outputBufferfn, bufferDist):
   inputds = ogr.Open(inputfn)
   inputlyr = inputds.GetLayer()

   shpdriver = ogr.GetDriverByName('ESRI Shapefile')
   if os.path.exists(outputBufferfn):
      shpdriver.DeleteDataSource(outputBufferfn)
   outputBufferds = shpdriver.CreateDataSource(outputBufferfn)
   
   bufferlyr = outputBufferds.CreateLayer(outputBufferfn, geom_type=ogr.wkbPolygon)
   featureDefn = bufferlyr.GetLayerDefn()
   
   inputlyrDefn = inputlyr.GetLayerDefn()
   for i in range(inputlyrDefn.GetFieldCount()):
      bufferlyr.CreateField ( inputlyrDefn.GetFieldDefn(i) )
    
   for feature in inputlyr:
      ingeom = feature.GetGeometryRef()
      geomBuffer = ingeom.Buffer(bufferDist)
      
      outFeature = ogr.Feature(featureDefn)
      outFeature.SetGeometry(geomBuffer)
      
      for i in range(inputlyrDefn.GetFieldCount()): 
         fieldName = inputlyrDefn.GetFieldDefn(i).GetName()
         outFeature.SetField(fieldName, feature.GetField(fieldName))
      bufferlyr.CreateFeature(outFeature)
      outFeature = None

def read_shapefile_points(shapefile):
   if shapefile.endswith('.shp'):
      ds = ogr.Open(shapefile)
      lyr = ds.GetLayer()
      feat = lyr.GetFeature(0)
      geom = feat.GetGeometryRef()
      
      x = np.array([])
      y = np.array([])
      points = geom.GetPoints()
      if points is None:
         print('ERROR: no points found in shapefile')
         return None, None

      for i, pointxy in enumerate(points):
         xtmp, ytmp = pointxy
         x  = np.append(x,  xtmp)
         y  = np.append(y,  ytmp)

   elif shapefile.endswith('.csv'):
      data = np.genfromtxt(shapefile, delimiter=',')
      data = data[~np.isnan(data).any(axis=1)]
      x = data[:,xcol]
      y = data[:,ycol]
     
   return x, y

