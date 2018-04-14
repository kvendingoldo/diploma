# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

from data import mesh as m
from algorithm import fem

import matplotlib.pyplot as plt

from sympy import symbols, diff, integrate as sp_integrate
from sympy.parsing.sympy_parser import parse_expr

from geometry.point import Point
from fe.triangle import Triangle




x1, x2 = symbols('x_1 x_2')
tri = Triangle(Point(1, 0), Point(0, 0), Point(0, 1))


print(tri.integrate(x1 - x2 ** 3))
