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

    max_val = np.max(functions[0][:, coordinate_number])
    for func in functions:
        current = np.max(func[:, coordinate_number])
        if current > max_val:
            max_val = current
    return float(max_val)


def minimum(functions, coordinate):
    if coordinate == 'x':
        coordinate_number = 0
    elif coordinate == 'y':
        coordinate_number = 1
    elif coordinate == 'z':
        coordinate_number = 2
    else:
        return

    min_val = np.min(functions[0][:, coordinate_number])
    for func in functions:
        current = np.min(func[:, coordinate_number])
        if current < min_val:
            min_val = current
    return float(min_val)
