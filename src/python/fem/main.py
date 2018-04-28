# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import datetime

from data import mesh as m
from algorithm import fem_old as fem
from data.plot import tri_plot
from utils import gif
from data.save import np_array
from data.plot import contour_lines as cs
from db import mongo

#DATA_DIR = '/Users/ashraov/data/%s' % datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")
DATA_DIR = '/data/%s' % datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")

#RESOURCES_DIR = '/Users/ashraov/projects/study/diploma/resources'
RESOURCES_DIR = '/opt/diploma/resources'

SURF_DIR = '%s/surf' % DATA_DIR
FRAME_DIR = '%s/frame' % DATA_DIR
WAVE_DIR = '%s/wave' % DATA_DIR
JSON_DIR = '%s/json' % DATA_DIR

MESH_TYPE = 'pqas.001D'
MESH_FILENAME = 'pond_without_islands_4e.poly'


def main():
    mesh = m.Mesh(RESOURCES_DIR + '/poly/%s' % MESH_FILENAME)
    mesh.generate(MESH_TYPE)
    mesh.generate_contour()

    #mesh.show()
    #mesh.draw_contour()

    # interval of integration (t0, tf)
    t_span = (1.90, 1.92)
    # times at which to store the computed solution, must be sorted and lie within t_span
    t_eval = [1.91]

    q1, q2, H, psi1, psi2, raw_solution, times = fem.solve(t_span, t_eval, mesh)

    np_array.write(JSON_DIR, 'solution.json', raw_solution)
    np_array.write(JSON_DIR, 'times.json', times)

    # surface q1
    tri_plot.draw_3d_surf(SURF_DIR, 'q_1', q1, times)
    gif.create('%s/q_1' % SURF_DIR)
    # frame q1
    tri_plot.draw_3d_frame(FRAME_DIR, 'q_1', q1, times)
    gif.create('%s/q_1' % FRAME_DIR)

    # surface q2
    tri_plot.draw_3d_surf(SURF_DIR, 'q_2', q2, times)
    gif.create('%s/q_2' % SURF_DIR)
    # frame q2
    tri_plot.draw_3d_frame(FRAME_DIR, 'q_2', q2, times)
    gif.create('%s/q_2' % FRAME_DIR)

    # surface H
    tri_plot.draw_3d_surf(SURF_DIR, 'H', H, times)
    gif.create('%s/H' % SURF_DIR)
    # frame H
    tri_plot.draw_3d_frame(FRAME_DIR, 'H', H, times)
    gif.create('%s/H' % FRAME_DIR)

    # wave function psi1
    cs.draw_psi_2d(WAVE_DIR, 'psi_1', psi1, times)
    gif.create('%s/psi_1' % WAVE_DIR)

    # wave function psi2
    cs.draw_psi_2d(WAVE_DIR, 'psi_2', psi2, times)
    gif.create('%s/psi_2' % WAVE_DIR)


if __name__ == "__main__":
    main()
