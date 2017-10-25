# -*- coding: utf-8 -*-
'''
Shift Test:
    
For A:
    
'''
import numpy as np
import matplotlib.pyplot as plt
import NewGUD_GetInitialLine
import NewGUD_GUD

serisA,serisB = NewGUD_GetInitialLine.getInitialAB()
num = len(serisA)
fm= np.arange(0.3,0.81,0.1)
fmNum = len(fm)
serisFm = np.zeros([fmNum,num])

for index, val in enumerate(fm):
    serisFm[index] = val * serisA + (1 - val) * serisB
    
plt.figure()
plt.plot(range(num),serisA,'r',range(num), serisB,'g')
for index, val in enumerate(serisFm):
    plt.plot(range(num), val,color = (index/(len(fm)),1 - index/(len(fm)),0))
plt.show()

plt.figure()
serisFmGUDsA = []
for val in serisFm:
    serisFmGUDsA.append(NewGUD_GUD.phenology(val))
plt.plot(range(len(serisFmGUDsA)),serisFmGUDsA,'ro--')
plt.title('NDVImax')

print(serisFmGUDsA)
'''
For B :
'''


for index, val in enumerate(fm):
    serisFm[index] = val * serisB + (1 - val) * serisA
    
plt.figure()
plt.plot(range(num),serisA,'r',range(num), serisB,'g')
for index, val in enumerate(serisFm):
    plt.plot(range(num), val,color = (index/(len(fm)),1 - index/(len(fm)),0))
plt.show()

plt.figure()
serisFmGUDsB = []
for val in serisFm:
    serisFmGUDsB.append(NewGUD_GUD.phenology(val))
plt.plot(range(len(serisFmGUDsB)),serisFmGUDsB,'ro--')
plt.title('NDVImax')

serisFmGUDsA = np.array(serisFmGUDsA)
serisFmGUDsB = np.array(serisFmGUDsB)

serisFmGUDsA = serisFmGUDsA - serisFmGUDsA[0]
serisFmGUDsB =  - (serisFmGUDsB - serisFmGUDsB[-1])[::-1]

plt.figure()
plt.plot(range(fmNum),serisFmGUDsA,'bo-',range(fmNum),serisFmGUDsB,'ro-')
plt.show()

print("serisMaturityPeriodGUDs")
