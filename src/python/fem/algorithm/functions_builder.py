# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

from sympy import Symbol, symbols, integrate
from numpy import array

from geometry.point import Point


def get_functions(mesh, solution, times):
    elements = mesh.splitting
    points = mesh.points
    M = mesh.quantity

    q1_data = []
    q2_data = []
    H_data = []

    psi1_data = []
    psi2_data = []

    for ind in range(0, len(times)):
        q1_at_time = []
        q2_at_time = []
        H_at_time = []

        # q1 = d(psi)/dx2
        psi1_at_time = []

        # q2 = - d(psi)/dx1
        psi2_at_time = []

        for point in points:
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

                    n_i = (element.get_basic_function_by_number(i)).subs(sub)
                    n_j = (element.get_basic_function_by_number(j)).subs(sub)
                    n_k = (element.get_basic_function_by_number(k)).subs(sub)

                    q1 += solution[i][ind] * n_i + solution[j][ind] * n_j + solution[k][ind] * n_k
                    q2 += solution[i + M][ind] * n_i + solution[j + M][ind] * n_j + solution[k + M][ind] * n_k
                    H += solution[i + 2 * M][ind] * n_i + solution[j + 2 * M][ind] * n_j + solution[k + 2 * M][
                        ind] * n_k

            q1_at_time.append([x1, x2, q1])
            q2_at_time.append([x1, x2, q2])
            H_at_time.append([x1, x2, H])

            psi1_at_time.append([x1,x2,integrate(q1, Symbol('x_2')).subs(Symbol('x_2'),x2)])
            psi2_at_time.append([x1,x2,-integrate(q1, Symbol('x_1')).subs(Symbol('x_1'),x1)])

        q1_data.append(array(q1_at_time))
        q2_data.append(array(q2_at_time))
        H_data.append(array(H_at_time))

        psi1_data.append(array(psi1_at_time))
        psi2_data.append(array(psi2_at_time))

    return q1_data, q2_data, H_data, psi1_data, psi2_data
