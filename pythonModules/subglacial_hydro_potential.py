#!/usr/bin/env python

import sys

from osgeo import gdal, gdalconst

import numpy as np
from matplotlib import pyplot as plt

sys.path.append('/home/student/denis/ScriptsAndUtilities/pythonModules')
from raster import *

# Setup
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--surface', type=str, default='/disk/staff/gcatania/polar/Arctic/data/Greenland_bed_data/Mass_Cons_Bed/BedMachineGreenland-2017-09-20/BedMachineGreenland-2017-09-20-Surface.tif')
parser.add_argument('--bed', type=str, default='/disk/staff/gcatania/polar/Arctic/data/Greenland_bed_data/Mass_Cons_Bed/BedMachineGreenland-2017-09-20/BedMachineGreenland-2017-09-20-Bed.tif')
parser.add_argument('--waterPressure', type=float, default=1.0, help='Percentage of ice overburden.')
args = parser.parse_args()

iceDensity = 0.917
k = args.waterPressure

# read surface
print 'reading surface'
surf_filename = args.surface
surf = gdal.Open(surf_filename, gdalconst.GA_ReadOnly)
surf_proj = surf.GetProjection()
surf_geotrans = surf.GetGeoTransform()
wide = surf.RasterXSize
high = surf.RasterYSize

# read bed
print 'reading bed'
bed_filename = args.bed
bed = gdal.Open(bed_filename, gdalconst.GA_ReadOnly)
bed_proj = bed.GetProjection()
bed_geotrans = bed.GetGeoTransform()

# interpolate bed to surface
print 'interpolating bed to surface'
bed_interp_filename = 'bed_warp.tif'
bed_interp = gdal.GetDriverByName('GTiff').Create(bed_interp_filename, wide, high, 1, gdalconst.GDT_Float32)
bed_interp.SetGeoTransform( surf_geotrans )
bed_interp.SetProjection( surf_proj )
gdal.ReprojectImage(bed, bed_interp, bed_proj, surf_proj, gdalconst.GRA_Bilinear)

# hydropotential using surface and bed values
surf = readRasterBandAsArray(surf_filename, 1)
bed_interp = readRasterBandAsArray(bed_interp_filename, 1)
potential = k * iceDensity * (9.8) * (surf) + (1.00-k*iceDensity) * (9.8) * (bed_interp) # kPa

# write potential
print 'writing hydro potential'
potential_filename = 'hydropo.tif'
writeArrayAsRasterBand(potential_filename, surf_geotrans, potential, -9999.)

