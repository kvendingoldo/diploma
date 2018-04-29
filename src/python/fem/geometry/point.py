# -*- coding: utf-8 -*-
# @Author: Alexander Sharov


class Point(object):
    """
    The class Point represents a 2D point
    """

    @property
    def x(self):
        return float(self.points[0])

    @property
    def y(self):
        return float(self.points[1])

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, value):
        if value >= 0:
            self.__number = value
        else:
            raise ValueError()

    def set_x(self, value):
        self.points[0] = value

    def set_y(self, value):
        self.points[1] = value

    def __init__(self, *args, **kwargs):
        self.points = []
        s = len(args)
        if s is 0:
            if len(kwargs) > 0:
                if ("number" in kwargs) or ("coordinates" in kwargs):
                    number = kwargs.get("number", 0)
                    if number is not None:
                        self.number = int(number)
                    self.points = kwargs.get("coordinates", ())
        elif s is 2:
            self.points.append(float(args[0]))
            self.points.append(float(args[1]))
        elif s is 3:
            self.points.append(float(args[0]))
            self.points.append(float(args[1]))
            self.number = args[2]

    def __str__(self):
        return '(%g, %g)' % (self.x, self.y)

    def __repr__(self):
        return 'Point(%g, %g)' % (self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
