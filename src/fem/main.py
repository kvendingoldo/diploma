# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

from data import mesh as m



#get_data()

#json2poly()

mesh = m.Mesh()

mesh.generate('/Users/ashraov/projects/study/diploma/resources/tmp.poly')

print(mesh.splitting)

mesh.show()

