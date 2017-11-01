# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import NewGUD_GetInitialLine
import NewGUD_GUD

serisA,serisB = NewGUD_GetInitialLine.getInitialAB()
serisAParameter = NewGUD_GetInitialLine.initialAParameter
serisBParameter = NewGUD_GetInitialLine.initialBParameter

shift_timeB = np.arange(0,21,4)
shift_timeA = np.arange(0,-21,-4)
fm = np.arange(0,1.01,0.1)
timeLen = len(shift_timeB)
fmLen = len(fm)
num = len(serisA)

a,b,c,d,a_down,b_down = NewGUD_GetInitialLine.timeSerisShift(\
                            NewGUD_GetInitialLine.initialAParameter['a'],\
                            NewGUD_GetInitialLine.initialAParameter['b'],\
                            NewGUD_GetInitialLine.initialAParameter['c'],\
                            NewGUD_GetInitialLine.initialAParameter['d'],\
                            NewGUD_GetInitialLine.initialAParameter['a_down'],\
                            NewGUD_GetInitialLine.initialAParameter['b_down'],
                            shift = -20)
serisAShift20 = NewGUD_GetInitialLine.getInitialLine(a,b,c,d,a_down,b_down)
    
a,b,c,d,a_down,b_down = NewGUD_GetInitialLine.timeSerisShift(\
                            NewGUD_GetInitialLine.initialBParameter['a'],\
                            NewGUD_GetInitialLine.initialBParameter['b'],\
                            NewGUD_GetInitialLine.initialBParameter['c'],\
                            NewGUD_GetInitialLine.initialBParameter['d'],\
                            NewGUD_GetInitialLine.initialBParameter['a_down'],\
                            NewGUD_GetInitialLine.initialBParameter['b_down'],
                            shift = 20)
serisBShift20 = NewGUD_GetInitialLine.getInitialLine(a,b,c,d,a_down,b_down)

plt.plot(range(num),serisA,'r')
plt.plot(range(num),serisB,'b')
plt.plot(range(num),serisAShift20,'r--')
plt.plot(range(num),serisBShift20,'b--')

print(NewGUD_GUD.phenology(serisA))
print(NewGUD_GUD.phenology(serisAShift20))

val = 0.2
serisFm = val * serisA + (1 - val) * serisB
a = NewGUD_GUD.phenology(serisFm)
print(a)
serisFm = 0.3 * serisA + (1 - 0.3) * serisB
a1 = NewGUD_GUD.phenology(serisFm)
print(a1)
serisFmShift = val * serisAShift20 + (1 - val) * serisB
b = NewGUD_GUD.phenology(serisFmShift)
print(b)
print(b - a)

'''
val = 0.4
serisFm = val * serisB + (1 - val) * serisA
a = NewGUD_GUD.phenology(serisFm)
print(a)
serisFmShift = val * serisBShift20 + (1 - val) * serisA
b = NewGUD_GUD.phenology(serisFmShift)
print(b)
print(b - a)
'''