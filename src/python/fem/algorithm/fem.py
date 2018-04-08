# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import matplotlib.pyplot as plt
import numpy as np

from sympy import *

from geometry.point import Point
from fe.triangle import Triangle


def integrate_by_triangle(func, triangle):
    x, y = symbols('x y')
    s = trianglelement.area

    integral_x = func.coeff(x) * s * Triangle.x(triangle.centroid())
    integral_y = func.coeff(y) * s * Triangle.y(triangle.centroid())
    integral_s = func.subs(x, 0).subs(y, 0) * s

    print(Float(integral_s + integral_x + integral_y))

    return Float(integral_s + integral_x + integral_y)


def calc(mesh):

    x1, x2, t = var('x1 x2 t', real=True)
    rho, rho_a, gamma, theta = symbols('rho rho_a gamma theta')
    f, W, g, c, Pa, h = symbols('f W g c Pa h')
    H, q1, q2 = symbols('H q1 q2')
    a_1, a_2 = symbols('a_1, a_2')

    eq1 = Derivative(q1, x1) + Derivative(q2, x2) + Derivative(rho * H, t)
    #eq2 = Derivative(q1, t) - (gamma**2 * rho_a * W**2 * cos(theta)) - Pa * Derivative(H, x1) - (rho * g * H) * Derivative(h, x1)
    #eq3 = Derivative(q2, t) - (gamma**2 * rho_a * W**2 * sin(theta)) - Pa * Derivative(H, x2) - (rho * g * H) * Derivative(h, x2)

    elements = mesh.splitting
    M = mesh.quantity
    K = np.zeros(shape=((3 * M), (3 * M)))
    f = np.zeros(shape=((3 * M)))

    sum = 0

    for element in elements:

        N_i, N_j, N_k = element.get_basic_functions()

        print(N_i)
        print(N_j)
        print(N_k)

        #x, y, t = symbols('x y t')
        #q_1 = a_11(t) * N_i + a_12(t) * N_j + a_13(t) * N_k
        #q_2 = a_21(t) * N_i + a_22(t) * N_j + a_23(t) * N_k
        #H = a_31(t) * N_i + a_32(t) * N_j + a_33(t) * N_k

