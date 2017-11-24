# -*- coding: utf-8 -*-

import numpy as np


def GUDThreCaculate(timeSeris, thre = 0.09):
    threValue = np.max(timeSeris) * thre
    for i in range(len(timeSeris)):
        if timeSeris(i) > threValue:
            return [float(i)/10, threValue]
    return

GUDThreCaculate([1,2,3,4,5])