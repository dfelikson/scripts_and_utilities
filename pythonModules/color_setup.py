import matplotlib
import pylab

import numpy as np

def paired_colormap_12():
   colors = []
   colors.append(166/255.0, 206/255.0, 227/255.0, 1.0)
   colors.append( 31/255.0, 120/255.0, 180/255.0, 1.0)
   colors.append(178/255.0, 223/255.0, 138/255.0, 1.0)
   colors.append( 51/255.0, 160/255.0,  44/255.0, 1.0)
   colors.append(251/255.0, 154/255.0, 153/255.0, 1.0)
   colors.append(227/255.0,  26/255.0,  28/255.0, 1.0)
   colors.append(253/255.0, 191/255.0, 111/255.0, 1.0)
   colors.append(255/255.0, 127/255.0,   0/255.0, 1.0)
   colors.append(202/255.0, 178/255.0, 214/255.0, 1.0)
   colors.append(106/255.0,  61/255.0, 154/255.0, 1.0)
   colors.append(255/255.0, 255/255.0, 153/255.0, 1.0)
   colors.append(177/255.0,  89/255.0,  40/255.0, 1.0)

   return colors


def paired_colormap(ntotal):
   colors = []
   #for i in range(0,ntotal,1):
   #   colors.append( pylab.cm.Paired(float(i)/float(ntotal)) )

   #colors_orig = matplotlib.cm.get_cmap('Paired')
   colors_orig = matplotlib.cm.get_cmap('tab20')
   print colors_orig
   for i in np.linspace(0.,1.,num=ntotal):
      colors.append(colors_orig(i))

   return colors


def custom_16_colors():
   colors = []
   colors.append( (255/255.0,   0/255.0,   0/255.0, 1.0) ) # red
   colors.append( (255/255.0, 160/255.0,   0/255.0, 1.0) )
   colors.append( (255/255.0,   0/255.0, 160/255.0, 1.0) )
   colors.append( (255/255.0, 160/255.0, 160/255.0, 1.0) )

   colors.append( (255/255.0, 255/255.0,   0/255.0, 1.0) ) # yellow

   colors.append( (  0/255.0, 255/255.0,   0/255.0, 1.0) ) # green
   colors.append( (160/255.0, 255/255.0,   0/255.0, 1.0) )
   colors.append( (  0/255.0, 255/255.0, 140/255.0, 1.0) )
   colors.append( (160/255.0, 255/255.0, 160/255.0, 1.0) )

   colors.append( (  0/255.0, 255/255.0, 255/255.0, 1.0) ) # cyan

   colors.append( (  0/255.0,   0/255.0, 255/255.0, 1.0) ) # blue
   colors.append( (  0/255.0, 160/255.0, 255/255.0, 1.0) )
   colors.append( (160/255.0,   0/255.0, 255/255.0, 1.0) )
   colors.append( (160/255.0, 160/255.0, 255/255.0, 1.0) )

   colors.append( (255/255.0,   0/255.0, 255/255.0, 1.0) ) # purple

   colors.append( (  0/255.0,   0/255.0,   0/255.0, 1.0) ) # black

   return colors

def glacier_colors(gl_abbr):
   from color_setup import paired_colormap
   
   glmap = dict()

   colors = paired_colormap(15)
   colors.append( (0.0, 0.0, 0.0, 1.0) ) # JAK

   glmap['ING'] = colors[ 0]
   glmap['UMI'] = colors[ 1]
   glmap['RNK'] = colors[ 2]
   glmap['KAS'] = colors[ 3]
   glmap['KSS'] = colors[ 4]
   glmap['PRD'] = colors[ 5]
   glmap['SIL'] = colors[ 6]
   glmap['KNG'] = colors[ 7]
   glmap['LIK'] = colors[ 8]
   glmap['LIL'] = colors[ 9]
   glmap['STR'] = colors[10]
   glmap['AVA'] = colors[11]
   glmap['KUJ'] = colors[12]
   glmap['KAN'] = colors[13]
   glmap['EQI'] = colors[14]
   glmap['JAK'] = colors[15]

   return glmap[gl_abbr]

