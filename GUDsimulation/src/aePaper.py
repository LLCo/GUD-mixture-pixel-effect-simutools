from Main import *
import batchCalculator
import timeseris
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1.colorbar import colorbar
import numpy as np


def firstPic():

    AlineP = batchCalculator.initialAParameterList
    BlineP = batchCalculator.initialBParameterList
    Aline = timeseris.get_initial_line(AlineP[0], AlineP[1], AlineP[2], AlineP[3], AlineP[4], AlineP[5], 3660)
    Bline = timeseris.get_initial_line(BlineP[0], BlineP[1], BlineP[2], BlineP[3], BlineP[4], BlineP[5], 3660)
    mixLine = (Aline + Bline)/2

    regress_line_up, regress_line_down, totalLine = logsticFit.curve_fit(mixLine)  # 获取到了拟合后的像素
    [GUDmix,derivative,derivative2,derivative3] = GUDcaculate(regress_line_up)
    thre = 0.09
    [GUDthre, threValue] = GUDThreCaculate(mixLine, thre)
    derivative3 = derivative3[0:1500] / (np.max(derivative3[0:1500])) / 1.2

    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.plot(Aline, color="#75bbfd")
    plt.plot(Bline, color="#ffb07c")
    plt.plot(mixLine, ls="--", lw=2, color="black")
    plt.ylim([0, 1])
    plt.xlim([0, 3660])
    plt.xticks(np.linspace(0, 3660, 5), ['', '', '', '', ''])

    plt.subplot(2, 2, 3)
    plt.plot(mixLine, ls="--", lw=2, color="black")
    plt.plot(totalLine, ls="-", lw=1, color="black")
    plt.plot(derivative3[0:1500], ls=":", lw=2, color="black")
    plt.ylim([0, 1])
    plt.xlim([0, 3660])
    plt.xticks(np.linspace(0, 3660, 5), ['', '', '', '', ''])

    plt.subplot(2, 2, 4)
    plt.plot(mixLine, ls="--", lw=2, color="black")
    plt.axhline((0.8-0.1)*0.09+0.1, ls=":", lw=2, color="black")
    plt.ylim([0, 1])
    plt.xlim([0, 3660])
    plt.xticks(np.linspace(0, 3660, 5), ['', '', '', '', ''])

    plt.subplot(2, 2, 2)
    plt.axhline(0.9, lw=2, color="#75bbfd")
    plt.axhline(0.8, lw=2, color="#ffb07c")
    plt.axhline(0.7, ls="--", lw=2, color="black")
    plt.axhline(0.6, ls="-", lw=1, color="black")
    plt.axhline(0.45, ls=":", lw=2, color="black")
    plt.axhline(0.35, ls=":", lw=2, color="black")
    plt.xticks([])
    plt.show()


def secondPic():
    """
    Draw picture about reason of advance effect
    Two picture:
    :return:
    """
    AlineP = batchCalculator.initialAParameterList
    BlineP = batchCalculator.initialBParameterList
    Aline = timeseris.get_initial_line(AlineP[0], AlineP[1], AlineP[2], AlineP[3], AlineP[4], AlineP[5], 3660)
    Bline = timeseris.get_initial_line(BlineP[0], BlineP[1], BlineP[2], BlineP[3], BlineP[4], BlineP[5], 3660)
    faList = np.linspace(0, 1, 50)
    thre = 0.09
    GUDs = np.zeros((50, 2))

    for i, fa in enumerate(faList):
        mixLine = fa*Aline + (1-fa)*Bline
        regress_line_up, regress_line_down, totalLine = logsticFit.curve_fit(mixLine)  # 获取到了拟合后的像素
        [GUDmix, derivative, derivative2, derivative3] = GUDcaculate(regress_line_up)
        [GUDthre, threValue] = GUDThreCaculate(mixLine, thre)
        GUDs[i, :] = [GUDmix/10, GUDthre/10]

    plt.figure(figsize=(12, 8))
    plt.subplot(2, 2, 1)
    plt.plot(GUDs[:, 0], lw=2, color="#214761")
    plt.plot([10, 36], [GUDs[10, 0], GUDs[36, 0]], ls=":", lw=2, color="#214761")
    label = ['0%', '20%', '40%', '60%', '80%', '100%']
    plt.xticks(np.int16(np.linspace(0, 50, 6)), label, rotation=45)

    plt.subplot(2, 2, 2)
    plt.plot(GUDs[:, 0], label="Curvature Method", color="#214761", zorder=1)
    plt.plot(GUDs[:, 1], label="Threshold Method", color="#9d0216", zorder=1)
    # plt.plot([0, 49], [140, 110], color="black", zorder=1)
    changeC = list(map(lambda x: (GUDs[-1, 0]-GUDs[0, 0])*(x/49) - GUDs[x, 0] + GUDs[0, 0], range(50)))
    changeT = list(map(lambda x: (GUDs[-1, 1]-GUDs[0, 1])*(x/49) - GUDs[x, 1] + GUDs[0, 1], range(50)))
    label = ['0%', '20%', '40%', '60%', '80%', '100%']
    plt.xticks(np.int16(np.linspace(0, 50, 6)), label, rotation=45)

    plt.subplot(2, 2, 3)
    plt.axhline(0.4, color="#214761")
    plt.axhline(0.3, color="#9d0216")
    plt.axhline(0.2, color="#214761")
    plt.axhline(0.1, ls=":", lw=2, color="#214761")
    plt.show()


    # ax2 = plt.gca().twinx()
    # ax2.plot(changeC, ls='--', color="#214761", zorder=0)
    # ax2.plot(changeT, ls='--', color="#9d0216", zorder=0)
    # plt.ylim((0, 30))
    plt.show()

if __name__ == "__main__":
    # firstPic()
    firstPic()
    print("end!")
