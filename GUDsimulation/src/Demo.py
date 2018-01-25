import numpy as np
<<<<<<< HEAD
import matplotlib.pyplot as plt
import math

# Python实现正态分布
# 绘制正态分布概率密度函数


def normal(u=0, sig=1, sample_numbers=11):
    x = np.linspace(u - 3 * sig, u + 3 * sig, 50)
    y = np.exp(-(x - u) ** 2 / (2 * sig ** 2)) / (math.sqrt(2 * math.pi) * sig)
    sample_point = np.int8(np.linspace(0, 49, sample_numbers))
    gud = np.array(x[sample_point])
    fa = np.array(y[sample_point])

    plt.figure()
    plt.plot(x, y)
    plt.plot(gud, fa, 'ro')
    plt.grid()
    plt.show()

    gud = np.round(gud)
    fa = fa / fa.sum()
    return fa, gud


fa, gud = normal(u=110, sig=3)
print(fa)
print(gud)

=======
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
>>>>>>> b8fd0e455029d33020fcd49e87d12c3df85da4f0


