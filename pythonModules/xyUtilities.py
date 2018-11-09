#!/bin/env python
import numpy as np
import matplotlib.pyplot as plt

def stats(y):
   yValid = y[~np.isnan(y)]
   min = np.min(yValid)
   max = np.max(yValid)
   mean = np.mean(yValid)
   medn = np.median(yValid)
   stddev = np.std(yValid)
   q75, q25 = np.percentile(yValid, [75 ,25])

   return min, max, mean, medn, stddev, q25, q75


def runningMaximum(y):
   runningMaxIdx = False*np.ones(y.shape)
   for idx in range(0,len(y),1):
      if ~np.isnan(y[idx]) and np.all(y[idx] > y[0:idx][~np.isnan(y[0:idx])]):
         runningMaxIdx[idx] = True

   return np.array(runningMaxIdx, dtype=bool)


# Find empirical half width at half maximum (HWHM) of a peak
def HWHM(x, y, peakIdx, halfwindow):
   halfwidth = np.nan

   if ~np.isnan(y[peakIdx]):
      
      # Find the highest local minimum 
      localMins = list()

      for step in (-1,1):
         i = peakIdx
         yCurr = y[i]
         yAdjc = y[i + step]
         localWindow = y[i - halfwindow : i + halfwindow]

         while yAdjc < yCurr or np.any(localWindow < yCurr):
            i = i + step
            yCurr = y[i]
            yAdjc = y[i + step]
            localWindow = y[i - halfwindow : i + halfwindow]

         localMins.append(i)

      i = np.argmax( (y[localMins[0]], y[localMins[1]]) )
      localMin = localMins[i]

      # Find half width at half maximum
      halfmax = (y[peakIdx] + y[localMin]) / 2
      if ~np.isnan(halfmax):
         if i == 0:
            halfmaxLocation = np.min( np.where(y[localMin:] > halfmax) ) + localMin
         if i == 1:
            halfmaxLocation = np.max( np.where(y[:localMin] > halfmax) )

         halfwidth = np.abs(x[peakIdx] - x[halfmaxLocation])

   return halfwidth


def runningMedian(x, y, xwindow, xcenterstart=None):
   sortIdx = np.argsort(x)
   x = x[sortIdx]
   y = y[sortIdx]

   medians  = np.array([])
   IQRs     = np.array([])
   q25s     = np.array([])
   q75s     = np.array([])
   
   if xcenterstart is not None:
      xcenters = np.arange( xcenterstart,          np.max(x) + xwindow/2, xwindow)
   else:
      xcenters = np.arange( np.min(x) + xwindow/2, np.max(x) + xwindow/2, xwindow)

   for xcenter in xcenters:
      xselect = x[np.logical_and(x >  xcenter-xwindow/2, x <= xcenter+xwindow/2)]
      yselect = y[np.logical_and(x >  xcenter-xwindow/2, x <= xcenter+xwindow/2)]
      
      # # Debug: double-check the data binning by uncommenting the following code:
      # #  NOTE: This will plot stuff over top of any plot that's already active
      # plt.plot(x, y, 'ko')
      # plt.plot(xselect, yselect, 'r.')
      # plt.show()
      # plt.clf()
      # import pdb; pdb.set_trace()

      validIdx = ~np.isnan(yselect)
      if len(yselect[validIdx]) >= 2:
         medians  = np.append(medians, np.nanmedian(yselect[validIdx]))
         q75, q25 = np.percentile(yselect[validIdx], [75 ,25])
         q25s     = np.append(q25s, q25)
         q75s     = np.append(q75s, q75)
         IQRs     = np.append(IQRs, q75 - q25)
      else:
         medians  = np.append(medians, np.nan)
         q25s     = np.append(q25s, np.nan)
         q75s     = np.append(q75s, np.nan)
         IQRs     = np.append(IQRs, np.nan)

   return (xcenters, medians, q25s, q75s)

def runningMean(x, y, xwindow, xcenterstart=None):
   sortIdx = np.argsort(x)
   x = x[sortIdx]
   y = y[sortIdx]

   means    = np.array([])
   stddevs  = np.array([])
   
   if xcenterstart is not None:
      xcenters = np.arange( xcenterstart,          np.max(x) - xwindow/2, xwindow)
   else:
      xcenters = np.arange( np.min(x) + xwindow/2, np.max(x) - xwindow/2, xwindow)

   for xcenter in xcenters:
      windowstart = np.min( np.where( x >  xcenter-xwindow/2 ) )
      windowend   = np.max( np.where( x <= xcenter+xwindow/2 ) )
      ywindow     = y[windowstart : windowend]
      
      validIdx = ~np.isnan(ywindow)
      if len(ywindow[validIdx]) >= 2:
         means    = np.append(means, np.nanmean(ywindow[validIdx]))
         stddevs  = np.append(stddevs, np.nanstd(ywindow[validIdx]))
      else:
         means    = np.append(means, np.nan)
         stddevs  = np.append(stddevs, np.nan)

      # Debug: double-check the data binning by uncommenting the following code:
      #  NOTE: This will plot stuff over top of any plot that's already active
      # plt.plot(x, y, 'ko')
      # plt.plot(x[windowstart : windowend], y[windowstart : windowend], 'r.')
      # plt.show()
      # plt.clf()
      # import pdb; pdb.set_trace()

   return (xcenters, means, stddevs)
