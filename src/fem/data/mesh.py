# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import matplotlib.pyplot as plt

from triangle import triangulate, plot as tplot

from fe.triangle import Triangle
from geometry.point import Point
from data.poly import read


DEFAULT_GRID = "pq20a.01D"


class Mesh(object):
    """
       The class Mesh represents a 2D mesh
       Class attributes:    raw_splitting
                            splitting
       Instance attributes: raw_splitting
                            splitting
    """

    def __init__(self, *args, **kwargs):
        self.raw_splitting = None
        self.splitting = list()

    def generate_raw(self, poly_file, step=DEFAULT_GRID):
        self.raw_splitting = triangulate(read(poly_file), step)

    def generate(self, poly_file, step=DEFAULT_GRID):
        self.generate_raw(poly_file, step)

        for triangle in self.raw_splitting['triangles']:
            tri = Triangle(*[Point(p[0], p[1]) for p in [self.raw_splitting['vertices'][v] for v in triangle]])
            tri.is_boundary = (sum([self.raw_splitting['vertex_markers'][v][0] for v in triangle]) >= 1)
            self.splitting.append(tri)

    def show(self):
        plt.figure(figsize=(8, 8))
        ax = plt.subplot(111, aspect='equal')
        tplot.plot(ax, **self.raw_splitting)
        plt.show()
