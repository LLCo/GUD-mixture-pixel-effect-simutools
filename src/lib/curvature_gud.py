# -*- coding:utf-8 -*-
'''
@Author:
    LLC
@Date:
    2018.7.9
@Description:
    Target is a single curve.
    This file is used to calculate the phenology pixel.
    And meantime return the mask value.
    The 1 is usefully while the 0 represent useless.

    The criterion is:
    1. With a low RMSE logistic fit.
    2. With strange phenology data.
    3. The interval of minimal and maximal is small.
    4. The interval of minimal and maximal of fit curve is small.

    The fitting criterion is:
    1. Extend the maximal value to fill up the entire date.
    2. Fit the curve by logistic function.

    通过以下方式调用程序：
    phe = Phenology()
    result = phe.get(vector)  # result为gud, md, vi_gud, vi_md, rmse
'''

import numpy as np
import time
from scipy.optimize import curve_fit
import math


# configuration parameters :
YEAR_DAY = 365
RMSE_THRE = np.inf  # The rmse must lower than it
INTERVAL_THRE = 0.1  # The interval must bigger than it
GUD_UP = 10
GUD_DOWN = 350
MD_UP = 10
MD_DOWN = 350
ApproximateRate = 0.092
Alpha = math.log(5 + 2*math.sqrt(6))


def img_phe(data, loc):
    x_size, y_size, band = data.shape
    result = np.zeros((x_size, y_size, 5))
    phe = Phenology()
    for i in range(x_size):
        for j in range(y_size):
            vector = data[i, j, :]
            result[i, j, :] = phe.get(vector)
    return result, loc


def img_phe_mask(data, img_phe_mask, loc):
    x_size, y_size, band = data.shape
    result = np.zeros((x_size, y_size, 5), dtype=np.float32)
    phe = Phenology()
    for i in range(x_size):
        for j in range(y_size):
            if img_phe_mask[i, j] == 0:
                continue
            vector = data[i, j, :]
            result[i, j, :] = phe.get(vector)
    return result, loc


class Phenology:
    '''
    本类集合了下面的三个类，做到了一步到位的进行优化。
    如果途中发生了任何错误，就返回-1, -1，error code
    else，返回gud，md，rmse
    '''
    def __init__(self):
        self.flt = LogisticFitting()
        self.phe_dri = PhenologyDerive()

    def get(self, vi):
        if not MaskCriterion.min_max_test(vi):  # Test the vi
            __error_meg = (-1, -1, -1)
            return __error_meg

        p, rmse = self.flt.fitting(vi)
        a, b, c, d = p[0]
        if (not MaskCriterion.min_max_logistic_test(c)) or\
                (not MaskCriterion.min_max_logistic_test(p[1][2])):
            __error_meg = (-1, -1, -2)
            return __error_meg

        if not MaskCriterion.parameters_test(a, b, d):
            __error_meg = (-1, -1, -3)
            return __error_meg

        gud, md = self.phe_dri.approximate_phe(a, b, c, d)
        if not MaskCriterion.phenology_test(gud, md):
            __error_meg = (-1, -1, -4)
            return __error_meg
        # self.flt.update_p((a, b), (p[1][0], p[1][1]))  # 传入上次回归出来的值，更新初始值，以方便程序快速收敛
        return gud, md, rmse

    def simple_get(self, vi, need_curves:bool=False):
        p, rmse, curves = self.flt.fitting(vi)
        a, b, c, d = p[0]
        gud, md = self.phe_dri.approximate_phe(a, b, c, d)
        if need_curves:
            return gud, md, rmse, curves
        else:
            return gud, md, rmse


class MaskCriterion:

    @staticmethod
    def min_max_test(vi: np.ndarray):
        return np.max(vi) > 0 and np.max(vi) - np.min(vi) >= INTERVAL_THRE

    @staticmethod
    def min_max_logistic_test(c):
        return c >= INTERVAL_THRE

    @staticmethod
    def phenology_test(gud, gmd):
        return GUD_DOWN >= gud >= GUD_UP and MD_UP <= gmd <= MD_DOWN

    @staticmethod
    def parameters_test(a, b, d):
        return a + b > 2.2 and a + YEAR_DAY*b < -2.5 and b > -1 and d > 0

    @staticmethod
    def rmse_test(rmse):
        return rmse <= RMSE_THRE

    @staticmethod
    def logistic4(t, a, b, c, d, Max=None):
        '''
        experiment = experiment(at+b) ; result = c/experiment + d
        :param a: frequency, speed
        :param b: frequency, shift
        :param c + d: max Value, greenness
        :param d: VI of soil
        :return: logistic curve
        '''

        expValue = np.exp(a + b * t)
        if Max is not None:
            c = Max - d
        logistic_vi = c / (1 + expValue) + d
        return logistic_vi

    @staticmethod
    def VerReLu(x):
        return -x * (-x > 0)


class PhenologyDerive:

    def __init__(self):
        self.vi_time = np.linspace(1, YEAR_DAY, 3660)

    def phenology(self, pslq):
        a, b, c, d = pslq
        return self.approximate_phe(a, b, c, d)

    def accurate_phe(self, a, b, c, d):
        cc = self.__change_rate(a, b, c)
        min_loc = np.argmin(cc)
        if min_loc == 0:
            return 0, 0, 0, 0
        gud = np.argmax(cc[:min_loc]) / 10
        md = (np.argmax(cc[min_loc:]) + min_loc) / 10
        vi_gud = MaskCriterion.logistic4(gud, a, b, c, d)
        vi_md = MaskCriterion.logistic4(md, a, b, c, d)
        return gud, md, vi_gud, vi_md

    def approximate_phe(self, a, b, c, d):

        gud = (Alpha - a) / b
        md = - (a + Alpha) / b
        return gud, md

    def __change_rate(self, a, b, c):
        z = np.exp(a+b*self.vi_time)
        KK_left = b**3 * c * z
        if np.max(np.abs(KK_left)) > 100:
            return np.zeros(len(KK_left))
        KK_middle_left = 3*z*(1-z)*(1+z)**3*(2*(1+z)**3+b**2*c**2*z)/((1+z)**4+(b*c*z)**2)**(5/2)
        KK_middle_right = (1+z)**2*(1+2*z-5*z**2)/((1+z)**4 + (b*c*z)**2)**(3/2)
        result = KK_left * (KK_middle_left - KK_middle_right)
        return result


class LogisticFitting:

    def __init__(self, start_time=0):
        self.vi_time = None
        self.p0 = None
        self.start_time = start_time
        self.__error_meg = ((0, 0, 0, 0), (0, 0, 0, 0)), -5
        self.p0 = np.array([10, -0.08, 0, 0])
        self.p0down = np.array([-21, 0.08, 0, 0])
        pass

    def half_fitting(self, vi: np.ndarray):
        '''
        只拟合上升曲线vi
        :param vi:
        :return:
        '''
        temp_vi = np.array(vi)
        interval = np.max(vi) - np.min(vi)
        if self.vi_time is None:
            self.vi_time = np.linspace(self.start_time, YEAR_DAY, len(temp_vi))  # Building the VI day
        self.__parameter_estimate(temp_vi)
        popt, pcov = curve_fit(MaskCriterion.logistic4, self.vi_time, temp_vi, p0=self.p0)
        return popt

    def fitting(self, vi: np.ndarray):
        temp_vi = np.array(vi)
        interval = np.max(vi) - np.min(vi)
        if self.vi_time is None:
            self.vi_time = np.linspace(self.start_time, YEAR_DAY, len(temp_vi))  # Building the VI day

        self.__parameter_estimate(temp_vi)  # Get the initialized fitting parameters
        max_loc = np.argmax(temp_vi)
        vi_down = temp_vi.copy()
        vi_down[:max_loc] = vi_down[max_loc]
        temp_vi[max_loc:] = temp_vi[max_loc]  # fill the vi by maximal value
        try:
            popt, pcov = curve_fit(MaskCriterion.logistic4, self.vi_time, temp_vi, p0=self.p0)
            popt_down, pcov_down = curve_fit(MaskCriterion.logistic4, self.vi_time, vi_down, p0=self.p0down)
        except RuntimeError:
            return self.__error_meg
        # reconstruct the fitting curve
        vi_fit_up = MaskCriterion.logistic4(self.vi_time, popt[0], popt[1], popt[2], popt[3])
        vi_fit_down = MaskCriterion.logistic4(self.vi_time, popt_down[0], popt_down[1], popt_down[2], popt_down[3])
        split_point_ = np.where(vi_fit_up > vi_fit_down)[0]
        if len(split_point_) == 0:
            return self.__error_meg
        split_point = split_point_[0]
        vi_fit_up[split_point:] = vi_fit_down[split_point:]
        relative_rmse = np.sqrt(np.mean((np.array(vi) - vi_fit_up)**2)) / interval
        return (popt, popt_down), relative_rmse, (self.vi_time, vi_fit_up)

    def cost_function(self, param, vi):
        a, b, c, d = param
        minus = vi - MaskCriterion.logistic4(self.vi_time, a, b, c, d)
        return np.mean(minus**2)

    def __parameter_estimate(self, vi):
        self.p0down[3] = np.percentile(vi, 10, axis=0)
        self.p0down[2] = np.percentile(vi, 90) - self.p0down[3]
        self.p0[2] = self.p0down[2]
        self.p0[3] = self.p0down[3]

    def update_p(self, up, down):
        self.p0[0] = up[0]
        self.p0[1] = up[1]
        self.p0down[0] = down[0]
        self.p0down[1] = down[1]


if __name__ == "__main__":

    # vi = [0.8445, 0.8445, 0.8445, 0.8445, 0.8445, 0.8445, 0.8445, 0.8445, 0.8445, 0.8445,
    #       0.8445, 0.8412, 0.8062, 0.7954, 0.8079, 0.7721, 0.7175, 0.7128, 0.7077, 0.6887,
    #       0.6955, 0.6383, 0.536]

    vi = [0.2513, 0.2, 0.371, 0.25, 0.2707, 0.3031, 0.2764, 0.3111, 0.4220, 0.5697,
          0.7492, 0.8959, 0.9367, 0.8905, 0.7849, 0.6198, 0.4598, 0.3491, 0.2955, 0.2750,
          0.2396, 0.2330, 0.2684]
    vi_time = np.linspace(1, 365, 23)
    rmse = None

    phe = Phenology()
    time0 = time.time()
    for i in range(100):
        for j in range(100):
            gud, md, rmse = phe.get(vi)  # 12.4s for 1e4 pixels
    print('time use: ', time.time() - time0, 's')
    print('rmse: ', rmse)

    # gud, md, rmse = phe.get(vi)
    # plt.figure()
    # plt.plot(vi_time, vi)
    # plt.axvline(gud)
    # plt.axvline(md)
    # plt.show()

    # phe = Phenology()
    # time0 = time.time()
    # for i in range(100):
    #     for j in range(100):
    #         phe.get(vi)
    # print('time use: ', time.time() - time0, 's')