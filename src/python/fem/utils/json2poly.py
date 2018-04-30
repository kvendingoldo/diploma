# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import json


def json2poly(file):
    with open(file, 'r', encoding='utf8') as data_file:
        data = json.load(data_file)

    points = data['features'][0]['geometry']['coordinates'][0]
    print(points)
    count = len(points)

    print('%d 2 0 0' % count)

    for point, point_number in zip(points, range(len(points))):
        print('%d %g %g' % (point_number + 1, point[0], point[1]))

    print('%d 0' % count)

    for ind in range(count):
        if ind == count:
            print('%d %d 0' % (ind + 1, ind + 1))
        else:
            print('%d %d %d' % (ind + 1, ind + 1, ind + 2))

    print('1')
    print('1 0 0')
    print('0')


# TODO: delete it
json2poly('/Users/ashraov/projects/study/diploma/resources/json/lake_elton_new.json')
