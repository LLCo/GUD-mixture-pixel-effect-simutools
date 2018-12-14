# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import leastsq

from lib import timeseris

'''

目前暂时是前端和后端单独拟合后使用其系数
没考虑前后两段组合拟合

'''


def logistic4New(x, A, B, C, D,A_down,B_down,MaxTime = 1800):
    """4PL lgoistic equation."""
    timeseris_up = logistic4(x, A, B, C, D)
    timeseris_down = logistic4(x, A_down,B_down, C, D)
    timeseris_merge = timeseris.merge_lines(timeseris_up, timeseris_down)
    
    return timeseris_merge


def residualsNew(p, y, x):
    """Deviations of data from fitted 4PL curve"""
    A,B,C,D,A_down,B_down = p
    err = y-logistic4New(x, A, B, C, D,A_down,B_down)
    return err


def Logistic_regressNew(x,y,p0):
    plsq = leastsq(residualsNew, p0, args=(y, x)) #maxfev = 1000
    return plsq[0]


def pevalNew(x, p):
    """Evaluated value at x with current parameters."""
    A, B, C, D,A_down,B_down = p
    return logistic4New(x, A, B, C, D,A_down,B_down)


def logistic4(x, A, B, C, D):
    """4PL lgoistic equation."""
    expValue = np.exp(A + B*x)
    timeseris = C/(1 + expValue) + D
    return timeseris


def residuals(p, y, x):
    """Deviations of data from fitted 4PL curve"""
    A,B,C,D = p
    err = y-logistic4(x, A, B, C, D)
    return err


def peval(x, p):
    """Evaluated value at x with current parameters."""
    A,B,C,D = p
    return logistic4(x, A, B, C, D)


def Logistic_regress(x,y,p0):
    plsq = leastsq(residuals, p0, args=(y, x)) #maxfev = 1000
    return plsq[0]


def curve_fit(NDVI, x=None, p0Up=None, p0Down=None):

    if p0Up is None:
        p0Up = [10, -0.007, 0.7, 0.1]

    if p0Down is None:
        p0Down = [-27,0.009,0.7,0.1]

    Num = len(NDVI)
    NDVI_max_index=np.argmax(NDVI)
    Y_NDVI1=NDVI[0:NDVI_max_index]
    Y_NDVI2=NDVI[NDVI_max_index:]

    if x is None:
        x = np.arange(0, Num, 1)
    
    regress_parameter_up = Logistic_regress(x[0:NDVI_max_index], Y_NDVI1, p0Up)
    regress_parameter_down = Logistic_regress(x[NDVI_max_index:], Y_NDVI2, p0Down)

    regress_line_up = peval(range(Num), regress_parameter_up)
    regress_line_down = peval(range(Num), np.array(regress_parameter_down))

    totalLine = timeseris.merge_lines(regress_line_up, regress_line_down)

    return [regress_line_up,regress_line_down,totalLine]