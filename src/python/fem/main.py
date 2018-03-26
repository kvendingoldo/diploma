# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

from data import mesh as m

mesh = m.Mesh()
mesh.generate('/Users/ashraov/projects/study/diploma/resources/poly/lake_superior.poly')
print(mesh.splitting[0])
print(len(mesh.splitting))
mesh.show()

