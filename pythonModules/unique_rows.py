import numpy as np

def unique_rows(a, **kwargs):

   rowtype = np.dtype((np.void, a.dtype.itemsize * a.shape[1]))
   b = np.ascontiguousarray(a).view(rowtype)
   return_index = kwargs.pop('return_index', False)
   out = np.unique(b, return_index=True, **kwargs)
   idx = out[1]
   uvals = a[idx]
   if (not return_index) and (len(out) == 2):
      return uvals
   elif return_index:
      return (uvals,) + out[1:]
   else:
      return (uvals,) + out[2:]
