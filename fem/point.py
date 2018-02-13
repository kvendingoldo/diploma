# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import numpy as np


class Point(object):
    """
       The class Point represents a 2D point
       Class attributes:    points
       Instance attributes: x
                            y
                            number
    """

    @property
    def x(self):
        return self.points[0]

    @property
    def y(self):
        return self.points[1]

    def set_x(self, value):
        self.points[0] = value

    def set_y(self, value):
        self.points[1] = value

    def set_number(self, value):
        if value >= 0:
            self.number = value
        else:
            raise ValueError()

    def __init__(self, *args, **kwargs):
        self.points = np.zeros(shape=2)
        s = len(args)
        if s is 0:
            if len(kwargs) > 0:
                if ("number" in kwargs) or ("coordinates" in kwargs):
                    number = kwargs.get("number", 0)
                    if number is not None:
                        self.number = int(number)
                    self.points = kwargs.get("coordinates", ())
        elif s is 2:
            self.points[0] = args[0]
            self.points[1] = args[1]
        elif s is 3:
            self.points[0] = args[0]
            self.points[1] = args[1]
            self.number = args[2]

    def __str__(self):
        return '(%g, %g)' % (self.x, self.y)

    def __repr__(self):
        return 'Point(%g, %g)' % (self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
