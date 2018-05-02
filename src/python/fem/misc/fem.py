# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

from sympy import *
from numpy import array, abs, zeros
from scipy.integrate import solve_ivp
from time import sleep
import os
import threading
from multiprocessing import Process, Pool
from multiprocessing.pool import ThreadPool
from fe.triangle import Triangle
from geometry.point import Point

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
###############################################


class solver(object):

    def __init__(self, mesh, sysfun, variables):
        self.mesh = mesh
        self.sysfun = sysfun
        self.variables = variables

    def check_boundary(self, element, number):
        if element[1].number == number:
            x, y = element[1].x, element[1].y
        elif element[2].number == number:
            x, y = element[2].x, element[2].y
        elif element[3].number == number:
            x, y = element[3].x, element[3].y
        else:
            return False

        for point in self.mesh.contour:
            if (abs(float(point[0] - x)) < 1e-6) and (abs(float(point[1] - y)) < 1e-6):
                return True
        return False

    def solve_element(self, element):
        print('I am alive')
        x1, x2 = symbols('x_1 x_2')

        M = self.mesh.quantity
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
                    + element.integrate(W_l * diff(-P_a * H0 - P_a * self.variables[2 * M + k] * N_k - ((g * rho / 2) * H0 ** 2) - g * rho * H0 * self.variables[2 * M + k] * N_k - g * rho / 2 * self.variables[2 * M + k] ** 2 * N_k ** 2, x1)) \
                    + element.integrate(P_a * W_l * diff(H0 + self.variables[2 * M + k] * N_k, x1)) \
                    + element.integrate(sqrt(2) / 2 * W ** 2 * gamma * rho_a * W_l) \
                    - element.integrate((gc2 * W_l * self.variables[k] / (rho * H0 ** 2) * self.variables[2 * M + k] ** 2 * N_k) * sqrt(self.variables[k] ** 2 * N_k ** 2 + self.variables[M + k] ** 2 * N_k ** 2))

                f_eq2 += \
                    + element.integrate(W_l * diff(-P_a * H0 - P_a * self.variables[2 * M + k] * N_k - ((g * rho / 2) * H0 ** 2) - g * rho * H0 * self.variables[2 * M + k] * N_k - g * rho / 2 * self.variables[2 * M + k] ** 2 * N_k ** 2, x2)) \
                    + element.integrate(P_a * W_l * diff(H0 + self.variables[2 * M + k] * N_k, x2)) \
                    + element.integrate(sqrt(2) / 2 * W ** 2 * gamma * rho_a * W_l) \
                    - element.integrate((gc2 * W_l * self.variables[M + k] / (rho * H0 ** 2) * self.variables[2 * M + k] ** 2 * N_k) * sqrt(self.variables[k] ** 2 * N_k ** 2 + self.variables[M + k] ** 2 * N_k ** 2))

                f_eq3 += \
                    - element.integrate(W_l * diff(N_k, x1)) * self.variables[k] \
                    - element.integrate(W_l * diff(N_k, x2)) * self.variables[M + k]

            coefficient_of_d_eq1 = element.integrate(weight_functions * N_k)
            coefficient_of_d_eq2 = element.integrate(weight_functions * N_k)
            coefficient_of_d_eq3 = element.integrate(rho * weight_functions * N_k)

            if coefficient_of_d_eq1 != 0:
                if self.check_boundary(element, k):
                    self.sysfun[k] = 0
                else:
                    self.sysfun[k] = (f_eq1 / coefficient_of_d_eq1)

            if coefficient_of_d_eq2 != 0:
                if self.check_boundary(element, k):
                    self.sysfun[M + k] = 0
                else:
                    self.sysfun[M + k] = (f_eq2 / coefficient_of_d_eq2)

            if coefficient_of_d_eq3 != 0:
                if self.check_boundary(element, k):
                    self.sysfun[2 * M + k] = 0
                else:
                    self.sysfun[2 * M + k] = (f_eq3 / coefficient_of_d_eq3)
        print('I am dead')


def solve(t_span, t_eval, mesh):
    M = mesh.quantity
    print('Number of elements = %d' % M)
    elements = mesh.splitting

    def system(time, variables):
        print('time=%s' % time)
        sysfun = zeros(shape=(3 * M))

        element_solver = solver(mesh, sysfun, variables)

        # It's work
        #p = Process(target=element_solver.solve_element, args=(elements[0]))
        #p.start()
        #p.join()

        #print(elements)
        #print(elements[0])

        #pool = Pool(processes=2)


        #with Pool(processes=2) as pool:
        #with ThreadPool(processes=10) as pool:
            #pool.map(element_solver.solve_element, elements)
            #for element in elements:
            #    pool.apply_async(element_solver.solve_element, args=(element,))

        #pool = ThreadPool(processes=4)
        pool = Pool(processes=4, maxtasksperchild=2)
        #[pool.apply(element_solver.solve_element, args=(element,)) for element in elements]

        #from functools import partial
        #func = partial(element_solver.solve_element)

        pool.apply(element_solver.solve_element, elements)
        pool.close()
        pool.join()
        #pool.close()
        #pool.join()

        #import pickle
        #print(pickle.dumps(element_solver.solve_element))
        #print(elements)
        #return



        #threading.Thread(target=element_solver.solve_element, args=(element)).start()


        print('sysfun=%s\n' % element_solver.sysfun)
        return sysfun

    y0 = zeros(3 * M)
    solution = solve_ivp(system, t_span=t_span, y0=y0, method='RK45', t_eval=t_eval, rtol=1e-3, atol=1e-3)
    print(solution)
    a = solution.y
    times = solution.t

    q1_data = list()
    q2_data = list()
    H_data = list()

    psi1_data = list()
    psi2_data = list()

    for ind in range(0, len(times)):
        q1_plt = list()
        q2_plt = list()
        H_plt = list()

        # q1 = dψ/dx2
        psi1_plt = list()
        # q2 = - dψ/dx1
        psi2_plt = list()

        for point in mesh.points:
            x1, x2 = point[0], point[1]
            q1 = 0
            q2 = 0
            H = 0

            for element in elements:
                if element.contain(Point(x1, x2)):
                    i, j, k = element.vertices_number

                    sub = {
                        symbols('x_1'): x1,
                        symbols('x_2'): x2
                    }

                    N_i = (element.get_basic_function_by_number(i)).subs(sub)
                    N_j = (element.get_basic_function_by_number(j)).subs(sub)
                    N_k = (element.get_basic_function_by_number(k)).subs(sub)

                    q1 += a[i][ind] * N_i + a[j][ind] * N_j + a[k][ind] * N_k
                    q2 += a[i + M][ind] * N_i + a[j + M][ind] * N_j + a[k + M][ind] * N_k
                    H += a[i + 2 * M][ind] * N_i + a[j + 2 * M][ind] * N_j + a[k + 2 * M][ind] * N_k

            q1_plt.append([x1, x2, q1])
            q2_plt.append([x1, x2, q2])
            H_plt.append([x1, x2, H])

            psi1_plt.append([x1, x2, integrate(q1, x2).subs(Symbol('x_2'), x2)])
            psi2_plt.append([x1, x2, -integrate(q1, x1).subs(Symbol('x_1'), x1)])

        q1_data.append(array(q1_plt))
        q2_data.append(array(q2_plt))
        H_data.append(array(H_plt))

        psi1_data.append(array(psi1_plt))
        psi2_data.append(array(psi2_plt))

    return q1_data, q2_data, H_data, psi1_data, psi2_data, a, times
