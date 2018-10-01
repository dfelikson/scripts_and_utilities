
import ogr
import numpy as np

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
         print 'ERROR: no points found in shapefile'
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
