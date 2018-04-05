# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

from data import mesh as m

mesh = m.Mesh('/Users/ashraov/projects/study/diploma/resources/poly/lake_superior.poly')
mesh.generate()
#print(mesh.splitting)
print(mesh.draw_contour())
#print(len(mesh.splitting))
#mesh.show()

