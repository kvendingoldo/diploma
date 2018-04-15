# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import matplotlib.pyplot as plt
import numpy as np

from sympy import *
from scipy import ones
from scipy.integrate import odeint

from geometry.point import Point
from fe.triangle import Triangle

# constants
rho = 1000
P_a = 10 ** 5
W = 1
gamma = 0.002
g = 9.832
rho_a = 1.2754
x1, x2 = symbols('x_1 x_2')


def choise(element, number):
    N_i, N_j, N_k = element.get_basic_functions()

    # print("start")
    # print(element[1].number)
    # print(element[2].number)
    # print(element[3].number)
    # print(number)
    # print("fin")

    if element[1].number == number:
        return N_i
    elif element[2].number == number:
        return N_j
    elif element[3].number == number:
        return N_k
    else:
        return 0


def solve(mesh):
    M = mesh.quantity

    def system(vars, time):
        print('time=%s' % time)
        elements = mesh.splitting
        # vars = ones(3 * M, int)

        sys = np.zeros(shape=(3 * M))

        weight_functions = 0
        for element in elements:
            F_eq1 = 0
            F_eq2 = 0
            F_eq3 = 0
            for k in range(0, M):
                N_k = choise(element, k)
                for l in range(0, M):
                    W_l = choise(element, l)
                    # print(W_l)
                    weight_functions += W_l

                    F_eq1 += \
                        - element.integrate(W_l * diff(N_k, x1)) * vars[k] \
                        - element.integrate(W_l * diff(N_k, x2)) * vars[M + k] \
                        + element.integrate(diff(g * rho / 2 * N_k, x2) * W_l * N_k) * vars[2 * M + k] ** 2

                    F_eq2 += \
                        - element.integrate(P_a * W_l * diff(N_k, x1)) * vars[2 * M + k] \
                        + element.integrate(-W ** 2 * gamma ** 2 * rho_a * W_l) \
                        + element.integrate(diff(g * rho / 2 * N_k, x1) * W_l * N_k) * vars[2 * M + k] ** 2

                    F_eq3 += \
                        -element.integrate(P_a * W_l * diff(N_k, x2)) * vars[k]

                coeff_of_drvt_eq1 = element.integrate(rho * weight_functions * N_k)
                coeff_of_drvt_eq2 = element.integrate(weight_functions * N_k)
                coeff_of_drvt_eq3 = element.integrate(weight_functions * N_k)

                if coeff_of_drvt_eq2 != 0:
                    # print(F_eq2)
                    sys[k] += F_eq2 / coeff_of_drvt_eq2
                    # [x / coeff_of_drvt_eq2 for x in F_eq2]

                if coeff_of_drvt_eq3 != 0:
                    sys[M + k] += F_eq3 / coeff_of_drvt_eq3
                    # [x / coeff_of_drvt_eq3 for x in F_eq3]

                if coeff_of_drvt_eq1 != 0:
                    sys[2 * M + k] += F_eq1 / coeff_of_drvt_eq1
                    # [x / coeff_of_drvt_eq1 for x in F_eq1]

        # print('sys=%s' % sys)
        return sys

    t = np.linspace(0, 0.01, 2)
    y0 = np.array([0, 0, 0, 0, 0, 0])
    sol = odeint(system, y0, t)
    y1 = sol[:, 0]  # вектор значений решения
    y2 = sol[:, 1]  # вектор значений производной
    # print(y1)

    plt.figure(figsize=(6, 4), dpi=300)
    plt.plot(y1, t)
    plt.show()
