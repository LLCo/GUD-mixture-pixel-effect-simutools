# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

from lib import logsticFit

'''
line = timeseris.get_initial_line(a=11.105, b=-0.008, c=0.7, d=0.1, a_down=-24.3, b_down=0.009, STEP=3660)
for i, val in enumerate(line):
    if i % 80 == 0:
        print(int(i/10), ' ', val + (random.random() * 0.1 - 0.05))
'''


def readtxt(fname='./NDVI time seris test.txt'):
    day = []
    NDVI = []
    fobj = open(fname, 'r')
    for i, eachline in enumerate(fobj):
        words = eachline.split()
        day.append(int(words[0]))
        NDVI.append(float(words[1]))
        # print(day[i], ' ', NDVI[i])
    return fit(NDVI, day)


def fit(NDVI, day):

    p0Up = [11.105, -0.008, 0.7, 0.1]
    p0Down = [-24.3, 0.009, 0.7, 0.1]
    NDVI = np.array(NDVI)
    day = np.array(day) * 10
    NDVI_max_index=np.argmax(NDVI)
    Y_NDVI1=NDVI[0:NDVI_max_index]
    Y_NDVI2=NDVI[NDVI_max_index:]
    Num = len(NDVI)

    regress_line_up_test = logsticFit.peval(day[0:NDVI_max_index], p0Up)
    regress_line_down_test = logsticFit.peval(range(Num), np.array(p0Down))

    regress_parameter = logsticFit.Logistic_regressNew(day[0:NDVI_max_index], Y_NDVI1, [11.105, -0.008, 0.7, 0.1, -24.3, 0.009])
    regress_line = logsticFit.pevalNew(day, regress_parameter)
    # totalLine = timeseris.merge_lines(regress_line_up, regress_line_down)

    plt.figure(figsize=(4.5, 3))
    plt.plot(day, regress_line, 'r', lw=2, label='fit line')
    plt.plot(day, NDVI, 'b', lw=2, label='original line')
    plt.ylim([0, 1]);
    plt.xlim([0, 3660]);
    plt.title('preview')
    plt.xlabel('Month of year')
    plt.ylabel('NDVI')
    plt.legend(loc='upper left')
    label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec','Jan']
    plt.xticks(np.int16(np.linspace(0, 3660, 5)), [label[0], label[3], label[6], label[9], label[12]], rotation=45)
    plt.savefig('data/preview.png')
    return regress_parameter


if __name__ == "__main__":
    readtxt()
