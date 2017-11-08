# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import numpy as np
from sympy import symbols

from point import Point


class Triangle(object):
    def __init__(self, point_1=None, point_2=None, point_3=None):
        if point_1 is None:
            point_1 = Point()
        if point_2 is None:
            point_2 = Point()
        if point_3 is None:
            point_3 = Point()

        if isinstance(point_1, Point):
            self.point_1 = point_1
        else:
            raise ValueError()

        if isinstance(point_2, Point):
            self.point_2 = point_2
        else:
            raise ValueError()

        if isinstance(point_3, Point):
            self.point_3 = point_3
        else:
            raise ValueError()

    def __getitem__(self, index):
        if index == 1:
            return self.point_1
        elif index == 2:
            return self.point_2
        elif index == 3:
            return self.point_3

    def __setitem__(self, index, value):
        if isinstance(value, Point):
            if index == 1:
                self.point_1 = value
            elif index == 2:
                self.point_2 = value
            elif index == 3:
                self.point_3 = value
        else:
            raise TypeError()

    @property
    def vertexes(self):
        return [self.point_1, self.point_2, self.point_3]

    @staticmethod
    def centroid(triangle):
        return Point(((triangle[1].x + triangle[2].x + triangle[3].x)/3),
                     ((triangle[1].y + triangle[2].y + triangle[3].y)/3))

    @property
    def centroid(self):
        return Point(((self[1].x + self[2].x + self[3].x)/3),
                     ((self[1].y + self[2].y + self[3].y)/3))

    def get_basic_functions(self):
        A = [[self[1].x, self[1].y, 1],
             [self[2].x, self[2].y, 1],
             [self[3].x, self[3].y, 1]]

        x, y = symbols('x y')

        f = [1, 0, 0]
        solution = np.linalg.solve(A, f)
        basic_i = solution[0] * x + solution[1] * y + solution[2]

        f = [0, 1, 0]
        solution = np.linalg.solve(A, f)
        basic_j = solution[0] * x + solution[1] * y + solution[2]

        f = [0, 0, 1]
        solution = np.linalg.solve(A, f)
        basic_k = solution[0] * x + solution[1] * y + solution[2]

        return basic_i, basic_j, basic_k

    def __str__(self):
        return '((%g, %g), (%g, %g), (%g, %g))' % (self.point_1.x, self.point_1.y,
                                                   self.point_2.x, self.point_2.y,
                                                   self.point_3.x, self.point_3.y)

    def __repr__(self):
        return 'Triangle((%g, %g), (%g, %g), (%g, %g))' % (self.point_1.x, self.point_1.y,
                                                           self.point_2.x, self.point_2.y,
                                                           self.point_3.x, self.point_3.y)

    @property
    def area(self):
        a = np.sqrt((self[2].y - self[3].y)**2 + (self[2].x - self[3].x)**2)
        b = np.sqrt((self[1].y - self[3].y)**2 + (self[1].x - self[3].x)**2)
        c = np.sqrt((self[1].y - self[2].y)**2 + (self[1].x - self[2].x)**2)
        p = (a + b + c) / 2.0
        return np.sqrt(p * (p - a) * (p - b) * (p - c))

    @staticmethod
    def random():
        return Triangle((np.random.uniform(0, 1000), np.random.uniform(0, 1000)),
                        (np.random.uniform(0, 1000), np.random.uniform(0, 1000)),
                        (np.random.uniform(0, 1000), np.random.uniform(0, 1000)))
