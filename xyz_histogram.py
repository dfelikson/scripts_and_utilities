#!/usr/bin/python

import numpy
import sys
import re

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

#z_array = numpy.empty([0,0])
z_array = list()

#fname=/science/dfelikson/RT_CX_OFP_comparison/method_sampling/antarctica/cx/vel_truth_and_cxsurf_pdiff_10k.xyz
xyz_file = sys.argv[1]
title    = sys.argv[2]
xlabel   = sys.argv[3]
xmin = float(sys.argv[4])
xmax = float(sys.argv[5])
plot_save_file = sys.argv[6]
if len(sys.argv) == 8:
    ymin = float(sys.argv[7])
    ymax = float(sys.argv[8])


for line in open(xyz_file):
    fields = re.findall(r"[\S]+", line)
    #x = float(fields[0])
    #y = float(fields[1])
    z = float(fields[2])

    #z_array = numpy.append(z_array,z)
    z_array.append(z)

# Histogram
num_bins = 1000
#n, bins, patches = plt.hist(z_array, range=(xmin, xmax), bins=num_bins, normed=1, facecolor='green', alpha=0.5)
n, bins, patches = plt.hist(z_array, range=(xmin, xmax), bins=num_bins, normed=False, facecolor='green', alpha=0.5)

plt.grid(True)
plt.title(title)
plt.xlabel(xlabel)
#plt.ylabel("Probability")
plt.ylabel("Count")
plt.xlim(xmin,xmax)
if len(sys.argv) == 8:
    plt.ylim(ymin,ymax)

#plt.axvline(x=1, ymin=0, ymax=500, color='r', linestyle='dashed')

plt.savefig(plot_save_file)
#plt.show()

