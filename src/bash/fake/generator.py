# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import numpy as np

from random import randint

MIN_VAL = 0
MAX_VAL = 100

def on_bondary(point, mesh):
    for pnt in mesh.contour:
        if (point[0] == pnt[0]) and (point[1] == pnt[1]):
            return True
    return False


def gen_solution_vector(mesh):
    solution = []
    print(len(mesh.points))

    for point in mesh.points:
        if on_bondary(point, mesh):
            solution.append([0.0])
        else:
            solution.append([randint(MIN_VAL, MAX_VAL) / randint(10, 100)])

    return np.array(solution)


