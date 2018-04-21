# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import simplejson
import os


def write(path, name, data):
    os.makedirs(path, exist_ok=True)
    with open(path + '/' + name, 'w') as the_file:
        simplejson.dump(data, the_file)
