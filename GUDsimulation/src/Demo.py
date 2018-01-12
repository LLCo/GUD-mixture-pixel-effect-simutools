import numpy as np
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



