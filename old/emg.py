# -*- coding: utf-8 -*-
'''
Exponentially Modified Gaussian (EMG)
http://en.wikipedia.org/wiki/Exponentially_modified_Gaussian_distribution
'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

def emg(x,y0,A,xc,w,t0):
  '''
  y0 = initial value
  A = amplitude
  xc = center of peak
  w = width of peak
  t0 = modification factor (skewness; t0 > 0 )
  '''
  y=np.zeros(0)
  for cx in x:
    z = (cx-xc)/w - w/t0
    expFactor = np.exp(0.5*(w/t0)**2.0 - (cx-xc)/t0)
    cy = y0+(A/t0)*expFactor*(0.5+0.5*erf(z/np.sqrt(2)))
    y=np.hstack([y,cy])
  return y

def erf(x):
  erf_func = lambda t: np.exp(-1.0*t*t)
  return (2.0/np.sqrt(np.pi))*((quad(erf_func,0,x))[0])

cFig=plt.figure()
cAx=cFig.add_subplot(111)
x=np.linspace(1,100,1000)
y=emg(x,0.0,10.,50.,1.0,5.0)
cAx.plot(x,y)
plt.show()
plt.close()