# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import leastsq
from scipy.interpolate import spline
import timeseris
import random
import logsticFit


'''
line = timeseris.get_initial_line(a=11.105, b=-0.008, c=0.7, d=0.1, a_down=-24.3, b_down=0.009, STEP=3660)
for i, val in enumerate(line):
    if i % 80 == 0:
        print(int(i/10), ' ', val + (random.random() * 0.1 - 0.05))
'''


