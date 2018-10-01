#!/bin/env python
import argparse
from osgeo import ogr

parser = argparse.ArgumentParser()
parser.add_argument('shapefile', type=str, help='ESRI shapefile file to open')

args = parser.parse_args()

driver = ogr.GetDriverByName("ESRI Shapefile")
dataSource = driver.Open(args.shapefile, 1)
layer = dataSource.GetLayer()

import pdb; pdb.set_trace()

