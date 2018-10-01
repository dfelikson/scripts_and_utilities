from __future__ import division 
import numpy as np

def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x,y
    else:
        return np.nan, np.nan

def ray_line_intersection(origin, direction, a, b):
   o = np.array(origin)
   d = np.array(direction)
   a = np.array(a)
   b = np.array(b)

   # From https://rootllama.wordpress.com/2014/06/20/ray-line-segment-intersection-test-in-2d/
   v1 = o - a
   v2 = b - a
   v3 = np.array( (-d[1], d[0]) )
   denom = np.dot(v2, v3)
   if denom == 0:
      return False, np.nan
   t1 = np.cross(v2, v1) / denom
   t2 = np.dot(v1, v3) / denom

   intersect = t1 >= 0 and t2 >= 0 and t2 <= 1
   if intersect:
      x1 = o + d*t1
      x2 = a + (b-a)*t2
      return intersect, x1
   else:
      return intersect, np.nan

