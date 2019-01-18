#!/usr/bin/env python

import sys, os
sys.path.append('/Users/dfelikso/Research/Software/ScriptsAndUtilities/pythonModules/')
import raster
from scipy.io import loadmat

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('matfile',     type=str, help='matfile filename')
parser.add_argument('-x',          type=str, help='name of variable with x coordinates', default='x')
parser.add_argument('-y',          type=str, help='name of variable with y coordinates', default='y')
parser.add_argument('-z',          type=str, help='name of variable with z coordinates', default='z')
parser.add_argument('--datatype',  type=str, help='data type of output tiff', default='Float32')
parser.add_argument('--showvars',            help='print all variable names to screen', action='store_true')
parser.add_argument('--outputdir', type=str, help='name of output directory', default='.')

args = parser.parse_args()
matfile = args.matfile
x_var = args.x
y_var = args.y
z_var = args.z
dt    = args.datatype
showvars = args.showvars
outputdir = args.outputdir

m = loadmat(matfile)
if showvars:
   sys.stdout.write('Available variables:\n')
   for k in m.keys():
      if not k.startswith('_'):
         sys.stdout.write('  {:s}\n'.format(k))
   sys.exit()

x_upperleft = m[x_var][0,0]
y_upperleft = m[y_var][0,0]
x_step = m[x_var][1,0] - m[x_var][0,0]
y_step = m[y_var][1,0] - m[y_var][0,0]

gt = (x_upperleft, x_step, 0., y_upperleft, 0., y_step)

filename = os.path.basename(matfile)
raster.writeArrayAsRasterBand(outputdir + '/' + filename + '_' + z_var + '.tif', gt, m[z_var], -9999., dataType=dt)

