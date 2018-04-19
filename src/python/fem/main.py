# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import numpy as np

from sympy import symbols, integrate
from sympy.plotting import plot3d

from data import mesh as m
from algorithm import fem
from misc import contour_lines


#psi1 = lambdify((x1, x2), integrate(q1, x2), 'numpy')
#psi2 = lambdify((x1, x2), -integrate(q2, x1), 'numpy')


def main():
    #mesh = m.Mesh('/Users/ashraov/projects/study/diploma/resources/poly/pond_without_islands_2e.poly')
    mesh = m.Mesh('/Users/ashraov/projects/study/diploma/resources/poly/lake_svetloyar.poly')
    mesh.generate()
    mesh.generate_contour()
    #mesh.show()
    #mesh.draw_contour()

    x1, x2 = symbols('x_1 x_2')
    time = np.linspace(3, 4, 2)
    q1, q2, H = fem.solve(time, mesh)


    print(time)
    print(q1)
    print(q2)
    print(H)

    plot3d(q1[1], (x1, -100, 100), (x2, 0, 1))
    plot3d(q2[1], (x1, -100, 100), (x2, 0, 1))
    plot3d(H[1], (x1, -100, 100), (x2, 0, 1))

if __name__ == "__main__":
    main()
