# -*- coding: utf-8 -*-

'''
; DESCRIPTION:
;       This function is used for deriving phenology time using NDVI-series data
;       Phenology time: t1: greenup onset; t2: maturity onset; t3: senescence onset; t4: dormancy onset
;       Ref:  Zhang et al., (2003), Monitoring vegetation phenology using MODIS, Remote Sensing of Environment, 84: 471-475.
;
; SYNTAX:
;      Result = phenoglogy_zhang( NDVI,  [,NDVIfit=vector] [,KK=vector] )
;
; RETURN VALUE: Returns a vector of [t1,t2,t3,t4].
'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq

def getFirstMaxValue(line):
    valTemp = -1000
    for i in range(len(line)):
        if(line[i] <= valTemp):
            return(i - 1)
        else: 
            valTemp = line[i]
            #print(str(line[i]) + str('...') + str(i))
    #print('error')
    return(-1)
    
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
    #print(GUD)
    #print(np.argmax(derivative3))
    #return(GUD,derivative2,derivative,derivative3)
    GUDnew = GUD / float(363) * 366
    return(GUD,derivative3,GUDnew)

def logistic4(x, A, B, C, D):
    """4PL lgoistic equation."""
    
    expValue = np.exp(A + B*x)
    timeseris = C/(1 + expValue) + D
    return (timeseris)
    
    #return ((A-D)/(1.0+((x/C)**B))) + D

def residuals(p, y, x):
    """Deviations of data from fitted 4PL curve"""
    A,B,C,D = p
    err = y-logistic4(x, A, B, C, D)
    return err

def peval(x, p):
    """Evaluated value at x with current parameters."""
    A,B,C,D = p
    return logistic4(x, A, B, C, D)

def Logistic_regress(x,y):
    #; This function is to logistic regression
    #;Provide an initial guess of the function's parameters.
    #;Compute the parameters.
    
    # Initial guess for parameters
    
    #p0 = [10,-0.07,0.7,0.1]
    #'a':12.1,'b':-0.07,'c':0.7,'d':0.1
    p0 = [12.1,-0.07,0.7,0.1]
    
    # Fit equation using least squares optimization
    plsq = leastsq(residuals, p0, args=(y, x)) #maxfev = 1000
    #print(plsq[0])
    # Plot results
    '''
    plt.plot(x,peval(x,plsq[0]),x,y,'--')
    plt.title('Least-squares 4PL fit to noisy data')
    plt.legend(['Fit', 'Orin'], loc='upper left')
    '''
    '''
    for i, (param, actual, est) in enumerate(zip('ABCD', [A,B,C,D], plsq[0])):
        plt.text(10, 3-i*0.5, '%s = %.2f, est(%s) = %.2f' % (param, actual, param, est))
    plt.savefig('logistic.png')
    '''
    return(plsq[0])


def phenology(NDVI):
    Num = len(NDVI)
    '''
    plt.figure()
    plt.plot(range(Num),NDVI)
    plt.show()
    '''
    
    # find the maximum NDVI value and split NDVI series into Y_NDVI1 and Y_NDVI2
    NDVI_max_index=np.argmax(NDVI)
    Y_NDVI1=NDVI[0:NDVI_max_index]
    Y_NDVI2=NDVI[NDVI_max_index:]

    '''
    plt.figure()
    plt.plot(range(len(Y_NDVI1)),Y_NDVI1,'--')
    plt.plot(range(len(Y_NDVI2)),Y_NDVI2,'--')
    plt.show()
    '''

    x = np.arange(0,Num,1)
    
    Regress_parameter=Logistic_regress(x[0:NDVI_max_index],Y_NDVI1)
    '''
    plt.figure()
    plt.plot(range(366),peval(range(366),Regress_parameter))
    plt.show()
    '''

    regressLine = peval(range(Num),Regress_parameter)
    GUD,line,GUDnew = getMatrixGUD(regressLine)
    '''
    plt.figure()
    plt.plot(range(len(line)),line)
    plt.axvline(GUD,ls="--",color="r")
    plt.show()
    '''
    
    return(round(GUDnew))
    
    