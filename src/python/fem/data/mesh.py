# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import matplotlib.pyplot as plt

from triangle import triangulate, plot as tplot

from fe.triangle import Triangle
from geometry.point import Point
from data.poly import read_tri, read_pts
from data.plot.poly_contour import plot as dplot

DEFAULT_GRID = 'pqas.001D'


class Mesh(object):
    """
    The class Mesh represents a 2D mesh
    """

    def __init__(self, file):
        self.raw_file = file
        self.raw_splitting = None
        self.splitting = list()
        self.contour = list()

    def generate_raw(self, step=DEFAULT_GRID):
        self.raw_splitting = triangulate(read_tri(self.raw_file), step)

    def generate(self, step=DEFAULT_GRID):
        self.generate_raw(step)

        for triangle in self.raw_splitting['triangles']:
            points = list()
            for v in triangle:
                point = Point(*self.raw_splitting['vertices'][v])
                point.number = v
                points.append(point)
            tri = Triangle(*points)
            tri.is_boundary = (sum([self.raw_splitting['vertex_markers'][v][0] for v in triangle]) >= 1)
            self.splitting.append(tri)

    def generate_contour(self):
        for vertex, vertex_matrix in zip(self.raw_splitting['vertices'], self.raw_splitting['vertex_markers']):
            if vertex_matrix == 1:
                self.contour.append(vertex)

    def show(self):
        plt.figure(figsize=(8, 8))
        ax = plt.subplot(111, aspect='equal')
        tplot.plot(ax, **self.raw_splitting)
        plt.show()

    @property
    def quantity(self):
        return len(self.splitting)

    @property
    def points(self):
        return self.raw_splitting['vertices']

    def draw_contour(self):
        plt.figure(figsize=(8, 8))
        ax = plt.subplot(111, aspect='equal')
        dplot(ax, **self.raw_splitting)
        plt.show()
