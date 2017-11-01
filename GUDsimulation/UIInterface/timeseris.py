# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

'''
本部分用于A，B初始时间序列的绘制，以及各种参数的位移
'''

initialAParameter = {'a': 10, 'b': -0.07, 'c': 0.7, 'd': 0.1, 'a_down': -27, 'b_down': 0.09}
initialBParameter = {'a': 12.1, 'b': -0.07, 'c': 0.7, 'd': 0.1, 'a_down': -29.7, 'b_down': 0.09}

def get_logistic_line(a, b, c, d, time=366):
    time = np.arange(0, time, 1)
    exp_value = np.exp(a + b * time)
    timeseris = c / (1 + exp_value) + d
    return timeseris


def merge_lines(timeSerisUp, timeSerisDown):
    length = len(timeSerisUp)
    temp = np.copy(timeSerisUp)
    flag = 0
    for i in range(length):
        if (timeSerisUp[i] >= timeSerisDown[i] or flag == 1):
            temp[i] = timeSerisDown[i]
            flag = 1
    return (temp)


def get_initial_line(a=10, b=-0.07, c=0.7, d=0.1, a_down=-27, b_down=0.09,STEP = 366):
    timeseris_up = get_logistic_line(a, b, c, d,time=STEP)
    timeseris_down = get_logistic_line(a_down, b_down, c, d,time=STEP)
    timeseris_merge = merge_lines(timeseris_up, timeseris_down)

    return timeseris_merge


def NDVImaxShift(a, b, c, d, a_down, b_down, shift=0):
    return [a, b, c - shift, d, a_down, b_down]


def NDVIminShift(a, b, c, d, a_down, b_down, shift=0):
    return [a, b, c - shift, d + shift, a_down, b_down]


def maturityPeriodShift(a, b, c, d, a_down, b_down, GUD=110, shift=0):  # shift range(-1 ,1)
    # range = -0.08 ~ ~0.06
    bNew = 0.02 * (shift + 1) / 2
    bNew = -0.08 + bNew
    a = a - GUD * (bNew - b)
    return ([a, bNew, c, d, a_down, b_down])


def timeSerisShift(a, b, c, d, a_down, b_down, shift=0):
    a_New = a - shift * b
    a_down_New = a_down - shift * b_down
    return ([a_New, b, c, d, a_down_New, b_down])


def getInitialAB():
    timeSerisA = get_initial_line()
    timeSerisB = get_initial_line(
        initialBParameter['a'], \
        initialBParameter['b'], \
        initialBParameter['c'], \
        initialBParameter['d'], \
        initialBParameter['a_down'], \
        initialBParameter['b_down'], )
    return ([timeSerisA, timeSerisB])


'''
test code
'''


def test():
    timeSerisA = get_initial_line()
    a, b, c, d, a_down, b_down = timeSerisShift( \
        initialAParameter['a'], \
        initialAParameter['b'], \
        initialAParameter['c'], \
        initialAParameter['d'], \
        initialAParameter['a_down'], \
        initialAParameter['b_down'],
        shift=30)

    print(a, b, c, d, a_down, b_down)
    timeSerisB = get_initial_line(
        initialBParameter['a'], \
        initialBParameter['b'], \
        initialBParameter['c'], \
        initialBParameter['d'], \
        initialBParameter['a_down'], \
        initialBParameter['b_down'], )

    a, b, c, d, a_down, b_down = NDVImaxShift( \
        initialAParameter['a'], \
        initialAParameter['b'], \
        initialAParameter['c'], \
        initialAParameter['d'], \
        initialAParameter['a_down'], \
        initialAParameter['b_down'],
        shift=0.2)
    lineMAXShift = get_initial_line(a, b, c, d, a_down, b_down)

    a, b, c, d, a_down, b_down = NDVIminShift( \
        initialAParameter['a'], \
        initialAParameter['b'], \
        initialAParameter['c'], \
        initialAParameter['d'], \
        initialAParameter['a_down'], \
        initialAParameter['b_down'],
        shift=0.2)
    lineMINShift = get_initial_line(a, b, c, d, a_down, b_down)

    a, b, c, d, a_down, b_down = maturityPeriodShift( \
        initialAParameter['a'], \
        initialAParameter['b'], \
        initialAParameter['c'], \
        initialAParameter['d'], \
        initialAParameter['a_down'], \
        initialAParameter['b_down'],
        shift=1)
    linePeriodShift = get_initial_line(a, b, c, d, a_down, b_down)

    plt.figure(figsize=(6, 3))
    plt.plot(range(366), lineMAXShift)
    plt.plot(range(366), lineMINShift)
    plt.plot(range(366), timeSerisB)
    plt.plot(range(366), timeSerisA, 'b--')
    plt.plot(range(366), linePeriodShift, 'r')
    plt.show()
    return


'''
serisA,serisB = getInitialAB()

a,b,c,d,a_down,b_down = timeSerisShift(\
                            initialAParameter['a'],\
                            initialAParameter['b'],\
                            initialAParameter['c'],\
                            initialAParameter['d'],\
                            initialAParameter['a_down'],\
                            initialAParameter['b_down'],
                            shift = -30)
timeSerisA = getInitialLine(a,b,c,d,a_down,b_down)
a,b,c,d,a_down,b_down = timeSerisShift(\
                            initialBParameter['a'],\
                            initialBParameter['b'],\
                            initialBParameter['c'],\
                            initialBParameter['d'],\
                            initialBParameter['a_down'],\
                            initialBParameter['b_down'],
                            shift = 30)


timeSerisB = getInitialLine(a,b,c,d,a_down,b_down)


plt.figure(figsize = (12,8))
plt.plot(range(366),timeSerisA,'--')
plt.plot(range(366),timeSerisB,'--')
plt.plot(range(366),serisA)
plt.plot(range(366),serisB)
plt.show()
'''