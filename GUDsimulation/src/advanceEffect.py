from Main import *
import batchCalculator
import timeseris
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as pcolor
import numpy as np

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


def __advanceDetection():

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


def advanceChangeDetection():

    return

if __name__ == "__main__":
    # mixPattern()
    # GUDderive()
    # advanceReason()
    advanceDetection()
    # __advanceDetection()
    print("end!")
