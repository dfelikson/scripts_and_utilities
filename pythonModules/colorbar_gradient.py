#!/usr/bin/env python

import sys
import numpy as np
import matplotlib
from matplotlib import pyplot as plt

try:
   matplotlib.cm.get_cmap(sys.argv[1])
except:
   print('error finding colormap: ' + sys.argv[1])

cmap = matplotlib.cm.get_cmap(sys.argv[1])
print('found colormap: ' + sys.argv[1])

gradient = np.linspace(1, 0, 256) # for some reason, this needs to be backward
gradient = np.vstack((gradient, gradient))

fig = plt.figure(figsize=(8, 1))
ax = fig.add_axes([0.05, 0.5, 0.9, 0.45])
ax.imshow(gradient, aspect='auto', cmap=cmap, vmin=0., vmax=1.)
ax.set_axis_off()

plt.savefig(sys.argv[1]+'.pdf', bbox_inches='tight')
plt.close()

