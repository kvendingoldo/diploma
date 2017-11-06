# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import numpy as np


class Point(object):
    def x(self):
        return self.point[0]

    def y(self):
        return self.point[1]

    def get_number(self):
        return self.number

    def set_x(self, value):
        self.point[0] = value

    def set_y(self, value):
        self.point[1] = value

    def set_number(self, value):
        if value >= 0:
            self.number = value
        else:
            raise ValueError()

    def __init__(self, *args, **kwargs):
        s = len(args)
        if s is 0:
            if len(kwargs) > 0:
                if ("number" in kwargs) or ("coordinates" in kwargs):
                    number = kwargs.get("number", 0.0)
                    if number is not None:
                        self.number = float(number)
                    self.point = np.zeros(shape=2)
                    self.point = kwargs.get("coordinates", ())
        elif s is 2:
            self.point = np.zeros(shape=2)
            self.point[0] = args[0]
            self.point[1] = args[1]
        else:
            self.point = np.zeros(shape=2)
            self.point[0] = 0
            self.point[1] = 0

    def __str__(self):
        return '(%g, %g)' % (self.point[0], self.point[1])

    def __repr__(self):
        return 'point(%g, %g)' % (self.point[0], self.point[1])

    def __eq__(self, other):
        return self.point[0] == other.x() and self.point[1] == other.y()
