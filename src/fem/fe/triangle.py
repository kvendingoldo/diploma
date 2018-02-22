# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import numpy as np
from sympy import symbols

from geometry.point import Point


class Triangle(object):
    """
       The class Triangle represents a 2D triangle
       Class attributes:    points
       Instance attributes: vertexes
                            centroid
                            area

    """

    def __init__(self, *args, **kwargs):
        self.points = list()
        self.is_boundary = False

        s = len(args)
        if s is 3:
            for arg in args:
                if isinstance(arg, Point):
                    self.points.append(arg)
                else:
                    raise ValueError()
        else:
            self.points.append(Point())
            self.points.append(Point())
            self.points.append(Point())

    def __getitem__(self, index):
        if index == 1:
            return self.points[0]
        elif index == 2:
            return self.points[1]
        elif index == 3:
            return self.points[2]

    def __setitem__(self, index, value):
        if isinstance(value, Point):
            if index == 1:
                self.points[0] = value
            elif index == 2:
                self.points[1] = value
            elif index == 3:
                self.points[2] = value
        else:
            raise TypeError()

    @property
    def vertexes(self):
        return self.points

    @staticmethod
    def centroid(triangle):
        return Point(((triangle[1].x + triangle[2].x + triangle[3].x) / 3),
                     ((triangle[1].y + triangle[2].y + triangle[3].y) / 3))

    @property
    def centroid(self):
        return Point(((self[1].x + self[2].x + self[3].x) / 3),
                     ((self[1].y + self[2].y + self[3].y) / 3))

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
        return '((%g, %g), (%g, %g), (%g, %g))' % (self.points[0].x, self.points[0].y,
                                                   self.points[1].x, self.points[1].y,
                                                   self.points[2].x, self.points[2].y)

    def __repr__(self):
        return 'Triangle((%g, %g), (%g, %g), (%g, %g))' % (self.points[0].x, self.points[0].y,
                                                           self.points[1].x, self.points[1].y,
                                                           self.points[2].x, self.points[2].y)

    @property
    def area(self):
        a = np.sqrt((self[2].y - self[3].y) ** 2 + (self[2].x - self[3].x) ** 2)
        b = np.sqrt((self[1].y - self[3].y) ** 2 + (self[1].x - self[3].x) ** 2)
        c = np.sqrt((self[1].y - self[2].y) ** 2 + (self[1].x - self[2].x) ** 2)
        p = (a + b + c) / 2.0
        return np.sqrt(p * (p - a) * (p - b) * (p - c))

    @staticmethod
    def random():
        return Triangle((np.random.uniform(0, 1000), np.random.uniform(0, 1000)),
                        (np.random.uniform(0, 1000), np.random.uniform(0, 1000)),
                        (np.random.uniform(0, 1000), np.random.uniform(0, 1000)))
