#!/bin/env python
# -----
# Setup
# -----
import argparse
import numpy as np
import pylab as pl

# Input arguments
parser = argparse.ArgumentParser()
parser.add_argument('dataFile')
parser.add_argument('statsFile')
parser.add_argument('--col', type=int, help='column to derive stats from')
parser.add_argument("--histogram", help="histogram filename")
parser.add_argument("--histogramTitle")
parser.add_argument("--histogramXlabel")

args = parser.parse_args()

# normalized median absolute deviation (NMAD)
def nmad(errors):
   return 1.4826 * np.median( np.abs(errors - np.median(errors)) )

# ----------
# Processing
# ----------
dataList = []

if args.col:
   col = args.col
else:
   col = 1

# Read data file
dataFile = open(args.dataFile, "r")
for columns in ( raw.strip().split() for raw in dataFile ):  
   dataList.append(float(columns[col-1]))

dataFile.close()


# Write dh statistics
statsFile = open(args.statsFile, "w")
statsFile.write('     dhMin      dhMax     dhMean      dhMed      dhStd     dhNMAD     nPts\n')
statsFile.write('{0: 10.2f} {1: 10.2f} {2: 10.2f} {3: 10.2f} {4: 10.2f} {5: 10.2f} {6:8d} \n '.\
   format(np.min(dataList), np.max(dataList), np.mean(dataList), np.median(dataList), np.std(dataList), nmad(dataList), len(dataList)))

statsFile.close()

# Plot histogram
if args.histogram:
   # Clip the data to 90%
   axisMin = np.percentile(dataList, 5)
   axisMax = np.percentile(dataList, 95)
   clipIdx = np.where((dataList >= axisMin) & (dataList <= axisMax))
   dataListClipped = [dataList[i] for i in clipIdx[0]]

   # Empirical distribution
   n, bins, patches = pl.hist(dataListClipped, 50, normed=1)
   pl.setp(patches, 'facecolor', 'g', 'alpha', 0.75)
   pl.axis([axisMin, axisMax, 0, np.max(n)])

   # Analytical normal distribution
   mu = np.median(dataList)
   sigma = nmad(dataList)
   y = pl.normpdf( bins, mu, sigma)
   pl.plot(bins, y, 'k--', linewidth=1.5)
   mu = np.mean(dataList)
   sigma = np.std(dataList)
   y = pl.normpdf( bins, mu, sigma)
   pl.plot(bins, y, 'r--', linewidth=1.5)

   # Save figure
   pl.grid(True)
   if args.histogramTitle:
      pl.title(args.histogramTitle)
   if args.histogramXlabel:
      pl.xlabel(args.histogramXlabel)
   pl.savefig(args.histogram + ".png")
   pl.close()

