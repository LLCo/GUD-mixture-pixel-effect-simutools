'''
import math
import matplotlib as mpl
from scipy.optimize import curve_fit
import numpy as np

#data
F1=[735.0,696.0,690.0,683.0,680.0,678.0,679.0,675.0,671.0,669.0,668.0,664.0,664.0]
t1=[1,90000.0,178200.0,421200.0,505800.0,592200.0,768600.0,1036800.0,1371600.0,1630800.0,1715400.0,2345400.0,2409012.0]

F1n=np.array(F1)
t1n=np.array(t1)

plt.plot(t1,F1,'ro',label="original data")

# curvefit
def func(t,a,b):
    return a+b*np.log(t)

t=np.linspace(0,3600*24*28,13)

popt, pcov = curve_fit(func, t1, F1n, maxfev=1000)    

plt.plot(t, func(t, *popt), label="Fitted Curve")

plt.legend(loc='upper left')
plt.show()

'''

import matplotlib.pyplot as plt
import scipy.optimize as optimize
import numpy as np

# data
F1 = np.array([
    735.0, 696.0, 690.0, 683.0, 680.0, 678.0, 679.0, 675.0, 671.0, 669.0, 668.0,
    664.0, 664.0])
t1 = np.array([
    1, 90000.0, 178200.0, 421200.0, 505800.0, 592200.0, 768600.0, 1036800.0,
    1371600.0, 1630800.0, 1715400.0, 2345400.0, 2409012.0])

plt.plot(t1, F1, 'ro', label="original data")

# curvefit

def func(t, a, b):
    return a + b * np.log(t)

popt, pcov = optimize.curve_fit(func, t1, F1, maxfev=1000)
t = np.linspace(1, 3600 * 24 * 28, 13)
plt.plot(t, func(t, *popt), label="Fitted Curve")
plt.legend(loc='upper left')
plt.show()