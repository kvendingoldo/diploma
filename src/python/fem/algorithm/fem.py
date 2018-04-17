# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import matplotlib.pyplot as plt
import numpy as np
# from mpmath import *

from sympy import *
from sympy import sqrt
from sympy.plotting import plot3d

from scipy.integrate import odeint

from geometry.point import Point
from fe.triangle import Triangle

# constants

# плотность воды [кг / м^3]
rho = 1000

# плотность воздуха [кг / м^3]
rho_a = 1.2754

# давление на поверхности воды [Па]
P_a = 10 ** 5

# скорость ветра [м / c]
W = 1

# gamma ^ 2
gamma = 0.002

# ускорение свободного падения [м * c^2]
g = 9.832

# коэффициент трения Шэззи
C = 1


def solve(mesh):
    M = mesh.quantity
    elements = mesh.splitting
    x1, x2 = symbols('x_1 x_2')

    def system(variables, time):
        print('time=%s' % time)
        sysfun = np.zeros(shape=(3 * M))

        for element in elements:
            f_eq1 = 0
            f_eq2 = 0
            f_eq3 = 0
            for k in range(0, M):
                N_k = element.get_basic_function_by_number(k)
                weight_functions = 0
                for l in range(0, M):
                    W_l = element.get_basic_function_by_number(l)
                    weight_functions += W_l

                    f_eq1 += \
                        + element.integrate(W_l * diff(-P_a * variables[2 * M + k] * N_k - g * rho / 2 * variables[2 * M + k] ** 2 * N_k ** 2, x1)) \
                        + element.integrate(P_a * W_l * diff(variables[2 * M + k] * N_k, x1)) \
                        + element.integrate(W ** 2 * gamma * rho_a * W_l) \
                        - element.integrate((g * W_l * variables[k] / C ** 2 * rho * variables[2 * M + k] ** 2 * N_k) * sqrt(variables[k] ** 2 * N_k ** 2 + variables[M + k] ** 2 * N_k ** 2))

                    f_eq2 += \
                        + element.integrate(W_l * diff(-P_a * variables[2 * M + k] * N_k - g * rho / 2 * variables[2 * M + k] ** 2 * N_k ** 2, x2)) \
                        + element.integrate(P_a * W_l * diff(variables[2 * M + k] * N_k, x2)) \
                        - element.integrate((g * W_l * variables[M + k] / C ** 2 * rho * variables[2 * M + k] ** 2 * N_k) * sqrt(variables[k] ** 2 * N_k ** 2 + variables[M + k] ** 2 * N_k ** 2))

                    f_eq3 += \
                        - element.integrate(W_l * diff(N_k, x1)) * variables[k] \
                        - element.integrate(W_l * diff(N_k, x2)) * variables[M + k]

                coefficient_of_d_eq1 = element.integrate(weight_functions * N_k)
                coefficient_of_d_eq2 = element.integrate(weight_functions * N_k)
                coefficient_of_d_eq3 = element.integrate(rho * weight_functions * N_k)

                if coefficient_of_d_eq1 != 0:
                    sysfun[k] += (f_eq1 / coefficient_of_d_eq1)
                # [x / coefficient_of_d_eq1 for x in f_eq2]

                if coefficient_of_d_eq2 != 0:
                    sysfun[M + k] += (f_eq2 / coefficient_of_d_eq2)
                # [x / coefficient_of_d_eq2 for x in f_eq3]

                if coefficient_of_d_eq3 != 0:
                    sysfun[2 * M + k] += (f_eq3 / coefficient_of_d_eq3)
                # [x / coefficient_of_d_eq3 for x in f_eq1]

        # print('sysfun=%s\n' % sysfun)

        return sysfun

    time = np.linspace(3, 4, 10)
    y0 = np.zeros(3 * M)
    sol = odeint(system, y0, time)

    q1_list = list()
    q2_list = list()
    H_list = list()

    for element in mesh.splitting:
        for ind in range(0, M):
            q1 = 0
            q2 = 0
            H = 0
            for k in range(0, M):
                N_k = element.get_basic_function_by_number(k)
                q1 += N_k * sol[ind][M + k]
                q2 += N_k * sol[ind][k]
                H += N_k * sol[ind][2 * M + k]

            q1_list.append(q1)
            q2_list.append(q2)
            H_list.append(H)

    print(sol)
    print(time)
    # print(q1_list)
    # print(q2_list)
    print(H_list)
    plot3d(H_list[1], (x1, -1, 1), (x2, -1, 1))
