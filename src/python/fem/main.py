# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import numpy as np
import datetime

from sympy import symbols, integrate
from sympy.plotting import plot3d

from data import mesh as m
from algorithm import fem
from misc import contour_lines as cl


def main():
    mesh = m.Mesh('/Users/ashraov/projects/study/diploma/resources/poly/pond_without_islands_4e.poly')
    #mesh = m.Mesh('/Users/ashraov/projects/study/diploma/resources/poly/lake_svetloyar.poly')
    mesh.generate()
    mesh.generate_contour()
    #mesh.show()
    #mesh.draw_contour()

    x1, x2 = symbols('x_1 x_2')
    time = np.linspace(3, 4, 1)
    q1, q2, H = fem.solve(time, mesh)

    print(time)
    print(q1)
    print(q2)
    print(H)

    images_path = '/Users/ashraov/projects/study/diploma/src/data/'

    for ind in range(0, len(q1)):
        date = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        if q1[ind] != 0:
            plot3d(q1[ind], (x1, 0, 3), (x2, 0, 3), show=False).save(images_path + 'q1_t=%s_%s.png' % (str(ind), date))
            cl.draw_2d(integrate(q1[ind], x2), images_path + 'contour_lines_q1_t=%s_%s.png' % (str(ind), date))

        if q2[ind] != 0:
            plot3d(q2[ind], (x1, 0, 3), (x2, 0, 3), show=False).save(images_path + 'q2_t=%s_%s.png' % (str(ind), date))
            cl.draw_2d(-integrate(q2[ind], x1), images_path + 'contour_lines_q2_t=%s_%s.png' % (str(ind), date))

        if H[ind] != 0:
            plot3d(H[ind], (x1, 0, 3), (x2, 0, 3), show=False).save(images_path + 'H_t=%s_%s.png' % (str(ind), date))


if __name__ == "__main__":
    main()
