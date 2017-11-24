import numpy as np
import matplotlib.pyplot as plt


def ndvi(nir,r):
    return (nir - r)/(nir  + r)

a = np.arange(0.1,1,0.1)
print(a)

NDVImix = np.zeros(len(a))
NDVImixl = np.zeros(len(a))

NIRv = 0.9
Rv = 0.3
NIRs = 0.4
Rs = 0.3



for i in range(len(a)):
    NDVImix[i] = a[i] * ndvi(NIRv,Rv) + (1 - a[i]) * ndvi(NIRs,Rs)
    
    NDVImixl[i] = ndvi(a[i] * NIRv + (1 - a[i]) * NIRs,a[i] * Rv + (1 - a[i]) * Rs)

plt.plot(a,NDVImix)
plt.plot(a,NDVImixl)
