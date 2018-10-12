#!/usr/bin/env python

import sys
sys.path.append('/Users/dfelikso/Research/Software/ScriptsAndUtilities/pythonModules/')
import raster
from scipy.io import loadmat

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('matfile',    type=str, help='matfile filename')
parser.add_argument('-x',         type=str, help='name of variable with x coordinates', default='x')
parser.add_argument('-y',         type=str, help='name of variable with y coordinates', default='y')
parser.add_argument('-z',         type=str, help='name of variable with z coordinates', default='z')
parser.add_argument('--datatype', type=str, help='data type of output tiff', default='float')

args = parser.parse_args()
matfile = args.matfile
x_var = args.x
y_var = args.y
z_var = args.z
dt    = args.datatype

m = loadmat(matfile)

x_upperleft = m[x_var][0,0]
y_upperleft = m[y_var][0,0]
x_step = m[x_var][1,0] - m[x_var][0,0]
y_step = m[y_var][1,0] - m[y_var][0,0]

gt = (x_upperleft, x_step, 0., y_upperleft, 0., y_step)
raster.writeArrayAsRasterBand(matfile+'.tif', gt, m[z_var], -9999., dataType=dt)

