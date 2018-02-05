from Main import *
import batchCalculator
import timeseris
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1.colorbar import colorbar
import numpy as np
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"C:\\WINDOWS\\Fonts\\times.ttf", size=12)#C:\WINDOWS\Fonts


def secondFixPic():
    AlineP = batchCalculator.initialAParameterList
    BlineP = batchCalculator.initialBParameterList
    Bline = timeseris.get_initial_line(BlineP[0], BlineP[1], BlineP[2], BlineP[3], BlineP[4], BlineP[5], 3660)
    Aline = timeseris.get_initial_line(AlineP[0], AlineP[1], AlineP[2], AlineP[3], AlineP[4], AlineP[5], 3660)
    centerLine = timeseris.get_initial_line((AlineP[0]+BlineP[0])/2, (AlineP[1]+BlineP[1])/2,
                                            AlineP[2], AlineP[3], (AlineP[4]+BlineP[4])/2,
                                            (AlineP[5]+BlineP[5])/2, 3660)
    plt.figure(figsize=(8, 6))
    plt.plot(Aline, color="#75bbfd", label='A series')
    plt.plot(Bline, color="#ffb07c", label='B series')
    plt.plot((Aline+Bline)/2, ls="-", lw=2, color="black", label='Mix series')
    plt.plot(centerLine, ls='--', lw=2, color='black', label='Virtual series')
    plt.ylim([0, 1])
    plt.xlim([0, 3660])
    label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
    plt.xticks(np.int16(np.linspace(0, 3660, 5)), [label[0], label[3], label[6], label[9], label[12]], rotation=45,
               FontProperties=font)
    plt.xlabel('Month of the year', FontProperties=font)
    plt.ylabel('NDVI', FontProperties=font)
    plt.legend(prop=font, edgecolor=(1, 1, 1), loc=2)
    plt.show()


def thirdFixPic():
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

    N = 25
    u = 110
    o = 15
    days = np.linspace(u-3*o, u+3*o, N)
    normal = lambda u, o: np.exp(-(days-u)**2/(2*o**2))/np.sqrt(2*np.pi*o**2)
    normalFa = normal(u, o)
    normalFa = normalFa / np.sum(normalFa)

    AlineP = batchCalculator.initialAParameterList
    alist = AlineP[0] + np.linspace(-3 * o, 3 * o, N) * -AlineP[1] * 10
    a_downlist = AlineP[4] + np.linspace(-3 * o, 3 * o, N) * -AlineP[5] * 10

    print(a_downlist)
    print(alist)
    normalList = np.zeros((3660, N))
    for i, a in enumerate(alist):
        normalList[:, i] = timeseris.get_initial_line(a, AlineP[1], AlineP[2], AlineP[3], a_downlist[i], AlineP[5], 3660)
    normalMix = np.dot(normalFa, normalList.T)

    regress_line_up, regress_line_down, totalLine = logsticFit.curve_fit(normalMix)  # 获取到了拟合后的像素
    [GUDmix, derivative, derivative2, derivative3] = GUDcaculate(regress_line_up)
    # [GUDthre, threValue] = GUDThreCaculate(normalMix, thre)

    thre = 0.09
    guds = np.zeros((10, 2))
    oslist = np.linspace(0, 20, 10)

    for index, os in enumerate(oslist):
        days = np.linspace(u - 3 * os, u + 3 * os, N)
        if os == 0:
            normalFa = np.zeros(N) + 1/N
        else:
            normal = lambda u, o: np.exp(-(days - u) ** 2 / (2 * o ** 2)) / np.sqrt(2 * np.pi * o ** 2)
            normalFa = normal(u, os)
            normalFa = normalFa / np.sum(normalFa)
        alist = AlineP[0] + np.linspace(-3 * os, 3 * os, N) * -AlineP[1] * 10
        a_downlist = AlineP[4] + np.linspace(-3 * os, 3 * os, N) * -AlineP[5] * 10
        normalList = np.zeros((3660, N))
        for i, a in enumerate(alist):
            normalList[:, i] = timeseris.get_initial_line(a, AlineP[1], AlineP[2], AlineP[3], a_downlist[i], AlineP[5],
                                                          3660)
        normalMix = np.dot(normalFa, normalList.T)
        regress_line_up, regress_line_down, totalLine = logsticFit.curve_fit(normalMix)  # 获取到了拟合后的像素
        [guds[index, 0], derivative, derivative2, derivative3] = GUDcaculate(regress_line_up)
        [guds[index, 1], threValue] = GUDThreCaculate(normalMix, thre)

    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(GUDs[:, 0], label="Curvature Method", color="#75bbfd", zorder=1)
    plt.plot(GUDs[:, 1], label="Threshold Method", color="#ffb07c", zorder=1)
    plt.plot([0, 49], [140, 110], ls=':', color='black', zorder=0, label="Field GUD")
    # plt.plot([0, 49], [140, 110], color="black", zorder=1)
    label = ['0%', '20%', '40%', '60%', '80%', '100%']
    plt.xticks(np.int16(np.linspace(0, 50, 6)), label)
    plt.xlabel('Advantage plant percentage', FontProperties=font)
    plt.ylabel('GUD', FontProperties=font)
    plt.legend(prop=font, edgecolor=(1, 1, 1), loc=1)

    plt.subplot(1, 2, 2)
    plt.plot(oslist, guds[:, 0]/10 - guds[0, 0]/10, label="Curvature Method", lw=2, color="#75bbfd")
    plt.plot(oslist, guds[:, 1]/10 - guds[0, 1]/10, label="Threshold Method", lw=2, color="#ffb07c")
    plt.axhline(0, label="Field GUD", ls=":", color="black")
    plt.xlabel("Variances", fontproperties=font)
    plt.ylabel("Bias", fontproperties=font)
    # plt.legend(prop=font, edgecolor=(1, 1, 1), loc=3)

    plt.show()


def forthFixPic():
    """
    i: fa change, advantage: 0% -> 100%
    j: interval change, 0 -> 30 days
    dGUD(fa, interval)/ dfa
    dGUD(fa, interval)/ dinterval
    :return:
    """
    AlineP = batchCalculator.initialBParameterList
    N = 11
    Alines = np.zeros((3660, N))
    shiftDays = np.linspace(-30, 0, N)
    shiftDays = shiftDays[::-1]
    print(shiftDays)
    shiftDaysUp = AlineP[0] + shiftDays * -AlineP[1] * 10
    shiftDaysDown = AlineP[4] + shiftDays * -AlineP[5] * 10
    for i in range(N):
        Alines[:, i] = timeseris.get_initial_line(shiftDaysUp[i], AlineP[1], AlineP[2], AlineP[3], shiftDaysDown[i],
                                                  AlineP[5], 3660)
    """
    Alines[:, 0] is the earliest plant!
    """
    # plt.figure()
    # plt.plot(Alines[:, 0], color='black')
    # plt.plot(Alines[:, -1])
    # plt.show()
    Aline = Alines[:, 0]
    thre = 0.09
    GUDs = np.zeros((N, N, 2))
    GUDsTemp = np.zeros((N, N, 2))
    for i, fa in enumerate(np.linspace(0, 1, N)):
        for j in range(N):
            line = Alines[:, j]
            regress_line_up, regress_line_down, totalLine = logsticFit.curve_fit(line*fa + Aline*(1-fa))  # 获取到了拟合后的像素
            [GUDs[i, j, 0], derivative, derivative2, derivative3] = GUDcaculate(regress_line_up)
            [GUDs[i, j, 1], threValue] = GUDThreCaculate(line*fa + Aline*(1-fa), thre)

    GUDs = GUDs / 10
    for i in range(N):
        GUDsTemp[i, :, :] = GUDs[N-i-1, :, :]
    GUDs = GUDsTemp

    plt.figure(figsize=(10, 10))

    GUDsField = np.zeros((N, N))
    for i, fa in enumerate(np.linspace(0, 1, N)):
        for j, shiftday in enumerate(shiftDays):
            GUDsField[i, j] = (1-fa) * (140 + shiftday) + fa * 140

    print(GUDs[:, :, 0])
    print(GUDsField)
    GUDsDFa = GUDs[0:-1, :, 0] - GUDs[1:, :, 0]
    GUDsDFaMinus = GUDsDFa - (GUDsField[0:-1, :] - GUDsField[1:, :])

    GUDsDinterval = GUDs[:, 1:, 0] - GUDs[:, 0:-1, 0]
    GUDsDintervalMinus = GUDsDinterval - (GUDsField[:, 1:] - GUDsField[:, 0:-1])

    plt.subplot(2, 2, 1)
    ax2 = plt.gca()
    im2 = ax2.imshow(GUDsDFa)
    plt.title("(a)", FontProperties=font)
    plt.ylabel('fa', FontProperties=font)
    plt.yticks(np.linspace(0, 9, 2), ['100%', '0%'], rotation=45)
    plt.xticks([], [], rotation=45)

    plt.subplot(2, 2, 2)
    ax2 = plt.gca()
    im2 = ax2.imshow(GUDsDinterval)
    plt.title("(b)", FontProperties=font)
    cb2 = colorbar(im2, ax=ax2)
    plt.yticks([], [], rotation=45)
    plt.xticks([], [], rotation=45)

    plt.subplot(2, 2, 3)
    ax2 = plt.gca()
    im2 = ax2.imshow(-GUDsDFaMinus)
    plt.title("(c)", FontProperties=font)
    plt.ylabel('fa', FontProperties=font)
    cb2 = colorbar(im2, ax=ax2)
    plt.xlabel('Interval', FontProperties=font)
    plt.yticks(np.linspace(0, 9, 2), ['100%', '0%'], rotation=45)
    plt.xticks(np.linspace(0, 10, 2), ['0 day', '30 day'], rotation=45)

    plt.subplot(2, 2, 4)
    ax2 = plt.gca()
    im2 = ax2.imshow(-GUDsDintervalMinus)
    plt.title("(d)", FontProperties=font)
    cb2 = colorbar(im2, ax=ax2)
    plt.xlabel('interval', FontProperties=font)
    plt.yticks([], [], rotation=45)
    plt.xticks(np.linspace(0, 9, 2), ['0 day', '30 day'], rotation=45)

    # cb2.ax.set_yticks([-1, 0, 1.2], ['Increase', 'Invariant', 'Reduce'])
    # plt.ylabel("Interval", FontProperties=font)
    # plt.title("(d)", FontProperties=font)
    # plt.xticks([0, 9], ['start', 'end'])
    # plt.yticks(np.linspace(0, 10, 6), np.linspace(20, -20, 6), rotation=45)
    plt.show()

    plt.axhline(0.9, lw=2, color="#75bbfd")
    plt.axhline(0.8, lw=2, color="#ffb07c")


def forthFixPicConcise():
    AlineP = batchCalculator.initialAParameterList
    BlineP = batchCalculator.initialBParameterList
    Bline = timeseris.get_initial_line(BlineP[0], BlineP[1], BlineP[2], BlineP[3], BlineP[4], BlineP[5], 3660)
    Aline = timeseris.get_initial_line(AlineP[0], AlineP[1], AlineP[2], AlineP[3], AlineP[4], AlineP[5], 3660)


if __name__ == "__main__":
    # firstPic()
    # secondPic()
    # thirdPic()
    # forthPic()
    # thirdFixPic()
    forthFixPic()
    print("end!")
