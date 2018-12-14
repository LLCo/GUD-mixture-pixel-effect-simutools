# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

from lib.curvature_gud import Phenology
from lib.curvature_gud import LogisticFitting

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
    return fit(NDVI, day)


def fit(NDVI, day):

    NDVI = np.array(NDVI)
    day = np.array(day)

    lf = LogisticFitting()

    lf.vi_time = day
    ps, relative_rmse, curves = lf.fitting(NDVI)
    fit_t, fit_curve = curves

    plt.figure(figsize=(4.5, 3))
    plt.plot(fit_t, fit_curve, 'r', lw=2, label='fit line')
    plt.plot(day, NDVI, 'b', lw=2, label='original line')
    plt.ylim([0, 1])
    plt.xlim([0, 365])
    plt.title('preview')
    plt.xlabel('Month of year')
    plt.ylabel('NDVI')
    plt.legend(loc='upper left')
    label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec','Jan']
    plt.xticks(np.int16(np.linspace(0, 365, 5)), [label[0], label[3], label[6], label[9], label[12]], rotation=45)
    plt.savefig('data/preview.png')

    p_u, p_d = ps
    p_as = [p_u[0], p_u[1], p_u[2], p_u[3], p_d[0], p_d[1]]
    return p_as


if __name__ == "__main__":
    readtxt()
