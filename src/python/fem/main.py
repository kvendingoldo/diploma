# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import numpy as np

from data import mesh as m
from algorithm import fem
from data.plot import tri_plot
from utils import gif

# DATA_DIR = '/Users/ashraov/data'
DATA_DIR = '/data/'

# RESOURCES_DIR = '/Users/ashraov/projects/study/diploma/resources'
RESOURCES_DIR = '/opt/diploma/resources'


def main():
    mesh = m.Mesh(RESOURCES_DIR + '/poly/pond_without_islands_4e.poly')
    mesh.generate()
    mesh.generate_contour()

    # mesh.show()
    # mesh.draw_contour()

    time = np.linspace(3, 4, 2)
    q1, q2, H, times = fem.solve(time, mesh)

    tri_plot.draw_3d_surf(DATA_DIR, 'q1', q1, times)
    #tri_plot.draw_3d_scatt(DATA_DIR, 'q1', q1, times)
    gif.create(DATA_DIR + '/q1')

    tri_plot.draw_3d_surf(DATA_DIR, 'q2', q2, times)
    #tri_plot.draw_3d_scatt(DATA_DIR, 'q2', q2, times)
    gif.create(DATA_DIR + '/q2')

    tri_plot.draw_3d_surf(DATA_DIR, 'H', H, times)
    #tri_plot.draw_3d_scatt(DATA_DIR, 'H', H, times)
    gif.create(DATA_DIR + '/H')


if __name__ == "__main__":
    main()
