# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

from data import mesh as m
from algorithm import fem

mesh = m.Mesh('/Users/ashraov/projects/study/diploma/resources/poly/pond_without_islands.poly.poly')
mesh.generate()

print(mesh.splitting)

#mesh.show()


#fem.calc(mesh)
