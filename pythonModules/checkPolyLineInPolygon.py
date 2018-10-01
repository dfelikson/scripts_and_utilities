import sys
import numpy as np

from osgeo import gdal,ogr
from pyproj import Proj, transform

import matplotlib.path as mplPath
import numpy as np

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('line', type=str, help='line shapefile filename (must be polyline if shapefile)')
parser.add_argument('polygon', type=str, help='polygon shapefile filename')
parser.add_argument('field_names', nargs='+', type=str, help='field names to return')
parser.add_argument('--project-line-from', type=str, help='epsg code to project from')
parser.add_argument('--project-line-to', type=str, help='epsg code to project to')

args = parser.parse_args()
line_filename = args.line
polygon_filename = args.polygon
field_names = args.field_names

if (args.project_line_from is not None and args.project_line_to is None) or (args.project_line_to is not None and args.project_line_from is None):
   print 'must specify both --project-line-from and --project-line-to or neither'
   sys.exit()

if args.project_line_from is not None and args.project_line_to is not None:
   inP  = Proj(init="epsg:"+args.project_line_from)
   outP = Proj(init="epsg:"+args.project_line_to)

# Read in all points from line
if line_filename.endswith('.shp'):
   ds = ogr.Open(line_filename)
   lyr = ds.GetLayer()

   xy = np.array([0,0])
   for i in range(lyr.GetFeatureCount()):
      feat = lyr.GetFeature(i)
      geom = feat.GetGeometryRef()
      for iPoint in range(geom.GetPointCount()):
         x,y = geom.GetX(iPoint), geom.GetY(iPoint)

         # Append
         xy = np.vstack((xy, [x, y]))

   # Delete first row (initialized as [0,0])
   xy = np.delete(xy, (0), axis=0)

elif line_filename.endswith('.csv'):
   data = np.genfromtxt(line_filename, delimiter=',')
   data = data[~np.isnan(data).any(axis=1)]
   
   xy = data[:,0:2]


# Transform
if args.project_line_from is not None and args.project_line_to is not None:
   x, y = transform(inP, outP, xy[:,0], xy[:,1])
   xy = np.hstack( x, y )

# Read polygon vertices
ds = ogr.Open(polygon_filename)
lyr = ds.GetLayer()
for feat in lyr:
   geom = feat.GetGeometryRef()
   ring = geom.GetGeometryRef(0)
   #bbPath = mplPath.Path(np.array([[ring.GetPoint(0)[0], ring.GetPoint(0)[1]],
   #                                [ring.GetPoint(1)[0], ring.GetPoint(1)[1]],
   #                                [ring.GetPoint(2)[0], ring.GetPoint(2)[1]],
   #                                [ring.GetPoint(3)[0], ring.GetPoint(3)[1]]]))
   bbPath = mplPath.Path(ring.GetPoints())

   if len(xy.shape) == 2:
      if np.any(bbPath.contains_points(xy)):
         for field_name in field_names:
            sys.stdout.write(feat.GetField(field_name))
            sys.stdout.write(' ')
         sys.stdout.write('\n')

