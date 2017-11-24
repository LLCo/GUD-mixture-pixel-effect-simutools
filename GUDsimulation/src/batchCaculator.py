from Main import *

initialAParameter = {'a': 11.105, 'b': -0.008, 'c': 0.7, 'd': 0.1, 'a_down': -24.3, 'b_down': 0.009}
initialBParameter = {'a': 13.501, 'b': -0.008, 'c': 0.7, 'd': 0.1, 'a_down': -27, 'b_down': 0.009}
initialAParameterList = [11.105, -0.008, 0.7, 0.1, -24.3, 0.009]
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

    for i in range(seris_length):
        input_value = np.array([[p_a[i % len(p_a)], p_b[i % len(p_b)], p_c[i % len(p_c)],\
                       p_d[i % len(p_d)], p_a_down[i % len(p_a_down)], p_b_down[i % len(p_b_down)]], fix_parameter])
        # GUDmix, GUDothers, GUDthre, GUDthreothers = main(input_value, fa=[0.5, 0.5], thre=0.09, txt_flag=False)
        # input_value = input_value.tolist()
        # print_operation(input_value, [0.5, 0.5], GUDmix, GUDothers, GUDthre, GUDthreothers)

        mix_line = allOrinTimeseris(input_value, step, fa=[fa, 1-fa])
        print(input_value)
        regress_line_up, regress_line_down, total_line = logsticFit.curve_fit(mix_line[-1])  # 获取到了拟合后的像素
        GUDmix_curva, derivative, derivative2, derivative3 = GUDcaculate(regress_line_up)  # 计算混合NDVI光谱的curvature GUD
        GUDmix_thre, thre_value = GUDThreCaculate(mix_line[-1], thre=0.09)  # 计算混合NDVI光谱的relative threshold GUD
        GUDmix_curvas.append(GUDmix_curva)
        GUDmix_thres.append(GUDmix_thre)

        regress_line_up, regress_line_down, total_line = logsticFit.curve_fit(mix_line[0])  # 获取到了拟合后的像素
        GUDchange_curva, derivative, derivative2, derivative3 = GUDcaculate(regress_line_up)  # 计算混合NDVI光谱的curvature GUD
        GUDchange_thre, thre_value = GUDThreCaculate(mix_line[0], thre=0.09)  # 计算混合NDVI光谱的relative threshold GUD
        GUDchange_curvas.append(GUDchange_curva)
        GUDchange_thres.append(GUDchange_thre)

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

    return GUDmix_thres,GUDmix_curvas


# calculate_list_seris(fix_parameter=initialBParameterList, change_parameter=initialAParameterList,\
#                      p_a=[11.105, 10.705, 10.305, 9.905, 9.505])
#   GUDmix_thres,GUDmix_curvas = calculate_list_seris(\
#                        fix_parameter=initialAParameterList, change_parameter=initialBParameterList,\
#                        p_a=[13.501, 13.901, 14.301, 14.704, 15.101], fa=i)
print('\n\n-------------------------------------------------------\n\n')
threMatrix = []
curvaMatrix = []
for i in np.arange(0.1, 0.901, 0.1):
    GUDmix_thres, GUDmix_curvas = calculate_list_seris(fix_parameter=initialBParameterList, change_parameter=initialAParameterList,\
            p_a=[11.105, 10.705, 10.305, 9.905, 9.505], fa=i)
    threMatrix.append(GUDmix_thres)
    curvaMatrix.append(GUDmix_curvas)
print(np.array(threMatrix)/10)
print('\n\n-------------------------------------------------------\n\n')
print(np.array(curvaMatrix)/10)
