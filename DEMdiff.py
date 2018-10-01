#!/bin/env python

import argparse
import sys, os

parser = argparse.ArgumentParser()
parser.add_argument('dem1', type=str)
parser.add_argument('dem2', type=str)
parser.add_argument('outputDir', type=str)
parser.add_argument('--mask1', type=str)
parser.add_argument('--mask1valid', type=str)
parser.add_argument('--mask2', type=str)
parser.add_argument('--mask2valid', type=str)

args = parser.parse_args()

# Apply masks
dem1filename = os.path.splitext(os.path.basename(args.dem1))[0]
dem2filename = os.path.splitext(os.path.basename(args.dem2))[0]
if args.mask1 and args.mask1valid:
   os.system("gdal_calc.py -A " + args.dem1 + " -B " + args.mask1 + " --calc=\"(B" + args.mask1valid + ")*A\" " + \
                          "--outfile=" + args.outputDir + "/" + dem1filename + "_masked.tif")
   dem1file = args.outputDir + "/" + dem1filename + "_masked.tif"
else:
   dem1file = args.dem1

if args.mask2 and args.mask2valid:
   os.system("gdal_calc.py -A " + args.dem2 + " -B " + args.mask2 + " --calc=\"(B" + args.mask2valid + ")*A\" " + \
                          "--outfile=" + dem2filename + "_masked.tif")
   dem2file = args.outputDir + "/" + dem2filename + "_masked.tif"
else:
   dem2file = args.dem2

# Warp dem1 to dem2 projection
os.system("sh warpDEMprojection.sh " + dem2file + " " + dem1file + " " + args.outputDir)
dem1file = args.outputDir + "/" + os.path.splitext(os.path.basename(dem1file))[0] + "_warped.tif"
dem2file = args.dem2

# Register to same coordinates
os.system("sh selectDEMoverlap.sh " + dem2file + " " + dem1file + " " + args.outputDir + " automatic")
dem1file = args.outputDir + "/" + os.path.splitext(os.path.basename(dem1file))[0] + "_select.tif"
dem2file = args.outputDir + "/" + os.path.splitext(os.path.basename(dem2file))[0] + "_select.tif"

# Difference
dem1filename = os.path.splitext(os.path.basename(dem1file))[0]
dem2filename = os.path.splitext(os.path.basename(dem2file))[0]
os.system("gdal_calc.py -A " + dem1file + " " + " -B " + dem2file + " " + \
                       "--calc=\"B-A\" --outfile=" + args.outputDir + "/" + dem2filename + "_MINUS_" + dem1filename + ".tif --NoDataValue=-9999")

# Make overviews for plotting
os.system("gdaladdo -ro " + args.outputDir + "/" + dem2filename + "_MINUS_" + dem1filename + ".tif 2 4 8 16")
sys.exit()

os.system("\\rm " + args.outputDir + "/*select*")

