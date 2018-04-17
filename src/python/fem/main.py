# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import numpy as np
import matplotlib

from sympy import symbols, lambdify
from sympy.plotting import plot3d

import matplotlib.pyplot as plt

from data import mesh as m
from algorithm import fem


def main():
    mesh = m.Mesh('/Users/ashraov/projects/study/diploma/resources/poly/pond_without_islands.poly')
    #mesh = m.Mesh('/Users/ashraov/projects/study/diploma/resources/poly/lake_svetloyar.poly')
    mesh.generate()
    #mesh.show()

    x1, x2 = symbols('x_1 x_2')
    time = np.linspace(3, 4, 2)
    q1, q2, H = fem.solve(time, mesh)


    print(time)
    print(q1)
    print(q2)
    print(H)

    plot3d(q1[1], (x1, -1, 1), (x2, -1, 1))
    plot3d(q2[1], (x1, -1, 1), (x2, -1, 1))
    plot3d(H[1], (x1, -1, 1), (x2, -1, 1))

    f1 = lambdify((x1, x2), q1[1], 'numpy')
    f2 = lambdify((x1, x2), q2[1], 'numpy')

    a = np.linspace(-7, 7, 1000)
    b = np.linspace(-5, 5, 1000)
    x, y = np.meshgrid(a, b)




    fig = plt.figure()
    ax = fig.gca()
    plt.grid()

    CS = matplotlib.pyplot.contour(x, y, f1(x, y))
    #CS = matplotlib.pyplot.contour(x, y, f2(x, y))
    plt.clabel(CS, fontsize=9, inline=10)
    plt.show()




if __name__ == "__main__":
    main()
