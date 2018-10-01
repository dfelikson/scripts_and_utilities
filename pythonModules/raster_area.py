#!/usr/bin/env python
import sys
sys.path.append('/home/student/denis/ScriptsAndUtilities/pythonModules')
import raster
import numpy as np

gt = raster.getCoordinates(sys.argv[1],1)
data = raster.readRasterBandAsArray(sys.argv[1],1)

pixel_area = abs(gt[1] * gt[5])
nvalid_pixels = np.nansum(data/data)

print pixel_area * nvalid_pixels

