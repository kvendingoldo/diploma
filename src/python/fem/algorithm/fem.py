# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import matplotlib.pyplot as plt
import numpy as np

from sympy import *

from geometry.point import Point
from fe.triangle import Triangle

# constants
rho = 1
x1, x2 = symbols('x1 x2')



def integrate_by_triangle(func, triangle):
    x, y = symbols('x y')
    s = trianglelement.area

    integral_x = func.coeff(x) * s * Triangle.x(triangle.centroid())
    integral_y = func.coeff(y) * s * Triangle.y(triangle.centroid())
    integral_s = func.subs(x, 0).subs(y, 0) * s

    print(Float(integral_s + integral_x + integral_y))

    return Float(integral_s + integral_x + integral_y)


def choise(element, number):
    N_i, N_j, N_k = element.get_basic_functions()
    if element[1].number == number:
        return N_i
    elif element[2].number == number:
        return N_j
    elif element[3].number == number:
        return N_k
    else:
        return 0


def system(vars, time, mesh):
    elements = mesh.splitting
    M = mesh.quantity

    sys = list()


    for element in elements:
        #N_i, N_j, N_k = element.get_basic_functions()
        for k in range(0, ((3 * M)-1)):
            coeff_of_derivative = 0
            B = 0
            if k < M:
                pass
                # eq2
            elif k >= M and  k < 2 * M:
                pass
                # eq3
            else:
                # eq1
                for l in range(0, ((3 * M)-1)):
                    W_l = choise(element, l+1)
                    N_k = choise(element, k+1)
                    coeff_of_derivative += W_l
                    #B += -(integrate_by_triangle(W_l * diff(N_k, x1)) * vars[k-1] +
                    #     integrate_by_triangle(W_l * diff(N_k, x2)) * vars[M+k-1])
                print(coeff_of_derivative)
                print()
                #coef = integrate_by_triangle(rho * coef * N_k, element)
                #sys_k
                #sys += B / coef
    return sys







