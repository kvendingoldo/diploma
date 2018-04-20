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
    mesh = m.Mesh('/Users/ashraov/projects/study/diploma/resources/poly/pond_without_islands_4e.poly')
    #mesh = m.Mesh('/opt/diploma/resources/poly/lake_svetloyar.poly')
    mesh.generate()
    mesh.generate_contour()

    print(mesh.contour)
    print(mesh.splitting)
    print(mesh.raw_splitting)
    #mesh.show()
    #mesh.draw_contour()

    x1, x2 = symbols('x_1 x_2')
    time = np.linspace(3, 4, 2)
    q1, q2, H = fem.solve(time, mesh)

    print(time)



    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    v = np.array(q1[5][0])
    print(v)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(v[:,0],v[:,1],v[:,2])
    plt.show()

    #print(q2)
    #print(H)

    images_path = '/data/'
        #'/Users/ashraov/data/'

if __name__ == "__main__":
    main()
