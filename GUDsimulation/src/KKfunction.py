from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1.colorbar import colorbar
import numpy as np

font = FontProperties(fname=r"C:\\WINDOWS\\Fonts\\times.ttf", size=14)#C:\WINDOWS\Fonts


def get_logistic_line(a, b, c, d, time=3660):
    time = np.arange(1, time, 1)
    exp_value = np.exp(a + b * time)
    timeseris = c / (1 + exp_value) + d
    return timeseris


def Kfunction(a, b, c, d):
    t = np.linspace(1, 3660, 3660)
    z = np.exp(a+b*t)

    up = b**2*c*z*(1-z)*(1+z)**3
    down = ((1+z)**4 + (b*c*z)**2)**(3/2)
    return up/down


def KKfunction(a, b, c, d):
    t = np.linspace(1, 3660, 3660)
    z = np.exp(a+b*t)
    left = b**3*c*z
    leftin = 3*z*(1-z)*(1+z)**3*(2*(1+z)**3+b**2*c**2*z)/((1+z)**4+(b*c*z)**2)**(5/2)
    rightin = (1+2)**2*(1+2*z-5*z**2)/((1+z)**4+(b*c*z)**2)**(3/2)
    return left*(leftin-rightin)


def KKUpfunction():

    lines = KKfunction(10, -0.008, 0.7, 0.1)
    lines = lines[500:1200]
    return lines


lines = KKfunction(10, -0.008, 0.7, 0.1)
lines2 = KKfunction(11.6, -0.008, 0.7, 0.1)
plt.plot(lines[500:1150], color="#75bbfd", label="Veg A'D3")
plt.plot(lines2[500:1300], color="#ffb07c", label="Veg B'D3")
# maxPoint = np.where(lines == np.max(lines[0:1200]))
# plt.axvline(maxPoint[0]-500, ls='--', lw=1, color="#75bbfd")
# maxPoint = np.where(lines2 == np.max(lines2[0:1400]))
# plt.axvline(maxPoint[0]-500, ls='--', lw=1, color="#ffb07c")
linesMix = (lines + lines2)/2
plt.plot(linesMix[500:1150], ls='--', color="black", label="Mix'D3")
plt.legend(prop=font)
plt.xticks([])
plt.yticks([])
plt.xlabel("Time", FontProperties=font)
plt.ylabel("NDVI 3D", FontProperties=font)
plt.title("Proof of 'Advance Effect'", FontProperties=font)
plt.show()
