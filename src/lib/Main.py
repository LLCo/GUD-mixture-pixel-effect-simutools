# -*- coding: utf-8 -*-
"""
This code provide input of GUD algorithm to C# UI program.
Function:
    input: NDVI time seris array/txt file
    output: 1.Original NDVI time seris map
            2.mix NDVI time seris map
            3.Curve Fit NDVI time seris map
"""
import matplotlib.pyplot as plt
import numpy as np

from lib import timeseris
from lib.curvature_gud import Phenology


def GUDThreCaculate(timeSeris, thre=0.09):

    if np.max(timeSeris) - np.min(timeSeris) < 0.05:
        return -1, -1

    threValue = (np.max(timeSeris) - np.min(timeSeris)) * thre + np.min(timeSeris)
    for i in range(len(timeSeris)):
        if timeSeris[i] > threValue:
            offset = (timeSeris[i] - threValue) / (timeSeris[i] - timeSeris[i - 1])
            return i - offset, threValue
    return


def GUDcaculate(timeSeris):

    if np.max(timeSeris) - np.min(timeSeris) < 0.05:
        return -1, np.linspace(0, 365, len(timeSeris)), timeSeris
    phe = Phenology()
    GUD, _, _, curves = phe.simple_get(timeSeris, need_curves=True)  # result为gud, md, vi_gud, vi_md, rmse
    t, fit_curve = curves
    return GUD, t, fit_curve


def drawPreview(parameter, name):
    STEP = 365
    line = timeseris.get_initial_line(
        parameter[0], parameter[1], parameter[2],
        parameter[3], parameter[4], parameter[5],
        STEP)
    plt.figure(figsize=(4.5, 3))
    plt.plot(range(len(line)), line, 'r', lw=2, label='preview line')
    plt.ylim([0, 1])
    plt.xlim([0, 365])
    plt.title('preview')
    plt.xlabel('0.1 Day of year')
    plt.ylabel('NDVI')
    plt.legend(loc='upper left')
    label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec','Jan']
    plt.xticks(np.int16(np.linspace(0, 365, 5)), [label[0], label[3], label[6], label[9], label[12]], rotation=45)
    plt.savefig(name)
    pass


def __drawThree(totalLine,GUDthre,threValue,thre):
    plt.figure(figsize=(5, 3))
    plt.title('GUD calculate by threshold')
    plt.xlabel('Day of year')
    plt.ylabel('NDVI')
    plt.plot(range(len(totalLine)),totalLine,'r-',lw = 2,label='orin')
    plt.ylim([0, 1]);
    plt.xlim([0, 365]);
    plt.axvline(GUDthre,ls = '--',lw = 3,label='GUD: ' + str(int(GUDthre/10)) + ' day')
    plt.axhline(threValue,ls = '--',lw = 2,color = 'r',label='%' + str(thre * 100) + ' NDVI')
    label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec','Jan']
    plt.xticks(np.int16(np.linspace(0, 365, 5)), [label[0],label[3],label[6],label[9],label[12]], rotation=45)
    plt.legend(loc ='upper left')
    plt.savefig("data\drawThree.png")
    pass


def __drawTwo(GUD, t, curve):# 画出不同的原始曲线
    '''
    画出第一幅显示图像，其内容有:
        1、原始的拟合后的混合时序变化图
        2、一阶倒数
        3、二阶倒数
        4、三阶倒
        5、返青期直线
    '''
    plt.figure(figsize=(5, 3))
    plt.title('GUD calculate by curvature')
    plt.xlabel('Day of year')
    plt.ylabel('NDVI')
    plt.plot(t, curve, 'r-', lw=2, label='orin')
    plt.ylim([0, 1])
    plt.xlim([0, 365])
    plt.axvline(GUD,ls = '--',lw = 3)
    label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec','Jan']
    plt.xticks(np.int16(np.linspace(0, 365, 5)), [label[0],label[3],label[6],label[9],label[12]], rotation=45)
    # ax1 = plt.gca()
    # ax2 = ax1.twinx()  # this is the important function
    # ax2.plot(range(len(derivative)),derivative,'--',label='first D')
    # ax2.plot(range(len(derivative2)),derivative2,'--',label='second D')
    # ax2.plot(range(len(derivative3)),derivative3,'-',lw = 2,label='third D')
    plt.legend(loc='upper left')
    # ax2.legend(loc ='upper right')
    plt.savefig("data\drawTwo.png")


def __drawOne(mixline,fit_curve, t, STEP):# 画出不同的原始曲线
    '''
    画出第一幅显示图像，其内容有:
        1、几条原始时序变化图
        2、求和后的时序变化图
        3、拟合后的时序变化图
    '''
    x = np.arange(0, STEP, 1)
    lineNums = mixline.shape[0]
    plt.figure(figsize=(4.5, 3))
    for i in range(lineNums - 1):
        plt.plot(x, mixline[i], '--', label='line:' + str(i))
    
    plt.plot(x, mixline[-1], 'r', lw = 4, label='mix line')
    plt.plot(t, fit_curve, 'g', lw = 2, label='fit line')
    plt.ylim([0, 1])
    plt.xlim([0, 365])
    plt.title('Mix & Fit')
    plt.xlabel('Day of year')
    plt.ylabel('NDVI')
    plt.legend(loc ='upper left')
    label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec','Jan']
    plt.xticks(np.int16(np.linspace(0, 365, 5)), [label[0],label[3],label[6],label[9],label[12]], rotation=45)
    plt.savefig("data\drawOne.png")


def __read_txt(txt_path,STEP):
    '''
    输入原始NDVI时序数据，获得混合曲线
    '''
    array = np.arange(0, STEP, 1)
    return array


def allOrinTimeseris(input_value, STEP, fa=[0.3, 0.3, 0.4]):
    '''
    输入原始NDVI参数，获得混合曲线
    '''
    onelines = np.zeros([input_value.shape[0], STEP])
    for index, parameters in enumerate(input_value):
        onelines[index] = timeseris.get_initial_line(
            parameters[0], parameters[1], parameters[2],
            parameters[3], parameters[4], parameters[5],
            STEP)
    '''
    判断fa
    '''
    mixline = 0
    for index, val in enumerate(fa):
        mixline = mixline + val * onelines[index]
    mixline = np.row_stack((onelines, mixline))
    
    return mixline


def main(input_value, fa=None, thre=0.092, txt_flag=False):
    STEP = 365
    if txt_flag:
        input_value = __read_txt(input_value, STEP)
    input_value = np.array(input_value)
    if fa is None:
        fa = [0.3, 0.3, 0.4]
    mixline = allOrinTimeseris(input_value, STEP, fa=fa)  # 获取到了输入各种参数后的混合光谱\

    # regress_line_up, regress_line_down, totalLine = logsticFit.curve_fit(mixline[-1]) # 获取到了拟合后的像素
    gud_mix, t, fit_curve = GUDcaculate(mixline[-1])
    __drawOne(mixline, fit_curve, t, STEP)  # 画出第一条显示的图像

    '''
    计算混合NDVI光谱的GUD
    '''
    GUDthre, threValue = GUDThreCaculate(mixline[-1], thre)
    __drawTwo(gud_mix, t, fit_curve)

    '''
    原始光谱的GUD
    '''
    __drawThree(fit_curve, GUDthre, threValue, thre) #画出第一条显示的图像

    GUDothers = []
    GUDthreothers = []
    for i in range(mixline.shape[0] - 1):
        GUDa, _, _ = GUDcaculate(mixline[i])
        GUDb, _ = GUDThreCaculate(mixline[i], thre)
        GUDothers.append(GUDa)
        GUDthreothers.append(GUDb)

    return [gud_mix, GUDothers, GUDthre, GUDthreothers]


if __name__ == "__main__" :
    '''
    print(timeseris.initialAParameter)
    '''
    # print(sys.path)
    a = [[10,-0.007,0.7,0.1,-27,0.009],[9,-0.007,0.7,0.1,-27,0.009],[11,-0.007,0.7,0.1,-27,0.009]]
    b = [[10.0, -0.007, 0.7, 0.1, -27.0, 0.009], [10.7, -0.007, 0.7, 0.1, -27.9, 0.009]]
    fa = [0.5, 0.5]
    main(b, fa=fa)
    #main()