#!/usr/bin/env python
import argparse
from netCDF4 import Dataset

parser = argparse.ArgumentParser()
parser.add_argument('netCDFfile', type=str, help='netCDF file to open')

args = parser.parse_args()

ncfile = Dataset(args.netCDFfile, 'r')

import pdb; pdb.set_trace()

