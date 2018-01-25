from Main import *
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from mpl_toolkits.axes_grid1 import make_axes_locatable
import math
import numpy as np

initialAParameterList = [11.105, -0.008, 0.7, 0.1, -24.3, 0.009]
initialAParameterListCopy = [11.105, -0.008, 0.7, 0.1, -24.3, 0.009]
initialBParameterList = [13.501, -0.008, 0.7, 0.1, -27, 0.009]


def print_operation(inputList, weightList, GUDmix, GUDothers, GUDthre, GUDthreothers):
    print("--------------------------------------")
    for i in range(len(GUDothers)):
        tstr = ' a: ' + str(inputList[i][0]) + ' b: ' + str(inputList[i][1]) + ' c: ' + str(inputList[i][2]) + \
               ' d: ' + str(inputList[i][3]) + ' a_down: ' + str(inputList[i][4]) + ' b_down: ' + str(inputList[i][5]) \
               + ' Weight: ' + str(weightList[i])
        print(tstr)
        print("This derivation line GUD is :" + str(GUDothers[i] / 10) + 'day')
    print("the mix derivation lenght GUD is :" + str(GUDmix / 10) + 'day\n')

    for i in range(len(GUDothers)):
        tstr = ' a: ' + str(inputList[i][0]) + ' b: ' + str(inputList[i][1]) + ' c: ' + str(inputList[i][2]) + \
               ' d: ' + str(inputList[i][3]) + ' a_down: ' + str(inputList[i][4]) + ' b_down: ' + str(inputList[i][5]) \
               + ' Weight: ' + str(weightList[i])
        print(tstr)
        print("This thre line GUD is :" + str(GUDthreothers[i] / 10) + 'day')
    print("the mix thre lenght GUD is :" + str(GUDthre / 10) + 'day')


def calculate_list_seris(fix_parameter=None, change_parameter=None, p_a=None, p_b=None, p_c=None, p_d=None, \
                         p_a_down=None, p_b_down=None, fa=0.5):

    step = 3660
    if p_a is None:
        p_a = [change_parameter[0]]
    if p_b is None:
        p_b = [change_parameter[1]]
    if p_c is None:
        p_c = [change_parameter[2]]
    if p_d is None:
        p_d = [change_parameter[3]]
    if p_a_down is None:
        p_a_down = [change_parameter[4]]
    if p_b_down is None:
        p_b_down = [change_parameter[5]]

    seris_length = max([len(p_a), len(p_b), len(p_c), len(p_d), len(p_a_down), len(p_b_down)])

    # b = [[10.0, -0.007, 0.7, 0.1, -27.0, 0.009], [10.7, -0.007, 0.7, 0.1, -27.9, 0.009]]
    GUDmix_curvas = []
    GUDmix_thres = []
    GUDchange_curvas = []
    GUDchange_thres = []
    mix_line = []
    mix_lineSet = []
    for i in range(seris_length):
        input_value = np.array([[p_a[i % len(p_a)], p_b[i % len(p_b)], p_c[i % len(p_c)],\
                       p_d[i % len(p_d)], p_a_down[i % len(p_a_down)], p_b_down[i % len(p_b_down)]], fix_parameter])
        # GUDmix, GUDothers, GUDthre, GUDthreothers = main(input_value, fa=[0.5, 0.5], thre=0.09, txt_flag=False)
        # input_value = input_value.tolist()
        # print_operation(input_value, [0.5, 0.5], GUDmix, GUDothers, GUDthre, GUDthreothers)

        mix_line = allOrinTimeseris(input_value, step, fa=[fa, 1-fa])
        # print(input_value)
        regress_line_up, regress_line_down, total_line = logsticFit.curve_fit(mix_line[-1])  # 获取到了拟合后的像素

        GUDmix_curva, derivative, derivative2, derivative3 = GUDcaculate(regress_line_up)  # 计算混合NDVI光谱的curvature GUD
        GUDmix_thre, thre_value = GUDThreCaculate(mix_line[-1], thre=0.09)  # 计算混合NDVI光谱的relative threshold GUD
        GUDmix_curvas.append(GUDmix_curva)
        GUDmix_thres.append(GUDmix_thre)

        regress_line_up, regress_line_down, total_line = logsticFit.curve_fit(mix_line[0])  # 获取到了拟合后的像素
        mix_lineSet.append(total_line)
        GUDchange_curva, derivative, derivative2, derivative3 = GUDcaculate(regress_line_up)  # 计算混合NDVI光谱的curvature GUD
        GUDchange_thre, thre_value = GUDThreCaculate(mix_line[0], thre=0.09)  # 计算混合NDVI光谱的relative threshold GUD
        GUDchange_curvas.append(GUDchange_curva)
        GUDchange_thres.append(GUDchange_thre)

    '''
    print("--------No Change seris---------")
    regress_line_up, regress_line_down, total_line = logsticFit.curve_fit(mix_line[1])  # 获取到了拟合后的像素
    GUD_no_change_curva, derivative, derivative2, derivative3 = GUDcaculate(regress_line_up)  # 计算混合NDVI光谱的curvature GUD
    GUD_no_change_thre, thre_value = GUDThreCaculate(mix_line[1], thre=0.09)  # 计算混合NDVI光谱的relative threshold GUD
    print("curvature GUD is :" + str(GUD_no_change_curva/10) + 'day' + " relative threshold GUD is :" + str(GUD_no_change_thre/10) + 'day')

    print("--------Change seris---------")
    # for i in range(len(GUDchange_curvas)):
    #     print("curvature GUD is :" + str(GUDchange_curvas[i]/10) + 'day' + " relative threshold GUD is :" + str(GUDchange_thres[i]/10) + 'day')
    print('thres: '+ str(np.array(GUDchange_thres) / 10))
    print('curvate: ' + str(np.array(GUDchange_curvas)/10))


    print("--------mix---------")
    # for i in range(len(GUDmix_curvas)):
    #     print("curvature GUD is :" + str(GUDmix_curvas[i]/10) + 'day' + " relative threshold GUD is :" + str(GUDmix_thres[i]/10) + 'day')
    print('thres: ' + str(np.array(GUDmix_thres) / 10))
    print('curvate: ' + str(np.array(GUDmix_curvas)/10))
    '''

    return GUDmix_thres, GUDmix_curvas, mix_lineSet


def unknown_plane_affect():

    pa_list = [round(initialAParameterList[0] - x * 10 * 0.008, 3) for x in range(-30, 30)]
    pa_down_list = [-round(abs(initialAParameterList[4]) - x * 10 * 0.009, 3) for x in range(-30, 30)]

    GUDmix_thres, GUDmix_curvas, mix_lineset = calculate_list_seris(initialAParameterListCopy, initialAParameterList,
                                                                    p_a=pa_list, p_a_down=pa_down_list)
    GUDmix_thres = np.array(GUDmix_thres)[::-1] / 10
    GUDmix_curvas = np.array(GUDmix_curvas)[::-1] / 10
    GUDmix_true = np.arange(-30, 30, 1) / 2 + 110
    plt.figure(1)
    plt.plot(range(-30, 30), GUDmix_thres, label='threshold GUD')
    plt.plot(range(-30, 30), GUDmix_curvas, label='curvature GUD')
    plt.plot(range(-30, 30), GUDmix_true, label='curvature GUD')
    plt.axvline(0, lw=4, ls='--', color='r', label='known plane GUD')
    plt.xlabel('unknown plane delta GUD')
    plt.ylabel('mix GUD')
    plt.title('mix GUD change with different unknown plane')
    plt.legend(loc='best')
    plt.grid()

    mix_lineset = np.array(mix_lineset)
    plt.figure(2)
    plt.ylim([0, 0.9])
    plt.xlim([0, 3660])
    plt.plot(range(len(mix_lineset[0, :])), mix_lineset[0, :], color='r', ls='--', lw=1, label='unknown plane B, right')
    plt.plot(range(len(mix_lineset[-1, :])), mix_lineset[-1, :], color='g', ls='--', lw=1, label='unknown plane B, left')
    plt.plot(range(len(mix_lineset[29, :])), mix_lineset[29, :], color=(0.5, 0.5, 0), ls='-', lw=2, label='known plane A')
    label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec','Jan']
    plt.xticks(np.int16(np.linspace(0, 3660, 5)), [label[0], label[3], label[6], label[9], label[12]], rotation=45)
    # plt.xlabel('day of year')
    plt.ylabel('NDVI')
    plt.title('mix model')
    plt.legend(loc='best')
    plt.grid()
    plt.show()


def unknown_plane_affect_and_fa(fas=None):
    '''
    当我们想检测某种植被的准确返青期，可能会因为在该区域一些返青期提前于它的植被，而检测结果提前。

    当我们想检测某种植被的返青期变化，可能会因为在该区域一些返青期在它之前的植被的影响，从而检测不到。
    '''
    if fas is None:
        fas = np.arange(0, 1.01, 0.25)
    pa_list = [round(initialAParameterList[0] - x * 10 * 0.008, 3) for x in range(-30, 30)]
    pa_down_list = [-round(abs(initialAParameterList[4]) - x * 10 * 0.009, 3) for x in range(-30, 30)]
    mat_curvas = np.zeros((len(fas), len(pa_list)))
    mat_threshhold = mat_curvas.copy()

    for i, fa in enumerate(fas):
        GUDmix_thres, GUDmix_curvas, mix_lineset = calculate_list_seris(initialAParameterListCopy,
                        initialAParameterList,p_a=pa_list, p_a_down=pa_down_list, fa=fa)
        mat_curvas[i, :] = np.array(GUDmix_curvas[::-1]) / 10
        mat_threshhold[i, :] = np.array(GUDmix_thres[::-1]) / 10

    cm = plt.get_cmap('jet')
    cNorm = colors.Normalize(vmin=0, vmax=5)
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)
    print(scalarMap.get_clim())
    plt.figure(figsize=(10, 10))
    plt.plot(range(-29, 31), mat_curvas[0, :], label='fb = ' + str(fas[0]*100) + '%', color=scalarMap.to_rgba(0))
    plt.plot(range(-29, 31), mat_curvas[1, :], label='fb = ' + str(fas[1]*100) + '%', color=scalarMap.to_rgba(1))
    plt.plot(range(-29, 31), mat_curvas[2, :], label='fb = ' + str(fas[2]*100) + '%', color=scalarMap.to_rgba(2))
    plt.plot(range(-29, 31), mat_curvas[3, :], label='fb = ' + str(fas[3]*100) + '%', color=scalarMap.to_rgba(3))
    plt.plot(range(-29, 31), mat_curvas[4, :], label='fb = ' + str(fas[4]*100) + '%', color=scalarMap.to_rgba(4))

    plt.axvline(0, lw=4, ls='--', color='r', label='known plane GUD')
    plt.xlabel('unknown plane delta GUD')
    plt.ylabel('mix GUD')
    plt.title('mix GUD change with different unknown plane and fa')
    plt.legend(loc='best')
    plt.grid()
    plt.show()


def error_detection_contourmap():

    fas = np.arange(0, 0.31, 0.02)
    pa_list = [round(initialAParameterList[0] - x * 10 * 0.008, 3) for x in range(-30, 30)]
    pa_down_list = [-round(abs(initialAParameterList[4]) - x * 10 * 0.009, 3) for x in range(-30, 30)]
    mat_curvas = np.zeros((len(fas), len(pa_list)))
    mat_threshhold = mat_curvas.copy()

    for i, fa in enumerate(fas):
        GUDmix_thres, GUDmix_curvas, mix_lineset = calculate_list_seris(initialAParameterListCopy,
                        initialAParameterList,p_a=pa_list, p_a_down=pa_down_list, fa=fa)
        mat_curvas[i, :] = np.array(GUDmix_curvas[::-1]) / 10
        mat_threshhold[i, :] = np.array(GUDmix_thres[::-1]) / 10
    mat_curvas = -(mat_curvas - 110)
    mat_curvas[np.where(mat_curvas > 5)] = 5
    mat_curvas = np.round(mat_curvas)

    plt.figure(figsize=(10, 8))
    plt.xlabel('delta GUD')
    plt.ylabel('disturb proportion (%)')
    ax = plt.gca()
    ax.set_yticks([0, 4, 8, 12, 16])
    ax.set_yticklabels(['0%', '7.5%', '15%', '22.5%', '30%'])
    ax.set_xticks([0, 14, 29, 44, 59])
    ax.set_xticklabels(['-30 day', '-15 day', '0 day', '15 day', '30 day'])
    divider = make_axes_locatable(ax)
    cm = plt.get_cmap('jet', 9)
    im = ax.imshow(mat_curvas, cmap=cm, interpolation='bilinear', vmax=mat_curvas.max(), vmin=mat_curvas.min())
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im, cax=cax)
    plt.show()


def miss_dynamic_detection_contourmap():
    fas = np.arange(0.70, 1.01, 0.02)
    pa_list = [round(initialAParameterList[0] - x * 10 * 0.008, 3) for x in range(-30, 30)]
    pa_down_list = [-round(abs(initialAParameterList[4]) - x * 10 * 0.009, 3) for x in range(-30, 30)]
    mat_curvas = np.zeros((len(fas), len(pa_list)))
    mat_threshhold = mat_curvas.copy()
    for i, fa in enumerate(fas):
        GUDmix_thres, GUDmix_curvas, mix_lineset = calculate_list_seris(initialAParameterListCopy,
                        initialAParameterList,p_a=pa_list, p_a_down=pa_down_list, fa=fa)
        mat_curvas[i, :] = np.array(GUDmix_curvas[::-1]) / 10
        mat_threshhold[i, :] = np.array(GUDmix_thres[::-1]) / 10
    mat_curvas_minus = mat_curvas[:, :-1] - mat_curvas[:, 1:]
    mat_curvas_minus = -np.round(mat_curvas_minus * 5)
    mat_curvas_minus[np.where(mat_curvas_minus > 5)] = 5
    mat_curvas_minus = np.int8(mat_curvas_minus)
    plt.figure(figsize=(10, 8))
    plt.xlabel('delta GUD')
    plt.ylabel('disturb proportion (%)')
    ax = plt.gca()
    ax.set_yticks([15, 11, 7, 4, 0])
    ax.set_yticklabels(['0%', '7.5%', '15%', '22.5%', '30%'])
    ax.set_xticks([0, 14, 29, 44, 58])
    ax.set_xticklabels(['-30 day', '-15 day', '0 day', '15 day', '29 day'])
    divider = make_axes_locatable(ax)
    cm = plt.get_cmap('jet', 5)
    im = ax.imshow(mat_curvas_minus, cmap=cm, interpolation='bilinear', vmax=mat_curvas_minus.max(), vmin=mat_curvas_minus.min())
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im, cax=cax)
    plt.show()


def normal(u=0, sig=1, sample_numbers=11):
    x1 = np.linspace(u - 3 * sig, u, 25)
    x2 = np.linspace(u, u + 3 * sig, 25)
    x = np.append(x1, x2[1:])
    # print(x)
    y = np.exp(-(x - u) ** 2 / (2 * sig ** 2)) / (math.sqrt(2 * math.pi) * sig)
    sample_point = np.int8(np.linspace(0, 24, int(sample_numbers/2) + 1))
    sample_point_inverse = (sample_point[-1] - (sample_point - sample_point[-1]))[::-1]
    sample_point = np.append(sample_point, sample_point_inverse[1:])
    gud = np.array(x[sample_point])
    fa = np.array(y[sample_point])
    '''
    plt.figure()
    plt.plot(x, y)
    plt.plot(gud, fa, 'ro')
    plt.grid()
    plt.axvline(110, lw=4, color='r', ls='--')
    plt.legend()
    plt.xlabel('day of year')
    plt.ylabel('distribution')
    plt.show()
    '''
    # gud = np.round(gud)
    fa = fa / fa.sum()
    return fa, gud, x, y


def normal_detection(sig=3):
    step = 3660
    centerGUD = 110
    fa, gud, x, y = normal(u=centerGUD, sig=sig)
    gud = gud - 110
    pa_list = [round(initialAParameterList[0] - x * 10 * 0.008, 3) for x in gud]
    pa_down_list = [-round(abs(initialAParameterList[4]) - x * 10 * 0.009, 3) for x in gud]

    input_value = []
    for i in range(len(pa_list)):
        input_value.append([pa_list[i % len(pa_list)], initialAParameterList[1], initialAParameterList[2], \
                    initialAParameterList[3], pa_down_list[i % len(pa_down_list)], initialAParameterList[5]])
    input_value = np.array(input_value)
    mix_line = allOrinTimeseris(input_value, step, fa=fa)
    # print(input_value)
    regress_line_up, regress_line_down, total_line = logsticFit.curve_fit(mix_line[-1])  # 获取到了拟合后的像素

    GUDmix_curva, derivative, derivative2, derivative3 = GUDcaculate(regress_line_up)  # 计算混合NDVI光谱的curvature GUD
    GUDmix_thre, thre_value = GUDThreCaculate(mix_line[-1], thre=0.09)  # 计算混合NDVI光谱的relative threshold GUD

    print('GUDmix_thre:', GUDmix_thre, 'GUDmix_curva:', GUDmix_curva)

    '''
    for i in range(len(pa_list)):
        centerPoint = i
        input_value = []
        input_value.append([pa_list[centerPoint], initialAParameterList[1], initialAParameterList[2], \
                    initialAParameterList[3], pa_down_list[centerPoint], initialAParameterList[5]])
        input_value.append([pa_list[centerPoint], initialAParameterList[1], initialAParameterList[2], \
                    initialAParameterList[3], pa_down_list[centerPoint], initialAParameterList[5]])
        input_value = np.array(input_value)
        mix_line = allOrinTimeseris(input_value, step, fa=[0.5, 0.5])
        regress_line_up, regress_line_down, total_line = logsticFit.curve_fit(mix_line[-1])  # 获取到了拟合后的像素
        GUDmix_curva, derivative, derivative2, derivative3 = GUDcaculate(regress_line_up)  # 计算混合NDVI光谱的curvature GUD
        GUDmix_thre, thre_value = GUDThreCaculate(mix_line[-1], thre=0.09)  # 计算混合NDVI光谱的relative threshold GUD
        print('GUDmix_thre:', GUDmix_thre, 'GUDmix_curva:', GUDmix_curva)
    '''
    return GUDmix_curva, x, y


def normal_detection_s():
    # plt.figure()
    # plt.grid()
    # colors = ['y', 'g', 'b']
    a = []
    for i in range(1, 20):
        mix_curvature, x, y = normal_detection(sig=i)
        mix_curvature = mix_curvature / 10
        a.append(mix_curvature)
        # plt.plot(x, y, label='sigma = ' + str(i) + ',GUD is : ' + str(mix_curvature), color=colors[int(i/5)-1])
        # plt.axvline(mix_curvature, lw=2, color=colors[int(i/5)-1], ls='--')
    # plt.axvline(110, lw=4, color='r', ls='--')
    # plt.legend()
    # plt.xlabel('day of year')
    # plt.ylabel('distribution')
    # plt.show()
    return a


def experiment_one():
    fb_list = np.arange(0.1, 1.1, 0.1)
    gud_thres_list = []
    gud_curva_list = []
    for fb in fb_list:
        GUDmix_thres, GUDmix_curvas, mix_lineset = calculate_list_seris(initialAParameterList,
                                                                        initialBParameterList,
                                                                        fa=fb)
        gud_thres_list.append(GUDmix_thres[0])
        gud_curva_list.append(GUDmix_curvas[0])
    plt.figure()
    plt.plot(gud_thres_list)
    plt.plot(gud_curva_list)
    plt.xlabel('fb ')
    plt.ylabel('green up date')
    plt.show()


# def experiment_two():

# def experiment_three:

if __name__ == '__main__':
    # unknown_plane_affect()
    # fas = np.arange(0.75, 1.01, 0.05)
    # unknown_plane_affect_and_fa(fas=fas)
    # error_detection_contourmap()
    # miss_dynamic_detection_contourmap()
    '''
    a = normal_detection_s()
    plt.figure()
    plt.plot(range(1, 20), a, label='GUD change with sigma')
    plt.axhline(110, color='r', ls='--', label='true GUD')
    plt.ylabel('GUD')
    plt.xlabel('sigma')
    plt.legend()
    plt.show()
    print()
    '''
    unknown_plane_affect()
