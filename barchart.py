#!/usr/bin/python

import sys

import re
import csv

import numpy as np
import matplotlib.pyplot as plt

stats_file = sys.argv[1]
ncategories = int(sys.argv[2])
title    = sys.argv[3]
xlabel   = sys.argv[4]
plot_save_file = sys.argv[5]

xaxis_list = list()
value_list = [[] for i in range(ncategories)]
error_list = [[] for i in range(ncategories)]

colors = ('red', 'blue', 'green')

with open(stats_file, 'rb') as f:
    reader = csv.reader(f)
    for field in reader:
        xaxis_list.append(field[0])

        for icategory in range(ncategories):
            value = float(field[2*icategory+1])
            error = float(field[2*icategory+2])
            value_list[icategory].append(value)
            error_list[icategory].append(error)

# Bar chart
ind = np.arange(len(xaxis_list))  # the x locations for the groups
width = 0.15       # the width of the bars

rects = list()
fig, ax = plt.subplots()
for icategory in range(ncategories):
    rect = ax.bar(ind+width*icategory, value_list[icategory], width, color=colors[icategory], yerr=error_list[icategory], ecolor='k')
    rects.append(rect)

ax.set_xticks(ind+width)
ax.set_xticklabels( xaxis_list )

plt.grid(True)
plt.title(title)
plt.xlabel(xlabel)
plt.ylabel("Volume Change [km$^3$/yr]")

for icategory in range(ncategories):
    ax.legend( (rects[0][0], rects[1][0], rects[2][0]), ('RT', 'CX', 'OFP') )

plt.savefig(plot_save_file)
#plt.show()

