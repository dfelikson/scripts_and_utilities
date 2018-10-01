import os

import csv
import osgeo.ogr, osgeo.osr #we will need some packages
from osgeo import ogr #and one more for the creation of a new field

from pyproj import Proj, transform

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('input_file',    type=str)
parser.add_argument('--input_EPSG',  type=str, default='4326')
parser.add_argument('--output_EPSG', type=str, default='4326')
parser.add_argument('--delimiter',   type=str, default=',')
parser.add_argument('--export_shp',  type=str)
parser.add_argument('--shp_type',    type=str, default='line', choices=['line','point'])
args = parser.parse_args()
input_file  = args.input_file
input_EPSG  = args.input_EPSG
output_EPSG = args.output_EPSG
delimiter   = args.delimiter
if args.export_shp is None:
   export_shp = input_file + '.shp'
else:
   export_shp = args.export_shp


spatialReference = osgeo.osr.SpatialReference() #will create a spatial reference locally to tell the system what the reference will be
spatialReference.ImportFromEPSG(int(output_EPSG)) #here we define this reference to be the EPSG code

driver = osgeo.ogr.GetDriverByName('ESRI Shapefile') # will select the driver for our shp-file creation.
if os.path.exists(export_shp):
     driver.DeleteDataSource(export_shp)

# create ogr geometry
line = ogr.Geometry(ogr.wkbLineString)
multipoint = ogr.Geometry(ogr.wkbMultiPoint)
with open(input_file, 'rb') as csvfile:
    readerDict = csv.DictReader(csvfile, delimiter=delimiter)

    for row in readerDict:

        if input_EPSG != output_EPSG:
            inProj  = Proj(init='epsg:' + input_EPSG)
            outProj = Proj(init='epsg:' + output_EPSG)
            x, y = transform(inProj, outProj, float(row['LON']), float(row['LAT']))
        else:
            x = float(row['LON']) #we do have LATs and LONs as Strings, so we convert them
            y = float(row['LAT'])
        
        if args.shp_type == 'line':
           line.AddPoint(x, y) 
        elif args.shp_type == 'point':
           point = ogr.Geometry(ogr.wkbPoint)
           point.AddPoint(x, y)
           multipoint.AddGeometry(point)


shapeData = driver.CreateDataSource(export_shp) #so there we will store our data

if args.shp_type == 'line':
   layer = shapeData.CreateLayer('layer', spatialReference, ogr.wkbLineString) #this will create a corresponding layer for our data with given spatial information.
elif args.shp_type == 'point':
   layer = shapeData.CreateLayer('layer', spatialReference, ogr.wkbMultiPoint) #this will create a corresponding layer for our data with given spatial information.

# create the field
layer.CreateField(ogr.FieldDefn('track', ogr.OFTInteger))

# Create the feature and set values
defn = layer.GetLayerDefn()
feat = ogr.Feature(defn)
feat.SetField('track', 9999)
if args.shp_type == 'line':
   feat.SetGeometry(line)
elif args.shp_type == 'point':
   feat.SetGeometry(multipoint)
layer.CreateFeature(feat)

shapeData.Destroy() #lets close the shapefile

