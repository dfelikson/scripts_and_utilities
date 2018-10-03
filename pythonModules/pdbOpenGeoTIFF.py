#!/usr/bin/env python

import sys
import raster
import matplotlib.pyplot as plt

filename = sys.argv[1]
bandnum = 1

rasterBandArray = raster.readRasterBandAsArray(filename, bandnum)
import pdb; pdb.set_trace()

