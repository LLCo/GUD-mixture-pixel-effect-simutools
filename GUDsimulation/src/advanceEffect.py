from Main import *
import batchCalculator
import timeseris
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1.colorbar import colorbar
import numpy as np


def __shade_color__(n, color=(1, 1, 1)):
    for i in range(n):
        yield((color[0], color[1]*(i/n), 1 -color[2]*(i/n)))
    return color


def mixPattern():
    """
    Draw picture the description of this experiment
    :show: a picture
    :return: No
    """

    AlineP = batchCalculator.initialAParameterList
    BlineP = batchCalculator.initialBParameterList
    Aline = timeseris.get_initial_line(AlineP[0], AlineP[1], AlineP[2], AlineP[3], AlineP[4], AlineP[5], 3660)
    Bline = timeseris.get_initial_line(BlineP[0], BlineP[1], BlineP[2], BlineP[3], BlineP[4], BlineP[5], 3660)
    plt.figure(figsize=(8, 6))
    plt.plot(Aline, label="NDVI(A)")
    plt.plot(Bline, label="NDVI(B)")
    plt.plot((Aline + Bline)/2, label="NDVI·mix(A,B,50%)", ls="--", lw=3)
    plt.ylim([0, 1]);
    plt.xlim([0, 3660]);
    plt.title('Generate of the NDVI·mix(A,B,50%)')
    plt.xlabel('Month of year')
    plt.ylabel('NDVI')
    plt.legend(loc='upper left')
    label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec','Jan']
    plt.xticks(np.int16(np.linspace(0, 3660, 5)), [label[0], label[3], label[6], label[9], label[12]], rotation=45)
    plt.show()


def GUDderive():
    """
    Show How Get GUD by threshold and curvature method
    :return:
    """
    AlineP = batchCalculator.initialAParameterList
    BlineP = batchCalculator.initialBParameterList
    Aline = timeseris.get_initial_line(AlineP[0], AlineP[1], AlineP[2], AlineP[3], AlineP[4], AlineP[5], 3660)
    Bline = timeseris.get_initial_line(BlineP[0], BlineP[1], BlineP[2], BlineP[3], BlineP[4], BlineP[5], 3660)
    mixLine = (Aline + Bline)/2

    regress_line_up, regress_line_down, totalLine = logsticFit.curve_fit(mixLine)  # 获取到了拟合后的像素
    [GUDmix,derivative,derivative2,derivative3] = GUDcaculate(regress_line_up)
    thre = 0.09
    [GUDthre, threValue] = GUDThreCaculate(mixLine, thre)

    plt.figure(figsize=(10, 6))
    plt.plot(mixLine, label="NDVI·mix(A,B,50%)", ls="-", lw=4, color="cyan")
    plt.plot(totalLine, label="Fit(NDVI·mix(A,B,50%))", ls="--", lw=2, color="red")
    plt.ylim([0, 1])
    plt.xlim([0, 3660])
    plt.title('Generate of the NDVI·mix(A,B,50%)')
    plt.xlabel('Month of year')
    plt.ylabel('NDVI')
    plt.legend(loc='upper left')
    label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec','Jan']
    plt.xticks(np.int16(np.linspace(0, 3660, 5)), [label[0], label[3], label[6], label[9], label[12]], rotation=45)
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(regress_line_up, label="Fit_Up(NDVI·mix(A,B,50%))", lw=4, color="green")
    plt.axvline(GUDmix, ls='--', lw=3, label="GUD detected by curvature", color="blue")
    plt.ylim([0, 1])
    plt.xlim([0, 3660])
    plt.title('GUD detected of the NDVI·mix(A,B,50%)')
    plt.xlabel('Month of year')
    plt.ylabel('NDVI')
    plt.xticks(np.int16(np.linspace(0, 3660, 5)), [label[0], label[3], label[6], label[9], label[12]], rotation=45)
    plt.legend(loc='upper left')
    ax2 = plt.gca().twinx()  # this is the important function
    ax2.plot(derivative/(max(abs(derivative))), label="First D", color="red")
    ax2.plot(derivative2/(max(abs(derivative2))), label="Second D", color="cyan")
    ax2.plot(derivative3/(max(abs(derivative3))), label="Third D", color="blue")
    plt.legend(loc='lower right')
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.title('GUD calculate by threshold')
    plt.xlabel('Day of year')
    plt.ylabel('NDVI')
    plt.plot(mixLine, 'r-', lw=4, color="green")
    plt.ylim([0, 1])
    plt.xlim([0, 3660])
    plt.axvline(GUDthre, ls='--', color="blue", lw=3, label="GUD detected by threshold")  # label='GUD: ' + str(int(GUDthre/10)) + ' day')
    plt.axhline(threValue, ls='--', color='b', label='%' + str(thre * 100) + ' NDVI')
    plt.xticks(np.int16(np.linspace(0, 3659, 5)), [label[0], label[3], label[6], label[9], label[12]], rotation=45)
    plt.legend(loc='upper left')

    # ax2 = plt.gca().twinx()  # 使坐标轴与上图对应
    # ax2.plot([1, 1], color="white")
    plt.show()


def advancentroduction():
    mixPattern()
    GUDderive()
    return


def advanceReason():
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

    plt.figure(figsize=(8, 6))
    plt.plot(GUDs[:, 0], label="Curvature Method", color="blue")
    # plt.plot(GUDs[:, 1], label="Threshold Method", color="red")
    # plt.title("Fit_Up(NDVI·mix(A,B,fa)) change with fa in Curvature & Threshold")
    # plt.scatter(10, GUDs[10, 1], marker='^', lw=2, color="red")
    # plt.scatter(35, GUDs[35, 1], marker='v', lw=2, color="red")
    plt.plot([10, 36], [GUDs[10, 0], GUDs[36, 0]], ls="--", lw=3)
    plt.plot([23, 23], [GUDs[23, 0], (GUDs[10, 0]+GUDs[36, 0])/2], ls="--")
    plt.scatter(10, GUDs[10, 0], marker='^', lw=2, color="blue")
    plt.scatter(36, GUDs[36, 0], marker='v', lw=2, color="blue")
    plt.scatter([23, 23], [GUDs[23, 0], (GUDs[10, 0]+GUDs[36, 0])/2])
    plt.xlabel("Fa")
    plt.ylabel("GUD")
    plt.title("Advance effect (Curvature Method)")
    plt.legend()
    label = ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%']
    plt.xticks(np.int16(np.linspace(0, 50, 10)), label, rotation=45)
    plt.show()

    plt.figure(figsize=(8, 6))
    plt.plot(GUDs[:, 0], label="Curvature Method", color="blue")
    plt.plot(GUDs[:, 1], label="Threshold Method", color="red")
    changeC = list(map(lambda x: (GUDs[-1, 0]-GUDs[0, 0])*(x/49) - GUDs[x, 0] + GUDs[0, 0], range(50)))
    changeT = list(map(lambda x: (GUDs[-1, 1]-GUDs[0, 1])*(x/49) - GUDs[x, 1] + GUDs[0, 1], range(50)))
    plt.title("Fit_Up(NDVI·mix(A,B,fa)) change with fa in Curvature & Threshold")
    plt.xlabel("Fa")
    plt.ylabel("GUD")
    plt.legend()
    label = ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%']
    plt.xticks(np.int16(np.linspace(0, 50, 10)), label, rotation=45)

    ax2 = plt.gca().twinx()
    ax2.fill(changeC, label="Curvature Method Minus", color=(0.1, 0.2, 0.5, 0.3))
    ax2.fill(changeT, label="Threshold Method Minus", color=(0.5, 0.2, 0.1, 0.3))
    plt.ylim((0, 30))
    plt.legend(loc="upper left")
    plt.show()

    return


def advanceDetection():
    """
    该函数用于绘制第二部分实验的图片，包含正态分布的选取位置，以及偏离程度随正态分布的方差的变化情况。
    是一种有偏估计
    :return:
    """
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

    # normalMix = np.zeros(3660)
    # for i in range(N):
    #     normalMix += normalFa[i]*normalList[:, i]
    normalMix = np.dot(normalFa, normalList.T)

    plt.figure()
    plt.plot()
    plt.plot(normalList[:, 12], label="Center NDVI Line", lw=3)
    plt.plot(normalMix, label="Mix NDVI Line (Dot)", lw=3)
    plt.xlabel("Month of year")
    plt.ylabel("NDVI")
    plt.title("Center NDVI Line & Mix NDVI Line")
    plt.legend()
    label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec','Jan']
    plt.xticks(np.int16(np.linspace(0, 3660, 5)), [label[0], label[3], label[6], label[9], label[12]], rotation=45)
    plt.show()

    regress_line_up, regress_line_down, totalLine = logsticFit.curve_fit(normalMix)  # 获取到了拟合后的像素
    [GUDmix, derivative, derivative2, derivative3] = GUDcaculate(regress_line_up)
    # [GUDthre, threValue] = GUDThreCaculate(normalMix, thre)

    plt.figure()
    normalFa = normalFa/np.sum(normalFa)
    plt.plot(days, normalFa, 'ro')
    plt.plot(days, normalFa)
    plt.axvline(u, lw=2, ls="--")
    plt.axvline(GUDmix/10, lw=3, ls="--")
    plt.xlabel("Day of year")
    plt.ylabel("Frequent")
    plt.title("GUD of Mix NDVI Line")
    plt.show()

    return


def advanceDetection_much():

    N = 25
    u = 110
    AlineP = batchCalculator.initialAParameterList

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

    plt.figure()
    plt.plot(oslist, guds[:, 0]/10, label="Mix GUD by Curvature", lw=3)
    plt.plot(oslist, guds[:, 1]/10, label="Mix GUD by Threshold", lw=3)
    plt.axhline(u, label="Field GUD", ls="--")
    plt.xlabel("Variance")
    plt.ylabel("GUD")
    plt.title("Green Up Data Change With Variance")
    plt.legend()
    plt.show()


def advanceChangeDetection_reason():

    AlineP = batchCalculator.initialAParameterList
    BlineP = batchCalculator.initialBParameterList
    Bline = timeseris.get_initial_line(BlineP[0], BlineP[1], BlineP[2], BlineP[3], BlineP[4], BlineP[5], 3660)
    Aline = timeseris.get_initial_line(AlineP[0], AlineP[1], AlineP[2], AlineP[3], AlineP[4], AlineP[5], 3660)

    Blines = np.zeros((3660, 5))
    Alines = np.zeros((3660, 5))
    shiftDays = -np.linspace(0, 20, 5)
    shiftDaysUp = AlineP[0] + shiftDays * -AlineP[1] * 10
    shiftDaysDown = AlineP[4] + shiftDays * -AlineP[5] * 10
    for i in range(5):
        Alines[:, i] = timeseris.get_initial_line(shiftDaysUp[i], AlineP[1], AlineP[2], AlineP[3], shiftDaysDown[i],
                                                  AlineP[5], 3660)
    shiftDays = np.linspace(0, 20, 5)
    shiftDaysUp = BlineP[0] + shiftDays * -BlineP[1] * 10
    shiftDaysDown = BlineP[4] + shiftDays * -BlineP[5] * 10
    for i in range(5):
        Blines[:, i] = timeseris.get_initial_line(shiftDaysUp[i], BlineP[1], BlineP[2], BlineP[3], shiftDaysDown[i],
                                                  BlineP[5], 3660)

    pcolor = __shade_color__(5)
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 2, 1)

    for index, val in enumerate(__shade_color__(5)):
        plt.plot(Alines[:, index], label=str(index) + 'th A line', color=val)
    plt.plot(Bline, label='B line')
    plt.ylabel('mix GUD')
    plt.title('A line(delta GUD) & B line')
    label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
    plt.xticks(np.int16(np.linspace(0, 3660, 5)), [label[0], label[3], label[6], label[9], label[12]], rotation=45)
    plt.legend(loc='best')

    plt.subplot(2, 2, 2)
    for index, val in enumerate(__shade_color__(5)):
        plt.plot((Alines[:, index] + Bline)/2, label=str(index) + 'th mix line', color=val)
    plt.ylabel('NDVI')
    plt.title('mix line change with delta GUD')
    label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
    plt.xticks(np.int16(np.linspace(0, 3660, 5)), [label[0], label[3], label[6], label[9], label[12]], rotation=45)
    rect = Rectangle((700, 0.1), 1000, 0.3, alpha=1, edgecolor="r", facecolor="white", zorder=-1, linestyle="--", lw=4)
    plt.gca().add_patch(rect)
    plt.legend(loc='best')

    plt.subplot(2, 2, 3)
    for index, val in enumerate(__shade_color__(5)):
        plt.plot(Blines[:, index], label=str(index) + 'th A line', color=val)
    plt.plot(Aline, label='A line')
    plt.xlabel('Month of year')
    plt.ylabel('mix GUD')
    plt.title('A line & B line(delta GUD)')
    label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
    plt.xticks(np.int16(np.linspace(0, 3660, 5)), [label[0], label[3], label[6], label[9], label[12]], rotation=45)
    plt.legend(loc='best')

    plt.subplot(2, 2, 4)
    for index, val in enumerate(__shade_color__(5)):
        plt.plot((Blines[:, index] + Bline)/2, label=str(index) + 'th mix line', color=val)
    plt.xlabel('Month of year')
    plt.ylabel('NDVI')
    plt.title('mix line change with delta GUD')
    label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
    plt.xticks(np.int16(np.linspace(0, 3660, 5)), [label[0], label[3], label[6], label[9], label[12]], rotation=45)
    plt.legend(loc='best')
    rect = Rectangle((1000, 0.1), 1000, 0.3, alpha=1, edgecolor="r", facecolor="white", zorder=-1, linestyle="--", lw=4)
    plt.gca().add_patch(rect)
    plt.show()

    return


def advanceChangeDetection_show():
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
    plt.figure(1)
    plt.plot(Alines, color='r', label='change line')
    plt.plot(Aline, color='b', lw=4, ls='--', label='change line')
    plt.xlabel("Month of years")
    plt.ylabel("NDVI")
    label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
    plt.xticks(np.int16(np.linspace(0, 3660, 5)), [label[0], label[3], label[6], label[9], label[12]], rotation=45)
    plt.title("GUD Change Detection")
    plt.show()
    thre = 0.09
    GUDs = np.zeros((10, 11, 2))
    for i, fa in enumerate(np.linspace(0, 1, 10)):
        for j in range(N):
            line = Alines[:, j]
            regress_line_up, regress_line_down, totalLine = logsticFit.curve_fit(line*fa + Aline*(1-fa))  # 获取到了拟合后的像素
            [GUDs[i, j, 0], derivative, derivative2, derivative3] = GUDcaculate(regress_line_up)
            [GUDs[i, j, 1], threValue] = GUDThreCaculate(line*fa + Aline*(1-fa), thre)
    print(GUDs[:, :, 0])
    GUDs = (GUDs[:, 1:, :] - GUDs[:, 0:-1, :]) / 40

    plt.figure(figsize=(10, 8))
    ax1 = plt.gca()
    im2 = ax1.imshow(GUDs[:, :, 1])
    cb1 = colorbar(im2, ax=ax1)
    cb1.ax.set_yticks([0, 0.25, 0.5, 0.75, 0.1], ['0%', '25%', '50%', '75%', '100%'])
    ax1.set_title("mix GUDs can show how much change of Veg A (Curvature)", size=10)
    plt.ylabel("fa")
    plt.xlabel("interval")
    plt.xticks(np.linspace(0, 9, 6), np.linspace(-20, 20, 6), rotation=45)
    plt.yticks(np.linspace(0, 9, 6), ['0%', '20%', '40%', '60%', '80%', '100%'], rotation=45)
    plt.show()

    plt.figure(figsize=(10, 8))
    ax2 = plt.gca()
    im2 = ax2.imshow(GUDs[:, :, 1])
    cb2 = colorbar(im2, ax=ax2)
    cb2.ax.set_yticks([0, 0.25, 0.5, 0.75, 0.1], ['0%', '25%', '50%', '75%', '100%'])
    ax2.set_title("mix GUDs can show how much change of Veg A (Threshold)", size=10)
    plt.ylabel("fa")
    plt.xlabel("interval")
    plt.xticks(np.linspace(0, 9, 6), np.linspace(-20, 20, 6), rotation=45)
    plt.yticks(np.linspace(0, 9, 6), ['0%', '20%', '40%', '60%', '80%', '100%'], rotation=45)
    plt.show()


def advanceChangeDetection_show_fix():
    AlineP = batchCalculator.initialAParameterList
    BlineP = batchCalculator.initialBParameterList
    Bline = timeseris.get_initial_line(BlineP[0], BlineP[1], BlineP[2], BlineP[3], BlineP[4], BlineP[5], 3660)
    Aline = timeseris.get_initial_line(AlineP[0], AlineP[1], AlineP[2], AlineP[3], AlineP[4], AlineP[5], 3660)
    N = 11
    Alines = np.zeros((3660, N))
    shiftDays = np.linspace(-20, 20, N)
    shiftDaysUp = AlineP[0] + shiftDays * -AlineP[1] * 10
    shiftDaysDown = AlineP[4] + shiftDays * -AlineP[5] * 10
    for i in range(N):
        Alines[:, i] = timeseris.get_initial_line(shiftDaysUp[i], AlineP[1], AlineP[2], AlineP[3], shiftDaysDown[i],
                                                  AlineP[5], 3660)
    plt.figure(1)
    plt.plot(Alines, color='r', label='change line')
    plt.plot(Aline, color='b', lw=4, ls='--', label='change line')
    plt.xlabel("Month of years")
    plt.ylabel("NDVI")
    label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
    plt.xticks(np.int16(np.linspace(0, 3660, 5)), [label[0], label[3], label[6], label[9], label[12]], rotation=45)
    plt.title("GUD Change Detection")
    plt.show()
    thre = 0.09
    GUDs = np.zeros((11, 11, 2))
    for i, fa in enumerate(np.linspace(0, 1, 11)):
        for j in range(N):
            line = Alines[:, j]
            fb = 1 - fa
            regress_line_up, regress_line_down, totalLine = logsticFit.curve_fit(line*fb + Aline*(1-fb))  # 获取到了拟合后的像素
            [GUDs[i, j, 0], derivative, derivative2, derivative3] = GUDcaculate(regress_line_up)
            [GUDs[i, j, 1], threValue] = GUDThreCaculate(line*fb + Aline*(1-fb), thre)
    print(GUDs[:, :, 0])
    GUDs = (GUDs[:, 1:, :] - GUDs[:, 0:-1, :]) / 40

    plt.figure(figsize=(10, 8))
    ax1 = plt.gca()
    im2 = ax1.imshow(GUDs[:, :, 0])
    cb1 = colorbar(im2, ax=ax1)
    cb1.ax.set_yticks([0, 0.25, 0.5, 0.75, 1], ['0%', '25%', '50%', '75%', '100%'])
    ax1.set_title("mix GUDs can show how much change of Veg A (Curvature)", size=10)
    plt.ylabel("fa")
    plt.xlabel("interval")
    plt.xticks(np.linspace(0, 9, 6), np.linspace(-20, 20, 6), rotation=45)
    plt.yticks(np.linspace(0, 10, 6), ['100%', '80%', '60%', '40%', '20%', '0%'], rotation=45)
    plt.show()

    plt.figure(figsize=(10, 8))
    ax2 = plt.gca()
    im2 = ax2.imshow(GUDs[:, :, 1])
    cb2 = colorbar(im2, ax=ax2)
    cb2.ax.set_yticks([0, 0.25, 0.5, 0.75, 1], ['0%', '25%', '50%', '75%', '100%'])
    ax2.set_title("mix GUDs can show how much change of Veg A (Threshold)", size=10)
    plt.ylabel("fa")
    plt.xlabel("interval")
    plt.xticks(np.linspace(0, 9, 6), np.linspace(-20, 20, 6), rotation=45)
    plt.yticks(np.linspace(0, 10, 6), ['100%', '80%', '60%', '40%', '20%', '0%'], rotation=45)
    plt.show()


def advanceChangeDetection_line_show():

    AlineP = batchCalculator.initialAParameterList
    Aline = timeseris.get_initial_line(AlineP[0], AlineP[1], AlineP[2], AlineP[3], AlineP[4], AlineP[5], 3660)
    N = 11
    Alines = np.zeros((3660, N))
    shiftDays = np.linspace(-30, 30, N)
    shiftDaysUp = AlineP[0] + shiftDays * -AlineP[1] * 10
    shiftDaysDown = AlineP[4] + shiftDays * -AlineP[5] * 10
    for i in range(N):
        Alines[:, i] = timeseris.get_initial_line(shiftDaysUp[i], AlineP[1], AlineP[2], AlineP[3], shiftDaysDown[i],
                                                  AlineP[5], 3660)

    thre = 0.09
    GUDs = np.zeros((3, N, 2))
    for i, fa in enumerate([0.25, 0.5, 0.75]):
        for j in range(N):
            line = Alines[:, j]
            regress_line_up, regress_line_down, totalLine = logsticFit.curve_fit(line*fa + Aline*(1-fa))  # 获取到了拟合后的像素
            [GUDs[i, j, 0], derivative, derivative2, derivative3] = GUDcaculate(regress_line_up)
            [GUDs[i, j, 1], threValue] = GUDThreCaculate(line*fa + Aline*(1-fa), thre)
    print(GUDs[:, :, 0])
    GUDs = GUDs / 10

    # plt.figure()
    # plt.plot(shiftDays + 110, lw=4, label='veg A')
    # plt.plot(np.zeros(11) + 110, lw=4, label='veg B')
    # plt.plot((shiftDays + np.zeros(11))*0.25 + 110, lw=2, label='25%', color='r')
    # plt.plot(GUDs[0, :, 0], ls='--', label='fa = 25%', marker='o', color='r')
    # plt.plot((shiftDays + np.zeros(11)) * 0.5 + 110, lw=2, label='50%', color='g')
    # plt.plot(GUDs[1, :, 0], ls='--', label='fa = 50%', marker='^', color='g')
    # plt.plot((shiftDays + np.zeros(11)) * 0.75 + 110, lw=2, label='75%', color='b')
    # plt.plot(GUDs[2, :, 0], ls='--', label='fa = 75%', marker='v', color='b')
    # plt.xlabel("Time")
    # plt.ylabel("GUD")
    # plt.title("GUD change with Time (curvature)")
    # plt.xticks([0, 10], ['start', 'end'])
    # plt.legend()
    # plt.show()
    #
    # plt.figure()
    # plt.plot(shiftDays + 110, lw=4, label='veg A')
    # plt.plot(np.zeros(11) + 110, lw=4, label='veg B')
    # plt.plot(GUDs[0, :, 1], ls='--', label='fa = 25%', marker='o')
    # plt.plot(GUDs[1, :, 1], ls='--', label='fa = 50%', marker='^')
    # plt.plot(GUDs[2, :, 1], ls='--', label='fa = 75%', marker='v')
    # plt.xlabel("Time")
    # plt.ylabel("GUD")
    # plt.title("GUD change with Time (threshold)")
    # plt.xticks([0, 10], ['start', 'end'])
    # plt.legend()
    # plt.show()

    plt.figure()
    plt.plot(shiftDays + 110, lw=4, label='veg A')
    plt.plot(np.zeros(11) + 110, lw=4, label='veg B')
    plt.plot((shiftDays + np.zeros(11)) * 0.5 + 110, lw=2, label='50%', color='g')
    plt.plot(GUDs[1, :, 0], ls='--', label='fa = 50%', marker='^', color='g')
    plt.xlabel("Time")
    plt.ylabel("GUD")
    plt.title("GUD change with Time (curvature)")
    plt.xticks([0, 10], ['start', 'end'])
    plt.legend()
    plt.show()


def advanceChangeDetection_faline_show():
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

    plt.figure()
    plt.plot(GUDs[:, 0, 0], ls='--', marker='o', label="RS detection ( deltaGUD = -20)")
    plt.plot(GUDs[:, -1, 0], ls='--', marker='^', label="RS detection ( deltaGUD = 20)")
    plt.plot([0, 10], [GUDs[0, 0, 0], GUDs[-1, 0, 0]], label="field detection ( deltaGUD = -20)")
    plt.plot([0, 10], [GUDs[0, -1, 0], GUDs[-1, -1, 0]], label="field detection ( deltaGUD = 20)")
    plt.xticks([0, 10], ['start', 'end'])
    plt.xlabel("fa change from 0% - 100%")
    plt.ylabel("GUD")
    plt.title("GUD change with fa")
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 8))
    ax2 = plt.gca()
    im2 = ax2.imshow(GUDs[:, :, 0], interpolation='bilinear')
    cb2 = colorbar(im2, ax=ax2)
    cb2.ax.set_yticks([90, 100, 110, 120, 130])
    ax2.set_title("mix GUDs (Threshold)", size=10)
    plt.ylabel("fa")
    plt.xlabel("interval")
    plt.xticks(np.linspace(0, 10, 6), np.linspace(-20, 20, 6), rotation=45)
    plt.yticks(np.linspace(0, 10, 6), ['0%', '20%', '40%', '60%', '80%', '100%'], rotation=45)
    plt.show()

    GUDsField = np.zeros((11, 11))
    for i, fa in enumerate(np.linspace(0, 1, 11)):
        for j, shiftday in enumerate(shiftDays):
            GUDsField[i, j] = fa * (110 + shiftday) + (1-fa) * 110

    plt.figure(figsize=(10, 8))
    ax2 = plt.gca()
    im2 = ax2.imshow(GUDsField, interpolation='bilinear')
    cb2 = colorbar(im2, ax=ax2)
    cb2.ax.set_yticks([90, 100, 110, 120, 130])
    ax2.set_title("Field mix GUDs (Threshold)", size=10)
    plt.ylabel("fa")
    plt.xlabel("interval")
    plt.xticks(np.linspace(0, 10, 6), np.linspace(-20, 20, 6), rotation=45)
    plt.yticks(np.linspace(0, 10, 6), ['0%', '20%', '40%', '60%', '80%', '100%'], rotation=45)
    plt.show()

    intervalChangeGUDs = (GUDs[:, 1:, 0] - GUDs[:, 0:-1, 0])-(GUDsField[:, 1:] - GUDsField[:, 0:-1])
    plt.figure(figsize=(10, 8))
    ax2 = plt.gca()
    im2 = ax2.imshow(intervalChangeGUDs)
    cb2 = colorbar(im2, ax=ax2)
    # cb2.ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
    ax2.set_title("Change rate (Threshold)", size=10)
    plt.ylabel("fa")
    plt.xlabel("the change rate in each fa")
    plt.xticks([0, 9], ['start', 'end'], rotation=45)
    plt.yticks(np.linspace(0, 10, 6), ['0%', '20%', '40%', '60%', '80%', '100%'], rotation=45)
    plt.show()

    intervalChangeGUDs = np.abs((GUDs[1:, :, 0] - GUDs[0:-1, :, 0]))-np.abs((GUDsField[1:, :] - GUDsField[0:-1, :]))
    intervalChangeGUDs = np.transpose(intervalChangeGUDs)
    plt.figure(figsize=(10, 8))
    ax2 = plt.gca()
    im2 = ax2.imshow(intervalChangeGUDs)
    cb2 = colorbar(im2, ax=ax2)
    # cb2.ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
    ax2.set_title("Change rate (Threshold)", size=10)
    plt.ylabel("interval")
    plt.xlabel("the change rate in each interval")
    plt.xticks([0, 9], ['start', 'end'], rotation=45)
    plt.yticks(np.linspace(0, 10, 6), np.linspace(-20, 20, 6), rotation=45)
    plt.show()


if __name__ == "__main__":
    # mixPattern()
    # GUDderive()
    # advanceReason()
    # __advanceDetection()
    # advanceChangeDetection_faline_show()
    # advanceDetection()
    # advanceDetection_much()
    advanceChangeDetection_line_show()
    advanceChangeDetection_faline_show()
    print("end!")
