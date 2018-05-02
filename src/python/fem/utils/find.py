# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import numpy as np


def maximum(functions, coordinate):
    if coordinate == 'x':
        coordinate_number = 0
    elif coordinate == 'y':
        coordinate_number = 1
    elif coordinate == 'z':
        coordinate_number = 2
    else:
        return

    max_val = 0
    for func in functions:
        current = np.max(func[:, coordinate_number])
        if current > max_val:
            max_val = current
    return float(max_val)


