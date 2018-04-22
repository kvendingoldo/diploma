# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import numpy as np

from data import mesh as m
from algorithm import fem
from data.plot import tri_plot
from utils import gif
from data.save import text

import profile


#DATA_DIR = '/Users/ashraov/data'
DATA_DIR = '/data'

#RESOURCES_DIR = '/Users/ashraov/projects/study/diploma/resources'
RESOURCES_DIR = '/opt/diploma/resources'


def main():
    mesh = m.Mesh(RESOURCES_DIR + '/poly/pond_without_islands_4e.poly')
    mesh.generate()
    mesh.generate_contour()

    #mesh.show()
    #mesh.draw_contour()

    time = np.linspace(3, 4, 2)
    q1, q2, H, psi1, psi2, raw_solution, times = fem.solve(time, mesh)

    text.write(DATA_DIR, 'solution.txt', raw_solution)
    text.write(DATA_DIR, 'times.txt', times)

    tri_plot.draw_3d_surf(DATA_DIR + '/surf', 'q1', q1, times)
    gif.create(DATA_DIR + '/surf/q1')
    tri_plot.draw_3d_scatt(DATA_DIR + '/scatt', 'q1', q1, times)
    gif.create(DATA_DIR + '/scatt/q1')

    tri_plot.draw_3d_surf(DATA_DIR + '/surf', 'q2', q2, times)
    gif.create(DATA_DIR + '/surf/q2')
    tri_plot.draw_3d_scatt(DATA_DIR + '/scatt', 'q2', q2, times)
    gif.create(DATA_DIR + '/scatt/q1')

    tri_plot.draw_3d_surf(DATA_DIR + '/surf', 'H', H, times)
    gif.create(DATA_DIR + '/surf/H')
    tri_plot.draw_3d_scatt(DATA_DIR + '/scatt', 'H', H, times)
    gif.create(DATA_DIR + '/scatt/H')


if __name__ == "__main__":
    # TODO: delete profiler and import
    profile.run('main()')
    #main()
