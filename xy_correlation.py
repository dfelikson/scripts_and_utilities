#!/usr/bin/python

import numpy
import sys
import re

import matplotlib.pyplot as plt

#z_array = numpy.empty([0,0])
x_array = list()
y_array = list()

#fname=/science/dfelikson/RT_CX_OFP_comparison/method_sampling/antarctica/cx/vel_truth_and_cxsurf_pdiff_10k.xyz
xy_file = sys.argv[1]
title    = sys.argv[2]
xlabel   = sys.argv[3]
ylabel   = sys.argv[4]
#xmin = float(sys.argv[4])
#xmax = float(sys.argv[5])
plot_save_file = sys.argv[5]

for line in open(xy_file):
    fields = re.findall(r"[\S]+", line)
    x = float(fields[0])
    y = float(fields[1])
    #z = float(fields[2])

    x_array.append(x)
    y_array.append(y)

# Correlation
c = numpy.corrcoef(x_array, y_array)
print c[0,1]

# Plot
plt.grid(True)
plt.title(title)
plt.xlabel(xlabel)
plt.ylabel(ylabel)

plt.plot(x_array,y_array,'bo')

plt.savefig(plot_save_file)
plt.show()

