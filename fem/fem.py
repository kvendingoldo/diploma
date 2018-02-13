# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import matplotlib

matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np

from sympy import symbols, diff, Float

from point import Point
from triangle import Triangle

M = 3
A = 1
B = 1
C = 1


def mesh():
    x, y = np.meshgrid(np.arange(M + 1), np.arange(M + 1))
    x = x.flatten()
    y = y.flatten()

    triangulation = tri.Triangulation(x, y)
    triangles = triangulation.triangles
    # triangles_quantity = triangles.shape[0]
    vertexes = np.vstack((triangulation.x, triangulation.y)).T
    # triangles_vertexes_quantity = vertexes.shape[0]

    matrix_of_triangles = list()

    for triangle in triangles:
        p1 = Point(vertexes[triangle[0]][0], vertexes[triangle[0]][1])
        p1.set_number(triangle[0])
        p2 = Point(vertexes[triangle[1]][0], vertexes[triangle[1]][1])
        p2.set_number(triangle[1])
        p3 = Point(vertexes[triangle[2]][0], vertexes[triangle[2]][1])
        p3.set_number(triangle[2])
        matrix_of_triangles.append(Triangle(p1, p2, p3))

    # plt.triplot(triangulation)
    # plt.show()

    return matrix_of_triangles


def boundary_condition_1(vertex):
    if vertex.y == 0 or vertex.x == 0:
        return True
    else:
        return False


def boundary_condition_2(vertex):
    if vertex.y == M or vertex.x == M:
        return True
    else:
        return False


def integrate_by_triangle(func, triangle):
    # TODO: incorrect function
    x, y = symbols('x y')
    s = trianglelement.area

    integral_x = func.coeff(x) * s * Triangle.x(triangle.centroid())
    integral_y = func.coeff(y) * s * Triangle.y(triangle.centroid())
    integral_s = func.subs(x, 0).subs(y, 0) * s

    print(Float(integral_s + integral_x + integral_y))

    return Float(integral_s + integral_x + integral_y)


def main():
    K = np.zeros(shape=((M + 1) ** 2, (M + 1) ** 2))

    f = np.zeros(shape=((M + 1) ** 2))

    elements = mesh()

    for element in elements:

        N_i, N_j, N_k = element.get_basic_functions()

        x, y = symbols('x y')

        for l in range(0, (M + 1) ** 2):

            f[l] = 0
            # if element[0][0] == l:
            #    f[l] = integrate_by_triangle(C * N_i, element)
            # elif element[1][0] == l:
            #    f[l] = integrate_by_triangle(C * N_j, element)
            # elif element[2][0] == l:
            #    f[l] = integrate_by_triangle(C * N_k, element)

            for m in range(0, (M + 1) ** 2):

                if element[1].number == l:
                    if element[1].number == m:
                        K[l][m] += (diff(N_i, x) * diff(N_i, x) + diff(N_i, y) + diff(N_i, y)) * element.area
                    elif element[2].number == m:
                        K[l][m] += (diff(N_i, x) * diff(N_j, x) + diff(N_i, y) + diff(N_j, y)) * element.area
                    elif element[3].number == m:
                        K[l][m] += (diff(N_i, x) * diff(N_k, x) + diff(N_i, y) + diff(N_k, y)) * element.area

                elif element[2].number == l:
                    if element[1].number == m:
                        K[l][m] += (diff(N_j, x) * diff(N_i, x) + diff(N_j, y) + diff(N_i, y)) * element.area
                    elif element[2].number == m:
                        K[l][m] += (diff(N_j, x) * diff(N_j, x) + diff(N_j, y) + diff(N_j, y)) * element.area
                    elif element[3].number == m:
                        K[l][m] += (diff(N_j, x) * diff(N_k, x) + diff(N_j, y) + diff(N_k, y)) * element.area

                elif element[3].number == l:
                    if element[1].number == m:
                        K[l][m] += (diff(N_k, x) * diff(N_i, x) + diff(N_k, y) + diff(N_i, y)) * element.area
                    elif element[2].number == m:
                        K[l][m] += (diff(N_k, x) * diff(N_j, x) + diff(N_k, y) + diff(N_j, y)) * element.area
                    elif element[3].number == m:
                        K[l][m] += (diff(N_k, x) * diff(N_k, x) + diff(N_k, y) + diff(N_k, y)) * element.area
                else:
                    K[l][m] += 0

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
