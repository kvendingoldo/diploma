# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np

from sympy import symbols, diff, Float

from geometry.point import Point
from fe.triangle import Triangle



def boundary_condition_1(vertex):
    # TODO: Заменим на первое граничное условие, эта функция пока не актуальна
    if vertex.y == 0 or vertex.x == 0:
        return True
    else:
        return False


def boundary_condition_2(vertex):
    # TODO: Заменим на второе граничное условие, эта функция пока не актуальна
    if vertex.y == M or vertex.x == M:
        return True
    else:
        return False


def integrate_by_triangle(func, triangle):
    # TODO: нужно ли нам вообще интегрирование по треугольнику?
    x, y = symbols('x y')
    s = trianglelement.area

    integral_x = func.coeff(x) * s * Triangle.x(triangle.centroid())
    integral_y = func.coeff(y) * s * Triangle.y(triangle.centroid())
    integral_s = func.subs(x, 0).subs(y, 0) * s

    print(Float(integral_s + integral_x + integral_y))

    return Float(integral_s + integral_x + integral_y)


def main():

    # какой размер у матрицы?
    K = np.zeros(shape=((M + 1) ** 2, (M + 1) ** 2))
    f = np.zeros(shape=((M + 1) ** 2))

    # получим тут сетку
    elements = mesh()

    for element in elements:

        N_i, N_j, N_k = element.get_basic_functions()


        # все функции зависят от (x1, x2, t)

        x, y, t = symbols('x y t')

        q_1 = a_11(t) * N_i + a_12(t) * N_j + a_13(t) * N_k
        q_2 = a_21(t) * N_i + a_22(t) * N_j + a_23(t) * N_k
        H = a_31(t) * N_i + a_32(t) * N_j + a_33(t) * N_k

        nit_state = [1, 1]



    print(np.linalg.det(K))
    print(K)

    # TODO
    for element in elements:
        for vertex in element.vertexes:
            if boundary_condition_1(vertex):
                K[vertex.number] = np.zeros(shape=((M + 1) ** 2))
                K[vertex.number][vertex.number] = 1
                f[vertex.number] = 0
            elif boundary_condition_2(vertex):
                K[vertex.number] = np.zeros(shape=((M + 1) ** 2))
                K[vertex.number][vertex.number] = 1
                f[vertex.number] = 1

    solution = np.linalg.solve(K, f)

    print("K = ", K)
    print("f = ", f)
    print("a = ", solution)

    N = M + 1
    func = np.zeros(shape=(N, N))
    index = 0
    for i in range(0, N):
        for j in range(0, N):
            func[i][j] = solution[index]
            index += 1

    fig = plt.figure()
    ax = fig.gca()
    # ax.set_xticks(np.arange(0.1, M, 0.1))
    # ax.set_yticks(np.arange(0.1, M, 0.1))
    plt.grid()

    # Resample data grid by a factor of 3 using cubic spline interpolation
    # ndimage.zoom(func, 3)
    CS = plt.contour(func)
    plt.clabel(CS, fontsize=9, inline=10)
    plt.show()


if __name__ == '__main__':
    main()
