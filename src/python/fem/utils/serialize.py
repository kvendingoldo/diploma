# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import pickle


def serialize(data):
    return pickle.dumps(data)


def deserialize(data):
    return pickle.loads(data)
