# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import numpy as np
from sympy import symbols, diff, integrate as sp_integrate
from sympy.parsing.sympy_parser import parse_expr

from geometry.point import Point


class Triangle(object):
    """
    The class Triangle represents a 2D triangle
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

        x1, x2 = symbols('x_1 x_2')

        f = [1, 0, 0]
        solution = np.linalg.solve(A, f)
        basic_i = solution[0] * x1 + solution[1] * x2 + solution[2]

        f = [0, 1, 0]
        solution = np.linalg.solve(A, f)
        basic_j = solution[0] * x1 + solution[1] * x2 + solution[2]

        f = [0, 0, 1]
        solution = np.linalg.solve(A, f)
        basic_k = solution[0] * x1 + solution[1] * x2 + solution[2]

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

    def integrate(self, func):
        def d_j(x1, x2):
            """Jacobian scaling factor"""
            u, v = symbols('u v')

            det_j = \
                + diff(x1, u) * diff(x2, v) \
                - diff(x1, v) * diff(x2, u)

            abs_det_j = parse_expr(str(det_j).replace('-', '+'), evaluate=False)

            return abs_det_j

        x1, y1 = self[1].x, self[1].y
        x2, y2 = self[2].x, self[2].y
        x3, y3 = self[3].x, self[3].y

        u, v = symbols('u v')

        # (x_1, x_2) is analogue of (x,y)
        x_1 = (1 - u) * x1 + u * ((1 - v) * x2 + v * x3)
        x_2 = (1 - u) * y1 + u * ((1 - v) * y2 + v * y3)

        #print('func=%s' % str(func))

        if func != 0:
            func = func.subs({symbols('x_1'): x_1,
                              symbols('x_2'): x_2})

        func *= d_j(x_1, x_2)
        return sp_integrate(func, (v, 0, 1), (u, 0, 1)).doit()
