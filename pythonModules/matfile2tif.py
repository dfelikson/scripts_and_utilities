#!/usr/bin/env python

import sys
sys.path.append('/Users/dfelikso/Research/Software/ScriptsAndUtilities/pythonModules/')

import raster

from scipy.io import loadmat

m = loadmat('GrIS_Tidewater_basins.mat')


x_upperleft = m['x'][0][0]
y_upperleft = m['y'][0][0]
x_step = m['x'][0][1] - m['x'][0][0]
y_step = m['y'][0][1] - m['y'][0][0]

gt = (x_upperleft, x_step, 0., y_upperleft, 0., y_step)
raster.writeArrayAsRasterBand('GrIS_Tidewater_basins.tif', gt, m['tidewater_basins'], -9999.)

