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


def solve(mesh):
    M = mesh.quantity

    def system(vars, time):
        print('time=%s' % time)
        elements = mesh.splitting
        # vars = ones(3 * M, int)

        sys = np.zeros(shape=(3 * M))

        for element in elements:
            F_eq1 = 0
            F_eq2 = 0
            F_eq3 = 0
            for k in range(0, M):
                N_k = element.get_basic_function_by_number(k)
                weight_functions = 0
                for l in range(0, M):
                    W_l = element.get_basic_function_by_number(l)
                    weight_functions += W_l

                    F_eq1 += \
                        - element.integrate(W_l * diff(N_k, x1)) * vars[k] \
                        - element.integrate(W_l * diff(N_k, x2)) * vars[M + k]

                    F_eq2 += \
                        + element.integrate(W ** 2 * gamma ** 2 * rho_a * W_l) \
                        + element.integrate(P_a * W_l * diff(vars[2 * M + k] * N_k, x1)) \
                        + element.integrate(W_l * diff(-(P_a + g * (rho / 2) * vars[2 * M + k] * N_k) * vars[2 * M + k] * N_k, x1))

                    F_eq3 += \
                        - element.integrate(-P_a * W_l * diff(vars[2 * M + k] * N_k, x2)) \
                        + element.integrate(W_l * diff(-(P_a * vars[2 * M + k] * N_k - g * (rho / 2) * vars[2 * M + k] ** 2 * N_k ** 2), x2))

                coeff_of_drvt_eq1 = element.integrate(rho * weight_functions * N_k)
                coeff_of_drvt_eq2 = element.integrate(weight_functions * N_k)
                coeff_of_drvt_eq3 = element.integrate(weight_functions * N_k)

                if coeff_of_drvt_eq1 != 0:
                    sys[2 * M + k] += F_eq1 / coeff_of_drvt_eq1
                # [x / coeff_of_drvt_eq1 for x in F_eq1]

                if coeff_of_drvt_eq2 != 0:
                    sys[k] += F_eq2 / coeff_of_drvt_eq2
                # [x / coeff_of_drvt_eq2 for x in F_eq2]

                if coeff_of_drvt_eq3 != 0:
                    sys[M + k] += F_eq3 / coeff_of_drvt_eq3
                # [x / coeff_of_drvt_eq3 for x in F_eq3]

                print('sys=%s' % sys)
                print()
        return sys

    t = np.linspace(0, 0.4, 10)
    y0 = np.array([0, 0, 0, 0, 0, 0])
    sol = odeint(system, y0, t)

    y1 = sol[:, 0]
    y2 = sol[:, 1]

    print(sol)
    print(y1)
    #print(y1)
    #print(y2)
    print(t)

    plt.figure(figsize=(10, 10), dpi=1000)
    plt.xlabel('t')
    plt.ylabel('value')

    plt.plot(t, sol[:, 0], label='a_1')
    plt.plot(t, sol[:, 1], label='a_2')
    plt.plot(t, sol[:, 2], label='a_3')
    plt.plot(t, sol[:, 3], label='a_4')
    plt.plot(t, sol[:, 4], label='a_5')
    plt.plot(t, sol[:, 5], label='a_6')

    plt.show()
