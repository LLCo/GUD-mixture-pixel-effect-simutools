# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt

class GUDcalculate:
    
    def __init__(self):
        print('')
                        
    def getMixNDVIGUD(NDVImix, A_abcdMatrix , B_abcdMatrix, GUDA ,GUDB):
        minus = A_abcdMatrix - NDVImix
        minusAbs = np.abs(minus).mean(axis = -1)
        d1,d2,d3,d4 = minusAbs.shape
        _positon = np.argmin(minusAbs)
        d1, d = divmod(_positon, d2*d3*d4)
        d2, d = divmod(d, d3*d4)
        d3, d4 = divmod(d, d4)
        print(minusAbs)
        print(minusAbs[d1,d2,d3,d4])
        return(A_abcdMatrix[d1,d2,d3,d4,:])
        
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
    '''    
    def drawFmLine():
        F_abcdMatrix,A_abcdMatrix,B_abcdMatrix = GUDcalculate.getAllLine()
        fmNum = shape(F_abcdMatrix)[0]
        for i in range(fmNum):
    '''
    
    def getFirstMaxValue(line):
        valTemp = -1000
        for index,val in enumerate(line):
            if(val < valTemp):
                return(index)
            else: valTemp = val
        print('error')
        return(-1)
        
    def getMatrixGUD(F_abcdMatrix):
        shape = np.shape(F_abcdMatrix)
        #print(shape)
        minusShape = list(shape)
        minusShape[-1] = minusShape[-1] - 1
        derivative = np.zeros(minusShape)
        derivative = F_abcdMatrix[:,:,:,:,1:] - F_abcdMatrix[:,:,:,:,:-1]
        derivative2 = derivative[:,:,:,:,1:] - derivative[:,:,:,:,:-1]
        derivative3 = derivative2[:,:,:,:,1:] - derivative2[:,:,:,:,:-1]
        GUD = np.zeros([shape[0],shape[1],shape[2],shape[3]])
        for i in range(shape[0]):
            for j in range(shape[1]):
                for m in range(shape[2]):
                    for n in range(shape[3]):
                        GUD[i,j,m,n] = GUDcalculate.getFirstMaxValue(derivative3[i,j,m,n,:])
        #return(GUD,derivative2,derivative,derivative3)
        #return(float(GUD) / ((shape[0] - 3)/shape[0]))
        #print(GUD)
        #print(np.shape(GUD))
        return[(GUD / (float(362)/365)),derivative3]

        
    def getFmline(GUD):
        Fmstep = np.shape(GUD)[0]
        #xstick = ['30%','40%','50%','60%','70%']
        x = range(0,11)
        #yA = np.zeros(Fmstep)
        #yB = np.zeros(Fmstep)
        yMix = np.zeros(Fmstep)
        for i in x:
            yMix[i] = GUD[i].mean()
        plt.figure()
        print(x)
        print(yMix)
        #yMix = yMix - yMix[0]
        plt.plot(x,yMix)
        axe = plt.gca()
        axe.set_xlabel('fm percentage');
        axe.set_ylabel('GUD Day')
        axes = plt.gca()
        axes.set_xticks(x)
        #axes.set_xticklabels(xstick,rotation = 40)
        plt.show()
        
    def getNDVImaxLine():
        '''
        控制的变量为：
        A:
            a:10
            b:-007
            d:
        B:
            a:12.1 (A，B地物有30天的返青期隔)
            b:-007 (返青期到成熟期所需要的时间不变)
            d:A,B地物的最小值不变
        '''
        return
        
    def getNDVIminLine():
        return
    
    def getAllLine():
        #parameter initialize
        #location: Fm, D, C, A, B, Time
        #initialize Line A
        #A_a=10
        #B_a=12.1
        #A_b=-0.007
        #A_c=0.7
        #A_d=0.1
        #
        '''
        A + B
        '''
        step = 365
        time = np.arange(0,step,1)
        A_a_range = np.arange(8.6, 10, 0.2)
        B_a_range = np.arange(12.1, 13.5, 0.2)
        b_range = np.arange(-0.08,-0.061,0.005)
        c_range = np.arange(0.3,0.81,0.1)
        d_range = np.arange(0.1, 0.31, 0.04)
        fa = 0.5
        fb = 0.5
        
        lengthBrange = len(b_range)
        bMatrix = np.zeros((lengthBrange, step))
        for i in range(lengthBrange):
            bMatrix[i,:] = b_range[i] * time
            
        lengthArange = len(A_a_range)
        A_abMatrix = np.zeros([lengthArange,lengthBrange,step])
        B_abMatrix = np.zeros([lengthArange,lengthBrange,step])
        for i in range(len(A_a_range)):
            A_abMatrix[i,:,:] = A_a_range[i] + bMatrix
            B_abMatrix[i,:,:] = B_a_range[i] + bMatrix
        
        A_abMatrix = 1 / (np.exp(A_abMatrix) + 1) #为A的exp部分
        B_abMatrix = 1 / (np.exp(B_abMatrix) + 1) #为B的exp部分
        '''
        C + D
        '''
        lengthCrange  = len(c_range)
        lengthDrange  = len(d_range)
        A_abcMatrix = np.zeros([lengthCrange,lengthArange,lengthBrange,step])
        B_abcMatrix = np.zeros([lengthCrange,lengthArange,lengthBrange,step])
        
        for i in range(lengthCrange):
            A_abcMatrix[i,:,:,:] = c_range[i] * A_abMatrix
            B_abcMatrix[i,:,:,:] = c_range[i] * B_abMatrix
        
        A_abcdMatrix = np.zeros([lengthDrange,lengthCrange,lengthArange,lengthBrange,step])
        B_abcdMatrix = np.zeros([lengthDrange,lengthCrange,lengthArange,lengthBrange,step])
        for i in range(lengthDrange):
            A_abcdMatrix[i,:,:,:,:] = d_range[i] * A_abcMatrix
            B_abcdMatrix[i,:,:,:,:] = d_range[i] * B_abcMatrix
                
        return(A_abcdMatrix, B_abcdMatrix)
    
#GUDins =  GUDcalculate()
A_abcdMatrix, B_abcdMatrix = GUDcalculate.getAllLine()
GUDA,derivative3A = GUDcalculate.getMatrixGUD(A_abcdMatrix)
GUDB,derivative3B = GUDcalculate.getMatrixGUD(B_abcdMatrix)
array = GUDcalculate.getMixNDVIGUD(0.5*A_abcdMatrix[1,1,1,1]\
        + 0.5*B_abcdMatrix[1,1,1,1],A_abcdMatrix , B_abcdMatrix, GUDA ,GUDB)
print(array)
plt.plot(range(365), array)
plt.plot(range(365), 0.5*A_abcdMatrix[1,1,1,1] + 0.5*B_abcdMatrix[1,1,1,1])
plt.show()

'''
print('ok')
shape = np.shape(A_abcdMatrix)
for i in range(shape[0]):
    for j in range(shape[1]):
        for m in range(shape[2]):
            for n in range(shape[3]):
                plt.figure()
                length = len(A_abcdMatrix[i,j,m,n,:])
                plt.plot(np.arange(0,length,1), A_abcdMatrix[i,j,m,n,:])
                plt.axvline(GUDA[i,j,m,n])
                plt.show()
                plt.figure()
                length = len(derivative3A[i,j,m,n,:])
                plt.plot(np.arange(0,length,1), derivative3A[i,j,m,n,:])
                plt.axvline(GUDA[i,j,m,n])
                plt.show()
'''
#print(np.shape(A_abcdMatrix))

#GUDcalculate.getFmline(GUD)

#plt.figure()
#plt.plot(range(365), A_abcdMatrix[3,3,3,6,:])
#plt.plot(range(365), A_abcdMatrix[3,3,3,3,:])
#plt.show()

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
'''
A_a=10
A_b=-0.007
A_c=0.7
A_d=0.1

timeseris1 = GUDins.getNDVITimeSeris(A_a,A_b,A_c,A_d)
timeseris2 = GUDins.getNDVITimeSeris(A_a + 2.1,A_b,A_c,A_d)

plt.figure()
length = len(timeseris1)
plt.plot(np.arange(0,length,1), timeseris1)
length = len(timeseris2)
plt.plot(np.arange(0,length,1), timeseris2)
plt.show()
'''
