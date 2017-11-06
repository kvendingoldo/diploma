# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import numpy as np
from sympy import symbols
from point import Point


class Triangle(object):
    def __init__(self, coordinate_1=None, coordinate_2=None, coordinate_3=None):
        if coordinate_1 is None:
            coordinate_1 = Point()
        if coordinate_2 is None:
            coordinate_2 = Point()
        if coordinate_3 is None:
            coordinate_3 = Point()

        if isinstance(coordinate_1, Point):
            self.coordinate_1 = coordinate_1
        else:
            raise ValueError()

        if isinstance(coordinate_2, Point):
            self.coordinate_2 = coordinate_2
        else:
            raise ValueError()

        if isinstance(coordinate_3, Point):
            self.coordinate_3 = coordinate_3
        else:
            raise ValueError()

    def __getitem__(self, index):
        if index == 1:
            return self.coordinate_1
        elif index == 2:
            return self.coordinate_2
        elif index == 3:
            return self.coordinate_3

    def vertexes(self):
        return [self.coordinate_1, self.coordinate_2, self.coordinate_3]

    @staticmethod
    def centroid(triangle):
        return Point(((triangle[1].x() + triangle[2].x() + triangle[3].x())/3),
                          ((triangle[1].y() + triangle[2].y() + triangle[3].y())/3))

    def centroid(self):
        return Point(((self[1].x() + self[2].x() + self[3].x())/3),
                          ((self[1].y() + self[2].y() + self[3].y())/3))

    def get_basic_functions(self):
        A = [[self[1].x(), self[1].y(), 1],
             [self[2].x(), self[2].y(), 1],
             [self[3].x(), self[3].y(), 1]]

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

    def __setitem__(self, index, value):
        if isinstance(value, Point):
            if index == 1:
                self.coordinate_one = value
            elif index == 2:
                self.coordinate_two = value
            elif index == 3:
                self.coordinate_three = value
        else:
            raise TypeError()

    def __str__(self):
        return '[(%g, %g), (%g, %g), (%g, %g)]' % (self.coordinate_1.x(), self.coordinate_1.y(),
                                                   self.coordinate_2.x(), self.coordinate_2.y(),
                                                   self.coordinate_3.x(), self.coordinate_3.y())

    def __repr__(self):
        return '[(%g, %g), (%g, %g), (%g, %g)]' % (self.coordinate_1.x(), self.coordinate_1.y(),
                                                   self.coordinate_2.x(), self.coordinate_2.y(),
                                                   self.coordinate_3.x(), self.coordinate_3.y())

    def area(self):
        a = np.sqrt((self[2].y() - self[3].y())**2 + (self[2].x() - self[3].x())**2)
        b = np.sqrt((self[1].y() - self[3].y())**2 + (self[1].x() - self[3].x())**2)
        c = np.sqrt((self[1].y() - self[2].y())**2 + (self[1].x() - self[2].x())**2)
        p = (a + b + c) / 2.0
        return np.sqrt(p * (p - a) * (p - b) * (p - c))

    def random(self):
        self[1] = (np.random.uniform(0, 1000), np.random.uniform(0, 1000))
        self[2] = (np.random.uniform(0, 1000), np.random.uniform(0, 1000))
        self[3] = (np.random.uniform(0, 1000), np.random.uniform(0, 1000))

    @staticmethod
    def random():
        return Triangle((np.random.uniform(0, 1000), np.random.uniform(0, 1000)),
                        (np.random.uniform(0, 1000), np.random.uniform(0, 1000)),
                        (np.random.uniform(0, 1000), np.random.uniform(0, 1000)))
