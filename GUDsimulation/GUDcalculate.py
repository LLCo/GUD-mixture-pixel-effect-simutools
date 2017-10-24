# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt

class GUDcalculate:
    step = 3650
    
    def __init__(self):
       self.time = np.arange(0,self.step,1)
       print(self.time)
    
    def getNDVITimeSeris(self,a,b,c,d):
        expValue = np.exp(a + b*self.time)
        self.timeseris = c/(1 + expValue) + d
        return(self.timeseris)
        #print('hello world')
    
    def drawLine(self, ndvi):
        plt.figure()
        length = len(ndvi)
        plt.plot(np.arange(0,length,1), ndvi)
        plt.show()
        
    def getGUD(self):
        derivative =  np.zeros(self.step - 1)
        derivative = self.timeseris[1:] - self.timeseris[0:-1]
        return([np.argmax(derivative),derivative])
        
GUDins =  GUDcalculate()

#parameter initialize
'''
initialize Line A
'''
A_a=10
A_b=-0.007
A_c=0.7
A_d=0.1

'''
initialize Line B
'''
A_a=12.1
A_b=-0.007
A_c=0.7
A_d=0.1

'''
FIRST TEST:
    CHANGE Fm FOR A,B;
    A_Fm = np.arange(0,1,0.01)
    B_Fm = 1 - A_Fm
'''


'''
SECOND TEST:
    CHANGE A_max_NDVI,B_max_NDVI;
    A_max_NDVI = np.arange(0.3,0.8.0.01)
    B_max_NDVI = np.arange(0.3,0.8.0.01)
'''

'''
THRID TEST:
    CHANGE A_min_NDVI,B_min_NDVI;
    A-> d = np.arange(0.1, 0.3, 0.01)
    B-> d = np.arange(0.1, 0.3, 0.01)
'''

'''
FORTH TEST:
    b change range : -0.08到-0.06
    b = np.arange(-0.06, -0.08, 0.001)
'''

'''
FIFTH TEST:
    Delaying the growth period B
    Advancing the growth period A
    A -> a = np.arange(8.6, 10, 0.1)
    B -> a = np.arange(12.1, 13.5, 0.1)
'''

#GUDins.drawLine(timeseris)
#GUD,derivative = GUDins.getGUD()
#print(GUD)
#GUDins.drawLine(derivative)
timeseris1 = GUDins.getNDVITimeSeris(a,b,c,d)
timeseris2 = GUDins.getNDVITimeSeris(a + 2.1,b,c,d)

plt.figure()
length = len(timeseris1)
plt.plot(np.arange(0,length,1), timeseris1)
length = len(timeseris2)
plt.plot(np.arange(0,length,1), timeseris2)
plt.show()
