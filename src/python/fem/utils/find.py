# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import numpy as np


def x_max(functions):
    max_val = 0
    for func in functions:
        current = np.max(func[:, 0])
        if current > max_val:
            max_val = current
    return float(max_val)


def y_max(functions):
    max_val = 0
    for func in functions:
        current = np.max(func[:, 1])
        if current > max_val:
            max_val = current
    return float(max_val)


def z_max(functions):
    max_val = 0
    for func in functions:
        current = np.max(func[:, 2])
        if current > max_val:
            max_val = current
    return float(max_val)
