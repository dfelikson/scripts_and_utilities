#!/bin/env python
import sys
import argparse
from osgeo import ogr

parser = argparse.ArgumentParser()
parser.add_argument('shapefile',  type=str, help='ESRI shapefile file to open')
parser.add_argument('fields', type=str, nargs='+', help='field(s) to read')

args = parser.parse_args()

driver = ogr.GetDriverByName("ESRI Shapefile")
dataSource = driver.Open(args.shapefile, 1)
layer = dataSource.GetLayer()

for feat in layer:
   for field in args.fields:
      sys.stdout.write(feat.GetField(field) + ' ')
   sys.stdout.write('\n')

