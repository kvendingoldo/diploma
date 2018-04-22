# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import datetime

from data import mesh as m
from algorithm import fem
from data.plot import tri_plot
from utils import gif
from data.save import np_array
from data.plot import contour_lines as cs


DATA_DIR = '/Users/ashraov/data/%s' % datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")
#DATA_DIR = '/data/%s' % datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")

RESOURCES_DIR = '/Users/ashraov/projects/study/diploma/resources'
#RESOURCES_DIR = '/opt/diploma/resources'


def main():
    mesh = m.Mesh(RESOURCES_DIR + '/poly/lake_elton.poly')
    mesh.generate()
    mesh.generate_contour()

    #mesh.show()
    #mesh.draw_contour()

    # interval of integration (t0, tf)
    t_span = [1.9, 2]
    # times at which to store the computed solution, must be sorted and lie within t_span
    t_eval = [1.91, 1.99]

    q1, q2, H, psi1, psi2, raw_solution, times = fem.solve(t_span, t_eval, mesh)

    np_array.write(DATA_DIR, 'solution.txt', raw_solution)
    np_array.write(DATA_DIR, 'times.txt', times)

    surf_dir = '%s/surf' % DATA_DIR
    frame_dir = '%s/frame' % DATA_DIR

    # surface q1
    tri_plot.draw_3d_surf(surf_dir, 'q_1', q1, times)
    gif.create('%s/q_1' % surf_dir)
    # frame q1
    tri_plot.draw_3d_frame(frame_dir, 'q_1', q1, times)
    gif.create('%s/q_1' % frame_dir)

    # surface q2
    tri_plot.draw_3d_surf(surf_dir, 'q_2', q2, times)
    gif.create('%s/q_2' % surf_dir)
    # frame q2
    tri_plot.draw_3d_frame(frame_dir, 'q_2', q2, times)
    gif.create('%s/q_2' % frame_dir)

    # surface H
    tri_plot.draw_3d_surf(surf_dir, 'H', H, times)
    gif.create('%s/H' % surf_dir)
    # frame H
    tri_plot.draw_3d_frame(frame_dir, 'H', H, times)
    gif.create('%s/H' % frame_dir)

    # wave function psi1
    cs.draw_psi_2d(DATA_DIR, 'psi_1', psi1, times)
    gif.create('%s/psi_1' % DATA_DIR)

    # wave function psi2
    cs.draw_psi_2d(DATA_DIR, 'psi_2', psi2, times)
    gif.create('%s/psi_2' % DATA_DIR)


if __name__ == "__main__":
    main()
