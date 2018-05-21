# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import json
import os


def write(directory, name, data):
    os.makedirs(directory, exist_ok=True)
    with open(directory + '/' + name, 'w') as the_file:
        json.dump(data.tolist(), the_file)
