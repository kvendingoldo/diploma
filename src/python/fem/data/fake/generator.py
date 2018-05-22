# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

from random import randint

MIN_VAL = 0
MAX_VAL = 100


def gen_solution_vector(quantity_of_elements):
    solution = []
    for ind in range(0, 3 * quantity_of_elements):
        solution.append([randint(MIN_VAL, MAX_VAL) / randint(10000, 1000000)])
    return solution
