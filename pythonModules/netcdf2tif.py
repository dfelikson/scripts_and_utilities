#!/usr/bin/env python

import sys, os
sys.path.append('/Users/dfelikso/Research/Software/ScriptsAndUtilities/pythonModules/')

import raster
from netCDF4 import Dataset
from pyproj import Proj, transform

import numpy as np

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('netCDFfile',   type=str,   help='netCDF filename')
parser.add_argument('-x',           type=str,   help='name of variable with x coordinates', default='x')
parser.add_argument('-y',           type=str,   help='name of variable with y coordinates', default='y')
parser.add_argument('-z',           type=str,   help='name of variable with z coordinates', default='z')
parser.add_argument('--inputEPSG',  type=str,   help='input epsg',  default='4326')
parser.add_argument('--outputEPSG', type=str,   help='output epsg', default='3413')
parser.add_argument('--outputNDV',  type=float, help='output no data value', default=-9999.)
parser.add_argument('--datatype',   type=str,   help='data type of output tiff', default='Float32')
parser.add_argument('--showvars',               help='print all variable names to screen', action='store_true')
parser.add_argument('--outputdir',  type=str,   help='name of output directory', default='.')

# Input args {{{
args = parser.parse_args()
netCDFfile = args.netCDFfile
x_var = args.x
y_var = args.y
z_var = args.z
input_EPSG  = args.inputEPSG
output_EPSG = args.outputEPSG
output_NDV = args.outputNDV
dt    = args.datatype
showvars = args.showvars
outputdir = args.outputdir
# }}}

nc_fid = Dataset(netCDFfile, 'r')
z = nc_fid[z_var][:]

# Show variables {{{
if showvars:
   sys.stdout.write('Available variables:\n')
   for k in nc_fid.variables.keys():
      sys.stdout.write(' {:s}\n'.format(k))
   import pdb; pdb.set_trace()
   sys.exit()
# }}}

# Reproject {{{
inProj  = Proj(init='epsg:' + input_EPSG)
outProj = Proj(init='epsg:' + output_EPSG)
x_proj = list()
y_proj = list()
if input_EPSG != output_EPSG:
   for (x, y) in zip(nc_fid[x_var][:], nc_fid[y_var][:]):
      x_tmp, y_tmp = transform(inProj, outProj, float(x), float(y))
      x_proj.append(x_tmp)
      y_proj.append(y_tmp)
else:
   for (x, y) in zip(nc_fid[x_var][:], nc_fid[y_var][:]):
      x_proj.append(x)
      y_proj.append(y)
# }}}

# No data values
z_masked = z.filled(output_NDV)

# Set up geotransform
x_upperleft = np.min(x_proj)
y_upperleft = np.max(y_proj)
x_step = np.mean(np.diff(x_proj))
y_step = np.mean(np.diff(y_proj))

gt = (x_upperleft, x_step, 0., y_upperleft, 0., y_step)

# Output
filename = os.path.basename(netCDFfile).split('.')[0]
raster.writeArrayAsRasterBand(outputdir + '/' + filename + '_' + z_var + '.tif', gt, z_masked, -9999., dataType=dt)

