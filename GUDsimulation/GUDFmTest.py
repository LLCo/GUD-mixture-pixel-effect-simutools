# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
def getFirstMaxValue(line):
    valTemp = -1000
    for index,val in enumerate(line):
        if(val < valTemp):
            return(index)
        else: valTemp = val
    print('error')
    return(-1)
    
def getNDVITimeSeris(a,b,c,d,time):
    expValue = np.exp(a + b*time)
    timeseris = c/(1 + expValue) + d
    return(timeseris)

def getMatrixGUD(timeSeris):
    shape = np.shape(timeSeris)
    minusShape = list(shape)
    minusShape[-1] = minusShape[-1] - 1
    derivative = np.zeros(minusShape)
    #print(timeSeris)
    derivative = timeSeris[1:] - timeSeris[:-1]
    #print(derivative)
    derivative2 = derivative[1:] - derivative[:-1]
    derivative3 = derivative2[1:] - derivative2[:-1]
    GUD = getFirstMaxValue(derivative3)
    #return(GUD,derivative2,derivative,derivative3)
    return(float(GUD) / ((shape[0] - 3)/shape[0]))

def getMixNDVI(timeSerisA, timeSerisB):
    fm = np.arange(0, 1.01, 0.1)
    mixNDVI = np.zeros([len(fm),len(timeSerisA)])
    for index,val in enumerate(fm):
        mixNDVI[index,:] =  val * timeSerisA\
            + (1 - val) * timeSerisB
    return(mixNDVI)
    
'''

不变量为：
A:
    a:10
    b:-0.07
    c:0.7
    d:0.1
B:
    a:12.1
    b:-0.07
    c:0.7
    d:0.1

(A，B地物有30天的返青期隔)
(返青期到成熟期所需要的时间不变)
(A,B地物NDVI的最大值变化)
(A,B地物NDVI的最小值不变)


变量为：
Fm:
    反应的是A，B两种地物类型混合程度对GUD的影像
    
'''

time = 365
timeX = np.arange(0,time,1)
a_A=10
a_B=12.1
b=-0.07
c=0.7
d=0.1

serisA = getNDVITimeSeris(a_A,b,c,d,timeX)
serisB = getNDVITimeSeris(a_B,b,c,d,timeX)

plt.figure(figsize = (14,5))
axes = plt.subplot(121)
axes.plot(timeX , serisA ,label = 'serisA');
axes.plot(timeX , serisB ,label = 'serisB');


GUD_A = getMatrixGUD(serisA)
print('GUD_A: ')
print(GUD_A)

GUD_B = getMatrixGUD(serisB)
print('GUD_B: ')
print(GUD_B)

serisMix = getMixNDVI(serisA,serisB)
fmStep = np.shape(serisMix)[0]
GUDmix = np.zeros(fmStep)
for i in range(fmStep):
    GUDmix[i] = getMatrixGUD(serisMix[i])
print(GUDmix)
axes.plot(timeX , serisMix[5],'--' ,label = 'serisMix fm = 50%');
axes.set_xlabel('day')
axes.set_ylabel('NDVI')
axes.grid()
axes.legend() 


axes2 = plt.subplot(122)
GUDmixA = GUDmix - GUDmix[0]
GUDmixB = GUDmix - GUDmix[-1]
GUDmixB = GUDmixB[::-1]
fm = np.arange(0, 1.01, 0.1)
plt.ylabel
axes2.plot(fm , GUDmixA,'o-',label = 'Fa');
axes2.plot(fm , GUDmixB,'o-',label = 'Fb');
axes2.set_xlabel('Percentage')
axes2.set_ylabel('Delta GUD')
axes2.legend() 
print(GUDmixA)
print(GUDmixB)
axes2.grid()
plt.show();

plt.figure()
plt.grid()
plt.plot(fm,GUDmix,'o-',label = 'serisMix change with Fa')
axe = plt.gca()
axe.set_xlabel('Fa Percentage')
axe.set_ylabel('mix GUD')
plt.legend()
plt.show()




