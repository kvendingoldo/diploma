x1, x2 = symbols('x_1 x_2')
tri = Triangle(Point(0, 0),Point(2, 0),Point(1, 1))


print(tri.integrate(x1 * x2))


#from fe.triangle import Triangle
#from geometry.point import Point

# x1, x2 = symbols('x_1 x_2')
#tri = Triangle(Point(0, 0), Point(2, 0), Point(1, 1))

#print(tri.basic_functions)

# print(tri.integrate(x1 * x2))
