# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

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
    #return(GUD)

def getMixNDVI(timeSerisA, timeSerisB):
    fm = np.arange(0, 1.01, 0.1)
    mixNDVI = np.zeros([len(fm),len(timeSerisA)])
    for index,val in enumerate(fm):
        mixNDVI[index,:] =  val * timeSerisA\
            + (1 - val) * timeSerisB
    return(mixNDVI)
    
def getFirstMaxValue(line):
    valTemp = -1000
    for index,val in enumerate(line):
        if(val < valTemp):
            return(index)
        else: valTemp = val
    print('error')
    return(-1)
    
'''

参数为：
A:
    a:10~~~
    b:-07~~~
    c:0.7
    d:0.1
B:
    a:12.1~~~
    b:-07~~~
    c:0.7
    d:0.1
    
(A，B地物有30天的返青期隔)
(返青期到成熟期所需要的时间不变)
(A,B地物NDVI的最大值不变)
(A,B地物NDVI的最小值变化)


变量为：
Fm:
    反应的是A，B两种地物类型混合程度对GUD的影像
b:
    最大值变化范围为：b_range = np.arange(0.06,0.08,0.003)
a:
    与之对应的：a_range = 10 + (b_range - 0.07) * 172
'''
time = 365
timeX = np.arange(0,time,1)
a_B = 12.1
a_A = 10
b = -0.07
c = 0.7
d = 0.1
b_range = - np.arange(0.06,0.08,0.003)[::-1]
Fm = np.arange(0,1.01,0.1)


'''

t = 111
a_range = 10 - (b_range + 0.07) * t
print(a_range + b_range*t)
print(b_range)
print(a_range)

serisB = getNDVITimeSeris(a_B,b,c,d,timeX)
serisAList = np.zeros([len(b_range),time])
for index,val in enumerate(b_range):
    serisAList[index,:] = getNDVITimeSeris\
        (a_range[index],b_range[index],c,d,timeX)

plt.figure(figsize = (10,6))
plt.plot(timeX,serisB,'g',label= 'serisB')
for index,val in enumerate(b_range):
    plt.plot(timeX,serisAList[index,:],'--',\
             label= 'serisA b = ' + str(val),\
             color = (1,index/(len(b_range)),0))
#GUD,y = getMatrixGUD(serisB)
#plt.plot(range(364),y)
plt.grid()
plt.legend()
plt.show()

GUDserisB = getMatrixGUD(serisB)
minusMatrix = np.zeros([len(Fm),len(b_range)])
for indexi,vali in enumerate(Fm):
    for indexj,valj in enumerate(b_range):
        mixSeris = vali * serisB + (1 - vali)*serisAList[indexj,:]
        GUDmix = getMatrixGUD(mixSeris)
        minusMatrix[indexi,indexj] = GUDmix
        #colorValue = (GUDmix - 142)/30
        #plt.plot(valj,vali,'o',color = (0, colorValue, colorValue))

plt.figure(figsize = (10,10))
ax = plt.gca()
im = ax.imshow(minusMatrix)
#print(im)
# create an axes on the right side of ax. The width of cax will be 5%
# of ax and the padding between cax and ax will be fixed at 0.05 inch.
ax.set_xlabel('A\'s b Value');
ax.set_ylabel('Fa');
ax.set_xticks(range(len(b_range)))
ax.set_yticks(range(11))
ax.set_xticklabels(list(map(str,b_range)))
label = ['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%']
label.reverse()
ax.set_yticklabels(label)
plt.title('mix GUD')
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax)
plt.show()
print(minusMatrix) 
print(minusMatrix.mean(axis = 1))
print()

plt.figure(figsize = (6,6))
temp = minusMatrix.mean(axis = 0)
plt.plot(range(len(b_range)),temp,'ro--')
ax = plt.gca()
ax.set_ylabel('mix GUD')
ax.set_xlabel('Maturity A\'NDVI');
#ax.set_xticks(range(len(b_range)))
#ax.set_xticklabels(list(map(str,np.arange(0.1,0.31,0.05))))
plt.show()
'''

t = 142
a_range = 12.1 - (b_range + 0.07) * t
print(a_range + b_range*t)
print(b_range)
print(a_range)

serisA = getNDVITimeSeris(a_A,b,c,d,timeX)
serisBList = np.zeros([len(b_range),time])
for index,val in enumerate(b_range):
    serisBList[index,:] = getNDVITimeSeris\
        (a_range[index],b_range[index],c,d,timeX)

plt.figure(figsize = (10,6))
plt.plot(timeX,serisA,'r',label= 'serisA')
for index,val in enumerate(b_range):
    plt.plot(timeX,serisBList[index,:],'--',\
             label= 'serisB b = ' + str(val),\
             color = (1 - index/(len(b_range)),1,0))
#GUD,y = getMatrixGUD(serisB)
#plt.plot(range(364),y)
plt.grid()
plt.legend()
plt.show()

GUDserisB = getMatrixGUD(serisA)
minusMatrix = np.zeros([len(Fm),len(b_range)])
for indexi,vali in enumerate(Fm):
    for indexj,valj in enumerate(b_range):
        mixSeris = vali * serisA + (1 - vali)*serisBList[indexj,:]
        GUDmix = getMatrixGUD(mixSeris)
        minusMatrix[indexi,indexj] = GUDmix
        #colorValue = (GUDmix - 142)/30
        #plt.plot(valj,vali,'o',color = (0, colorValue, colorValue))

plt.figure(figsize = (10,10))
ax = plt.gca()
im = ax.imshow(minusMatrix)
#print(im)
# create an axes on the right side of ax. The width of cax will be 5%
# of ax and the padding between cax and ax will be fixed at 0.05 inch.
ax.set_xlabel('B\'s b value');
ax.set_ylabel('Fb');
ax.set_xticks(range(len(b_range)))
ax.set_yticks(range(11))
ax.set_xticklabels(list(map(str,b_range)))
label = ['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%']
label.reverse()
ax.set_yticklabels(label)
plt.title('mix GUD')
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax)
plt.show()
print(minusMatrix) 
print(minusMatrix.mean(axis = 1))
print()

plt.figure(figsize = (6,6))
temp = minusMatrix.mean(axis = 0)
plt.plot(range(len(b_range)),temp,'ro--')
ax = plt.gca()
ax.set_ylabel('mix GUD')
ax.set_xlabel('Maturity B\'NDVI');
#ax.set_xticks(range(len(b_range)))
#ax.set_xticklabels(list(map(str,np.arange(0.1,0.31,0.05))))
plt.show()
