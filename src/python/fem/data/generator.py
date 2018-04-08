# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import json
from numpy import pi, linspace, sin, cos


def json2poly():
    with open('/Users/ashraov/projects/study/diploma/resources/lake_baikal.json', 'r', encoding='utf8') as data_file:
        data = json.load(data_file)

    points = data['features'][0]['geometry']['coordinates'][0]
    print(points)
    count = len(points)

    print("%d 2 0 0" % count)

    for point, point_number in zip(points, range(len(points))):
        print("%d %g %g" % (point_number+1, point[0], point[1]))

    print("%d 0" % count)

    for ind in range(count):
        if ind == count:
            print("%d %d 0" % (ind+1, ind+1))
        else:
            print("%d %d %d" % (ind+1, ind+1, ind+2))

    print("1")
    print("1 0 0")
    print("0")


def polygon2poly():
    return NotImplementedError()


def circumference():
    radius = 50

    points = [(radius * cos(x), radius * sin(x)) for x in linspace(0, 2 * pi, 1000)]
    count = len(points)
    print("%d 2 0 0" % count)
    for point, point_number in zip(points, range(len(points))):
        print("%d %g %g" % (point_number+1, point[0], point[1]))

    print("%d 0" % count)

    for ind in range(count):
        if ind == count:
            print("%d %d 0" % (ind+1, ind+1))
        else:
            print("%d %d %d" % (ind+1, ind+1, ind+2))

    print("1")
    print("1 0 0")
    print("0")
