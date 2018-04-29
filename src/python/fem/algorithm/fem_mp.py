# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

from sympy import *
from numpy import abs
from scipy.integrate import solve_ivp
from multiprocessing import Process, Manager

# from threading import Thread

# CONSTANTS
###############################################
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
# g / c^2
gc2 = 0.002
# коэффициент трения Шэззи [м^{1/2} * c^{-1}]
C = 40
# начальное возвышение
H0 = 0.01


class Solver(object):
    def __init__(self, mesh, t_span, t_eval):
        self.mesh = mesh
        self.M = mesh.quantity
        self.elements = mesh.splitting
        self.contour = mesh.contour
        self.t_span = t_span
        self.t_eval = t_eval

    def on_boundary(self, element, number):
        if element[1].number == number:
            x, y = element[1].x, element[1].y
        elif element[2].number == number:
            x, y = element[2].x, element[2].y
        elif element[3].number == number:
            x, y = element[3].x, element[3].y
        else:
            return False

        for point in self.contour:
            if (abs(float(point[0] - x)) < 1e-6) and (abs(float(point[1] - y)) < 1e-6):
                return True
        return False

    def calculate_element(self, sys_fun, element, variables):
        print('I am alive')

        x1, x2 = symbols('x_1 x_2')
        f_eq1 = 0
        f_eq2 = 0
        f_eq3 = 0
        for k in range(0, self.M):
            n_k = element.get_basic_function_by_number(k)
            weight_functions = 0
            print('I am still alive. [element=%s, k=%d]' % (str(element), k))
            for l in range(0, self.M):
                w_l = element.get_basic_function_by_number(l)
                weight_functions += w_l
                f_eq1 += \
                    + element.integrate(w_l * diff(
                        -P_a * H0 - P_a * variables[2 * self.M + k] * n_k - ((g * rho / 2) * H0 ** 2) - g * rho * H0 *
                        variables[2 * self.M + k] * n_k - g * rho / 2 * variables[2 * self.M + k] ** 2 * n_k ** 2, x1)) \
                    + element.integrate(P_a * w_l * diff(H0 + variables[2 * self.M + k] * n_k, x1)) \
                    + element.integrate(sqrt(2) / 2 * W ** 2 * gamma * rho_a * w_l) \
                    - element.integrate(
                        (gc2 * w_l * variables[k] / (rho * H0 ** 2) * variables[2 * self.M + k] ** 2 * n_k) * sqrt(
                            variables[k] ** 2 * n_k ** 2 + variables[self.M + k] ** 2 * n_k ** 2))

                f_eq2 += \
                    + element.integrate(w_l * diff(
                        -P_a * H0 - P_a * variables[2 * self.M + k] * n_k - ((g * rho / 2) * H0 ** 2) - g * rho * H0 *
                        variables[2 * self.M + k] * n_k - g * rho / 2 * variables[2 * self.M + k] ** 2 * n_k ** 2, x2)) \
                    + element.integrate(P_a * w_l * diff(H0 + variables[2 * self.M + k] * n_k, x2)) \
                    + element.integrate(sqrt(2) / 2 * W ** 2 * gamma * rho_a * w_l) \
                    - element.integrate(
                        (gc2 * w_l * variables[self.M + k] / (rho * H0 ** 2) * variables[
                            2 * self.M + k] ** 2 * n_k) * sqrt(
                            variables[k] ** 2 * n_k ** 2 + variables[self.M + k] ** 2 * n_k ** 2))

                f_eq3 += \
                    - element.integrate(w_l * diff(n_k, x1)) * variables[k] \
                    - element.integrate(w_l * diff(n_k, x2)) * variables[self.M + k]

            coefficient_of_d_eq1 = element.integrate(weight_functions * n_k)
            coefficient_of_d_eq2 = element.integrate(weight_functions * n_k)
            coefficient_of_d_eq3 = element.integrate(rho * weight_functions * n_k)

            if coefficient_of_d_eq1 != 0:
                if self.on_boundary(element, k):
                    sys_fun[k] = 0
                else:
                    sys_fun[k] = float((f_eq1.doit() / coefficient_of_d_eq1))

            if coefficient_of_d_eq2 != 0:
                if self.on_boundary(element, k):
                    sys_fun[self.M + k] = 0
                else:
                    sys_fun[self.M + k] = float((f_eq2.doit() / coefficient_of_d_eq2))

            if coefficient_of_d_eq3 != 0:
                if self.on_boundary(element, k):
                    sys_fun[2 * self.M + k] = 0
                else:
                    sys_fun[2 * self.M + k] = float((f_eq3.doit() / coefficient_of_d_eq3))

        print('I am dead')

    def system(self, time, variables):
        print('time = %s' % time)

        sys_fun = Manager().list([0] * (3 * self.M))
        tasks = []

        for element in self.elements:
            # thread = Thread(target=solve_element, args=(sys_fun, element, variables))
            process = Process(target=self.calculate_element, args=(sys_fun, element, variables))
            tasks.append(process)

        for task in tasks:
            task.start()

        for task in tasks:
            task.join()

        print('system of functions = %s\n' % sys_fun)

        return sys_fun

    def solve(self):
        # TODO: create time decorator for this function
        print('Number of elements = %d' % self.M)
        y0 = [0] * (3 * self.M)
        solution = solve_ivp(self.system,
                             y0=y0,
                             t_span=self.t_span,
                             t_eval=self.t_eval,
                             method='RK45',
                             rtol=1e-3,
                             atol=1e-3)

        print(solution.y)
        print(solution.t)

        return solution.y, solution.t
