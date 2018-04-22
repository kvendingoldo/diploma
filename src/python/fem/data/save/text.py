# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import json
import os


def write(path, name, data):
    os.makedirs(path, exist_ok=True)
    with open(path + '/' + name, 'w') as the_file:
        json.dump(data.tolist(), the_file)
