# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import numpy as np
import datetime
import matplotlib as plt

from sympy import symbols, integrate
from sympy.plotting import plot3d

from data import mesh as m
from algorithm import fem
from data.plot import contour_lines as cl

# This option needs for escaping 'RuntimeWarning: More than 20 figures have been opened'
plt.rcParams.update({'figure.max_open_warning': 0})

def main():
    #mesh = m.Mesh('/opt/diploma/resources/poly/pond_without_islands_4e.poly')
    #mesh = m.Mesh('/Users/ashraov/projects/study/diploma/resources/poly/pond_without_islands_4e.poly')
    mesh = m.Mesh('/opt/diploma/resources/poly/lake_svetloyar.poly')
    mesh.generate()
    mesh.generate_contour()

    print(mesh.contour)
    print(mesh.splitting)
    print(mesh.raw_splitting)
    mesh.show()
    #mesh.draw_contour()

    x1, x2 = symbols('x_1 x_2')
    time = np.linspace(3, 4, 2)
    q1, q2, H = fem.solve(time, mesh)

    print(time)
    print(q1)
    print(q2)
    print(H)

    images_path = '/data/'
        #'/Users/ashraov/data/'

    for ind in range(0, len(q1)):
        date = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        if q1[ind] != 0:
            plot3d(q1[ind], (x1, 45, 46), (x2, 56, 57), show=False).save(images_path + 'q1_t=%s_%s.png' % (str(ind), date))
            cl.draw_2d(integrate(q1[ind], x2), images_path + 'contour_lines_q1_t=%s_%s.png' % (str(ind), date))

        if q2[ind] != 0:
            plot3d(q2[ind], (x1, 45, 46), (x2, 56, 57), show=False).save(images_path + 'q2_t=%s_%s.png' % (str(ind), date))
            cl.draw_2d(-integrate(q2[ind], x1), images_path + 'contour_lines_q2_t=%s_%s.png' % (str(ind), date))

        if H[ind] != 0:
            plot3d(H[ind], (x1, 45, 46), (x2, 56, 57), show=False).save(images_path + 'H_t=%s_%s.png' % (str(ind), date))


if __name__ == "__main__":
    main()
