# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import NewGUD_GetInitialLine
import NewGUD_GUD
from mpl_toolkits.axes_grid1 import make_axes_locatable
'''
get initial parameter
a,b,c,d,a_down,b_down

'''

serisA,serisB = NewGUD_GetInitialLine.getInitialAB()
serisAParameter = NewGUD_GetInitialLine.initialAParameter
serisBParameter = NewGUD_GetInitialLine.initialBParameter

shift_timeB = np.arange(0,21,4)
shift_timeA = np.arange(0,-21,-4)
fm = np.arange(0,1.01,0.1)
timeLen = len(shift_timeB)
fmLen = len(fm)
num = len(serisA)

Alist = np.zeros([timeLen, num])
Blist = np.zeros([timeLen, num])
fixlist = np.zeros([fmLen, timeLen, num])
fixlistGUD = np.zeros([fmLen, timeLen])

plt.figure()
plt.plot(range(num),serisA,'b',range(num),serisB,'r')

for i in range(timeLen):
    a,b,c,d,a_down,b_down = NewGUD_GetInitialLine.timeSerisShift(\
                                NewGUD_GetInitialLine.initialAParameter['a'],\
                                NewGUD_GetInitialLine.initialAParameter['b'],\
                                NewGUD_GetInitialLine.initialAParameter['c'],\
                                NewGUD_GetInitialLine.initialAParameter['d'],\
                                NewGUD_GetInitialLine.initialAParameter['a_down'],\
                                NewGUD_GetInitialLine.initialAParameter['b_down'],
                                shift = shift_timeA[i])
    Alist[i] = NewGUD_GetInitialLine.getInitialLine(a,b,c,d,a_down,b_down)
    a,b,c,d,a_down,b_down = NewGUD_GetInitialLine.timeSerisShift(\
                                NewGUD_GetInitialLine.initialBParameter['a'],\
                                NewGUD_GetInitialLine.initialBParameter['b'],\
                                NewGUD_GetInitialLine.initialBParameter['c'],\
                                NewGUD_GetInitialLine.initialBParameter['d'],\
                                NewGUD_GetInitialLine.initialBParameter['a_down'],\
                                NewGUD_GetInitialLine.initialBParameter['b_down'],
                                shift = shift_timeB[i])
    Blist[i] = NewGUD_GetInitialLine.getInitialLine(a,b,c,d,a_down,b_down)
    plt.plot(range(num),Alist[i],color = (1 - float(i)/timeLen,0,0))
    plt.plot(range(num),Blist[i],color = (0,0,1 - float(i)/timeLen))
    

for i in range(fmLen):
    fixlist[i] = fm[i] * Alist + (1 - fm[i]) * Blist[0]
for i in range(fmLen):
    for j in range(timeLen):
        fixlistGUD[i,j] = NewGUD_GUD.phenology(fixlist[i,j])
        #print(fixlistGUD[i,j])
'''
plt.figure(figsize = (10,10))
ax = plt.gca()
im = ax.imshow(fixlistGUD)
'''

for i in range(fmLen):
    fixlist[i] = fm[i] * Alist + (1 - fm[i]) * Blist[0]
for i in range(fmLen):
    for j in range(timeLen):
        fixlistGUD[i,j] = NewGUD_GUD.phenology(fixlist[i,j])
        #print(fixlistGUD[i,j])

plt.figure(figsize = (10,10))
ax = plt.gca()
im = ax.imshow(fixlistGUD)

#print(im)
# create an axes on the right side of ax. The width of cax will be 5%
# of ax and the padding between cax and ax will be fixed at 0.05 inch.
'''
ax.set_xlabel('delta GUD');
ax.set_ylabel('Fa');
ax.set_xticks(range(len(b_range)))
ax.set_yticks(range(11))
ax.set_xticklabels(list(map(str,b_range)))
label = ['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%']
label.reverse()
ax.set_yticklabels(label)
plt.title('mix GUD')

'''
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax)
plt.show()
        
print(fixlistGUD[9])
print(fixlistGUD[5])
print(fixlistGUD[3])
