from Main import *
import batchCalculator
import timeseris
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1.colorbar import colorbar
import numpy as np
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"C:\\WINDOWS\\Fonts\\times.ttf", size=14)#C:\WINDOWS\Fonts


def __shade_color__(n, color=(1, 1, 1)):
    for i in range(n):
        yield((color[0], color[1]*(i/n), 1 -color[2]*(i/n)))
    return color


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


def thirdPic():
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

    plt.figure(figsize=(12, 8))
    plt.subplot(2, 2, 1)
    normalFa = normalFa/np.sum(normalFa)
    plt.plot(days, normalFa, '-.o', color="black")
    plt.xlabel("GUD", fontproperties=font)
    plt.ylabel("Frequency", fontproperties=font)

    plt.subplot(2, 2, 3)
    plt.plot()
    plt.plot(normalList[:, 12], label="Center NDVI Line", lw=2, color="black")
    plt.plot(normalMix, label="Mix NDVI Line (Dot)", lw=2, ls="--", color="black")
    label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec','Jan']
    plt.xticks(np.int16(np.linspace(0, 3660, 5)), [label[0], label[3], label[6], label[9], label[12]], rotation=45)
    plt.xlabel("Month", fontproperties=font)
    plt.ylabel("NDVI", fontproperties=font)

    plt.subplot(2, 2, 4)
    plt.plot(oslist, guds[:, 0]/10 - guds[0, 0]/10, label="Mix GUD by Curvature", lw=2, color="#214761")
    plt.plot(oslist, guds[:, 1]/10 - guds[0, 1]/10, label="Mix GUD by Threshold", lw=2, color="#9d0216")
    plt.axhline(0, label="Field GUD", ls=":", color="black")
    plt.xlabel("Variances", fontproperties=font)
    plt.ylabel("Bias", fontproperties=font)

    plt.subplot(2, 2, 2)

    plt.axhline(0.6, ls='-.', marker='o', color="black")
    plt.axhline(0.5, color="black")
    plt.axhline(0.4, ls="--", color="black")
    plt.axhline(0.2, lw=2, color="#214761")
    plt.axhline(0.1, lw=2, color="#9d0216")

    plt.show()


def forthPic():
    AlineP = batchCalculator.initialAParameterList
    BlineP = batchCalculator.initialBParameterList
    Bline = timeseris.get_initial_line(BlineP[0], BlineP[1], BlineP[2], BlineP[3], BlineP[4], BlineP[5], 3660)
    Aline = timeseris.get_initial_line(AlineP[0], AlineP[1], AlineP[2], AlineP[3], AlineP[4], AlineP[5], 3660)

    Blines = np.zeros((3660, 5))
    Alines = np.zeros((3660, 5))
    shiftDays = -np.linspace(10, 30, 5)
    shiftDaysUp = AlineP[0] + shiftDays * -AlineP[1] * 10
    shiftDaysDown = AlineP[4] + shiftDays * -AlineP[5] * 10
    for i in range(5):
        Alines[:, i] = timeseris.get_initial_line(shiftDaysUp[i], AlineP[1], AlineP[2], AlineP[3], shiftDaysDown[i],
                                                  AlineP[5], 3660)
    shiftDays = -np.linspace(-10, -30, 5)
    shiftDaysUp = AlineP[0] + shiftDays * -AlineP[1] * 10
    shiftDaysDown = AlineP[4] + shiftDays * -AlineP[5] * 10
    for i in range(5):
        Blines[:, i] = timeseris.get_initial_line(shiftDaysUp[i], AlineP[1], AlineP[2], AlineP[3], shiftDaysDown[i],
                                                  AlineP[5], 3660)

    pcolor = __shade_color__(5)
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 2, 1)

    for index, val in enumerate(__shade_color__(5)):
        plt.plot(Alines[:, index], label=str(index) + 'th A line', color=(1, 1*(index/5), 1*(1-index/5)), zorder=1)
        plt.plot(Blines[:, index], label=str(index) + 'th A line', color=(0, 1*(index/5), 1*(1-index/5)), zorder=2)
    plt.plot(Aline, label='B line', color="black")
    label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
    plt.xticks(np.int16(np.linspace(0, 3660, 5)), [label[0], label[3], label[6], label[9], label[12]], rotation=45)

    plt.subplot(2, 2, 3)
    for index, val in enumerate(__shade_color__(5)):
        plt.plot((Alines[:, index] + Aline)/2, label=str(index) + 'th mix line', color=(1, 1*(index/5), 1*(1-index/5)))
    label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
    plt.xticks(np.int16(np.linspace(0, 3660, 5)), [label[0], label[3], label[6], label[9], label[12]], rotation=45)
    rect = Rectangle((700, 0.1), 1000, 0.3, alpha=1, edgecolor="black", facecolor="white", zorder=-1, linestyle="--", lw=3)
    plt.gca().add_patch(rect)

    plt.subplot(2, 2, 4)
    for index, val in enumerate(__shade_color__(5)):
        plt.plot((Blines[:, index] + Aline)/2, label=str(index) + 'th mix line', color=(0, 1*(index/5), 1*(1-index/5)))
    label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
    plt.xticks(np.int16(np.linspace(0, 3660, 5)), [label[0], label[3], label[6], label[9], label[12]], rotation=45)
    rect = Rectangle((1000, 0.1), 1000, 0.3, alpha=1, edgecolor="black", facecolor="white", zorder=-1, linestyle="--", lw=3)
    plt.gca().add_patch(rect)
    plt.show()

    return


def fifthPic():
    AlineP = batchCalculator.initialAParameterList
    BlineP = batchCalculator.initialBParameterList
    Bline = timeseris.get_initial_line(BlineP[0], BlineP[1], BlineP[2], BlineP[3], BlineP[4], BlineP[5], 3660)
    Aline = timeseris.get_initial_line(AlineP[0], AlineP[1], AlineP[2], AlineP[3], AlineP[4], AlineP[5], 3660)
    N = 11
    Alines = np.zeros((3660, N))
    shiftDays = np.linspace(-20, 20, N)
    print(shiftDays)
    shiftDaysUp = AlineP[0] + shiftDays * -AlineP[1] * 10
    shiftDaysDown = AlineP[4] + shiftDays * -AlineP[5] * 10
    for i in range(N):
        Alines[:, i] = timeseris.get_initial_line(shiftDaysUp[i], AlineP[1], AlineP[2], AlineP[3], shiftDaysDown[i],
                                                  AlineP[5], 3660)
    thre = 0.09
    GUDs = np.zeros((11, 11, 2))
    for i, fa in enumerate(np.linspace(0, 1, 11)):
        for j in range(N):
            line = Alines[:, j]
            regress_line_up, regress_line_down, totalLine = logsticFit.curve_fit(line*fa + Aline*(1-fa))  # 获取到了拟合后的像素
            [GUDs[i, j, 0], derivative, derivative2, derivative3] = GUDcaculate(regress_line_up)
            [GUDs[i, j, 1], threValue] = GUDThreCaculate(line*fa + Aline*(1-fa), thre)
    print(GUDs[:, :, 0])
    GUDs = GUDs / 10

    plt.figure(figsize=(10, 8))
    plt.subplot(2, 2, 1)
    plt.plot(shiftDays + 110, lw=2, label='veg A', color='#75bbfd')
    plt.plot(np.zeros(11) + 110, lw=2, label='veg B', color='#ffb07c')
    plt.plot((shiftDays + np.zeros(11)) * 0.5 + 110, lw=2, ls='--', label='50%', color='black')
    plt.plot(GUDs[5, :, 0], ls='-', label='fa = 50%', marker='v', color='black')
    plt.ylabel("GUD", FontProperties=font)
    plt.xticks([0, 10], ['start', 'end'])
    plt.title("(a)", FontProperties=font)

    plt.subplot(2, 2, 3)
    plt.plot(GUDs[:, 0, 0], ls='-', marker='o', label="RS detection ( deltaGUD = -20)", color='black')
    plt.plot(GUDs[:, -1, 0], ls='-', marker='^', label="RS detection ( deltaGUD = 20)", color='black')
    plt.plot([0, 10], [GUDs[0, 0, 0], GUDs[-1, 0, 0]], ls='--', label="field detection ( deltaGUD = -20)", color='black')
    plt.plot([0, 10], [GUDs[0, -1, 0], GUDs[-1, -1, 0]], ls='--', label="field detection ( deltaGUD = 20)", color='black')
    plt.ylabel("GUD", FontProperties=font)
    plt.title("(b)", FontProperties=font)
    plt.xticks([0, 10], ['start', 'end'])

    GUDsField = np.zeros((11, 11))
    for i, fa in enumerate(np.linspace(0, 1, 11)):
        for j, shiftday in enumerate(shiftDays):
            GUDsField[i, j] = fa * (110 + shiftday) + (1-fa) * 110

    intervalChangeGUDs = (GUDs[:, 1:, 0] - GUDs[:, 0:-1, 0])-(GUDsField[:, 1:] - GUDsField[:, 0:-1])
    plt.subplot(2, 2, 2)
    ax2 = plt.gca()
    im2 = ax2.imshow(intervalChangeGUDs)
    cb2 = colorbar(im2, ax=ax2)
    # cb2.ax.set_yticks([-1.2, 0, 1.2], ['Increase', 'Invariant', 'Reduce'])
    plt.xticks([0, 9], ['start', 'end'])
    plt.ylabel("Fa", FontProperties=font)
    plt.title("(c)", FontProperties=font)
    plt.yticks(np.linspace(0, 10, 6), ['100%', '80%', '60%', '40%', '20%', '0%'], rotation=45)

    intervalChangeGUDs = np.abs((GUDs[1:, :, 0] - GUDs[0:-1, :, 0]))-np.abs((GUDsField[1:, :] - GUDsField[0:-1, :]))
    intervalChangeGUDs = -np.transpose(intervalChangeGUDs)
    plt.subplot(2, 2, 4)
    ax2 = plt.gca()
    im2 = ax2.imshow(intervalChangeGUDs)
    cb2 = colorbar(im2, ax=ax2)
    # cb2.ax.set_yticks([-1, 0, 1.2], ['Increase', 'Invariant', 'Reduce'])
    plt.ylabel("Interval", FontProperties=font)
    plt.title("(d)", FontProperties=font)
    plt.xticks([0, 9], ['start', 'end'])
    plt.yticks(np.linspace(0, 10, 6), np.linspace(20, -20, 6), rotation=45)
    plt.show()

    plt.axhline(0.9, lw=2, color="#75bbfd")
    plt.axhline(0.8, lw=2, color="#ffb07c")


if __name__ == "__main__":
    # firstPic()
    # secondPic()
    # thirdPic()
    # forthPic()
    fifthPic()
    print("end!")
