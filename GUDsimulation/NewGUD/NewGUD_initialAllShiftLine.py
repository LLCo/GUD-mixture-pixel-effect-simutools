# -*- coding: utf-8 -*-
'''
Shift Test:
    
A:
'''
import numpy as np
import matplotlib.pyplot as plt
import NewGUD_GetInitialLine
import NewGUD_GUD

'''
get initial parameter
a,b,c,d,a_down,b_down

'''


'''
A:
serisB,serisA = NewGUD_GetInitialLine.getInitialAB()
serisBParameter = NewGUD_GetInitialLine.initialAParameter
serisAParameter = NewGUD_GetInitialLine.initialBParameter

shift_NDVImax = np.arange(0,0.51,0.1)
shift_NDVImin = np.arange(0,0.21,0.05)
shift_time = np.arange(0,20,4)
shift_MaturityPeriod = np.arange(-1,1.1,0.5)
'''


    
serisA,serisB = NewGUD_GetInitialLine.getInitialAB()
serisAParameter = NewGUD_GetInitialLine.initialAParameter
serisBParameter = NewGUD_GetInitialLine.initialBParameter

shift_NDVImax = np.arange(0,0.51,0.1)
shift_NDVImin = np.arange(0,0.21,0.05)
shift_time = np.arange(0,-20,-4)
shift_MaturityPeriod = np.arange(-1,1.1,0.5)


'''
NDVImaxShift
'''

plt.figure(figsize= (16,10))
ax = plt.subplot(221)
serisNDVImax = np.zeros([len(shift_NDVImax),366])
for index,val in enumerate(shift_NDVImax):
    a,b,c,d,a_down,b_down = NewGUD_GetInitialLine.NDVImaxShift(\
                                        serisAParameter['a'],\
                                        serisAParameter['b'],\
                                        serisAParameter['c'],\
                                        serisAParameter['d'],\
                                        serisAParameter['a_down'],\
                                        serisAParameter['b_down'],
                                        shift = val)
    serisNDVImax[index,:] = NewGUD_GetInitialLine.getInitialLine(a,b,c,d,a_down,b_down)
    ax.plot(range(366),serisNDVImax[index,:],color = (index/(len(shift_NDVImax)),1,0))
    ax.set_title('NDVImax')
ax.plot(range(366),serisB,'r--')

'''
NDVIminShift
'''

ax = plt.subplot(222)
serisNDVImin = np.zeros([len(shift_NDVImin),366])
for index,val in enumerate(shift_NDVImin):
    a,b,c,d,a_down,b_down = NewGUD_GetInitialLine.NDVIminShift(\
                                        serisAParameter['a'],\
                                        serisAParameter['b'],\
                                        serisAParameter['c'],\
                                        serisAParameter['d'],\
                                        serisAParameter['a_down'],\
                                        serisAParameter['b_down'],
                                        shift = val)
    serisNDVImin[index,:] = NewGUD_GetInitialLine.getInitialLine(a,b,c,d,a_down,b_down)
    ax.plot(range(366),serisNDVImin[index,:],color = (index/(len(shift_NDVImax)),1,0))
    ax.set_title('NDVImin')
ax.plot(range(366),serisB,'r--')
'''
NDVIminShift
'''
ax = plt.subplot(223)
serisTime = np.zeros([len(shift_time),366])
for index,val in enumerate(shift_time):
    a,b,c,d,a_down,b_down = NewGUD_GetInitialLine.timeSerisShift(\
                                        serisAParameter['a'],\
                                        serisAParameter['b'],\
                                        serisAParameter['c'],\
                                        serisAParameter['d'],\
                                        serisAParameter['a_down'],\
                                        serisAParameter['b_down'],
                                        shift = val)
    serisTime[index,:] = NewGUD_GetInitialLine.getInitialLine(a,b,c,d,a_down,b_down)
    ax.plot(range(366),serisTime[index,:],color = (index/(len(shift_NDVImax)),1,0))
    ax.set_title('TimeGUD')
ax.plot(range(366),serisB,'r--')
'''
NDVIminShift
'''

ax = plt.subplot(224)
serisMaturityPeriod = np.zeros([len(shift_MaturityPeriod),366])
for index,val in enumerate(shift_MaturityPeriod):
    a,b,c,d,a_down,b_down = NewGUD_GetInitialLine.maturityPeriodShift(\
                                        serisAParameter['a'],\
                                        serisAParameter['b'],\
                                        serisAParameter['c'],\
                                        serisAParameter['d'],\
                                        serisAParameter['a_down'],\
                                        serisAParameter['b_down'],
                                        shift = val)
    serisMaturityPeriod[index,:] = NewGUD_GetInitialLine.getInitialLine(a,b,c,d,a_down,b_down)
    ax.plot(range(366),serisMaturityPeriod[index,:],color = (index/(len(shift_NDVImax)),1,0))
    ax.set_title('MaturityPeriod')
ax.plot(range(366),serisB,'r--')

plt.show()


'''
serisB

serisNDVImax
serisNDVImin
serisTime
serisMaturityPeriod
'''
plt.figure(figsize= (16,10))
ax1 = plt.subplot(221)
ax2 = plt.subplot(222)
ax3 = plt.subplot(223)
ax4 = plt.subplot(224)

serisNDVImax = (serisNDVImax + serisB) / 2
serisNDVImin = (serisNDVImin + serisB) / 2
serisTime = (serisTime + serisB) / 2
serisMaturityPeriod = (serisMaturityPeriod + serisB) / 2

for index,val in enumerate(serisNDVImax):
    ax1.plot(range(366),val,color = (index/(len(shift_NDVImax)),1,0))
    ax1.set_title('NDVImax')
    
for index,val in enumerate(serisNDVImin):
    ax2.plot(range(366),val,color = (index/(len(shift_NDVImax)),1,0))
    ax2.set_title('NDVIminGUD')
for index,val in enumerate(serisTime):
    ax3.plot(range(366),val,color = (index/(len(shift_NDVImax)),1,0))
    ax3.set_title('TimeGUD')
for index,val in enumerate(serisMaturityPeriod):
    ax4.plot(range(366),val,color = (index/(len(shift_NDVImax)),1,0))
    ax4.set_title('MaturityPeriod')
plt.show()

'''
draw line
'''
plt.figure(figsize= (16,10))
ax1 = plt.subplot(221)
ax2 = plt.subplot(222)
ax3 = plt.subplot(223)
ax4 = plt.subplot(224)

serisNDVImaxGUDs = []
for index in serisNDVImax:
    serisNDVImaxGUDs.append(NewGUD_GUD.phenology(index))
ax1.plot(range(len(serisNDVImaxGUDs)),serisNDVImaxGUDs,'ro--')
ax1.set_title('NDVImax')

serisNDVIminGUDs = []
for index in serisNDVImin:
    serisNDVIminGUDs.append(NewGUD_GUD.phenology(index))
ax2.plot(range(len(serisNDVIminGUDs)),serisNDVIminGUDs,'go--')
ax2.set_title('NDVIminGUD')

serisTimeGUDs = []
for index in serisTime:
    serisTimeGUDs.append(NewGUD_GUD.phenology(index))
ax3.plot(range(len(serisTimeGUDs)),serisTimeGUDs,'bo--')
ax3.set_title('TimeGUD')

serisMaturityPeriodGUDs = []
for index in serisMaturityPeriod:
    serisMaturityPeriodGUDs.append(NewGUD_GUD.phenology(index))
ax4.plot(range(len(serisMaturityPeriodGUDs)),serisMaturityPeriodGUDs,'ko--')
ax4.set_title('MaturityPeriod')
