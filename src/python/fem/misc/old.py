def calc(mesh):

    x1, x2, t = var('x1 x2 t', real=True)
    rho, rho_a, gamma, theta = symbols('rho rho_a gamma theta')
    f, W, g, c, Pa, h = symbols('f W g c Pa h')
    H, q1, q2 = symbols('H q1 q2')
    a_1, a_2 = symbols('a_1, a_2')

    eq1 = Derivative(q1, x1) + Derivative(q2, x2) + Derivative(rho * H, t)
    #eq2 = Derivative(q1, t) - (gamma**2 * rho_a * W**2 * cos(theta)) - Pa * Derivative(H, x1) - (rho * g * H) * Derivative(h, x1)
    #eq3 = Derivative(q2, t) - (gamma**2 * rho_a * W**2 * sin(theta)) - Pa * Derivative(H, x2) - (rho * g * H) * Derivative(h, x2)

    elements = mesh.splitting
    M = mesh.quantity


    # A * da/da + B * a + C = F
    A = np.zeros(shape=((3 * M)))
    B = np.zeros(shape=((3 * M), (3 * M)))
    C = np.zeros(shape=((3 * M)))
    F = np.zeros(shape=((3 * M)))

    for element in elements:
        N_i, N_j, N_k = element.get_basic_functions()
        for l in range(0, (3 * M)):
            for k in range(0, (3 * M)):
                if l < M:
                    A = 0
                    B = 0
                    C = 0
                    F = 0
                    # eq2
                elif l >= M and  l < 2 * M:
                    pass
                    # eq3
                else:
                    pass
                    # eq1







def dJ(u, v, p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    dxdu = ((1 - v) * x2 + v * x3 - x1)
    dxdv = (u * x3 - u * x2)
    dydu = ((1 - v) * y2 + v * y3 - y1)
    dydv = (u * y3 - u * y2)
    return np.abs(dxdu * dydv - dxdv * dydu)


def tridblquad(integrand, triangle):
    x1, y1 = triangle[1].x, triangle[1].y
    x2, y2 = triangle[2].x, triangle[2].y
    x3, y3 = triangle[3].x, triangle[3].y

    p1 = x1, y1
    p2 = x2, y2
    p3 = x3, y3
    # transformation to the unit square
    g = lambda u, v, c1, c2, c3: (1 - u) * c1 + u * ((1 - v) * c2 + v * c3)
    # transformation for the integrand,
    # including the Jacobian scaling factor
    def h( u, v ):
        x = g( u, v, x1, x2, x3 )
        y = g( u, v, y1, y2, y3 )
        I = integrand( x, y )
        I *= dJ( u, v, p1, p2, p3 )
        return I
    # perfrom the double integration using quadrature in the transformed space
    integral, error = integrate.dblquad( h, 0, 1, lambda x: 0, lambda x: 1, epsrel=1e-6, epsabs=0 )
    return integral, error


def integrate_by_triangle(func, triangle):
    x1, x2 = symbols('x_1 x_2')
    s = triangle.area
    c = triangle.centroid

    print(func.coeff(x1))

    integral_x1 = func.coeff(x1) * s * c.x
    integral_x2 = func.coeff(x2) * s * c.y
    integral_s = func.subs(x1, 0).subs(x2, 0) * s

    print(integral_x1)
    print(integral_x2)
    print(integral_s)

    print(Float(integral_s + integral_x1 + integral_x2))

    return Float(integral_s + integral_x1 + integral_x2)


# mesh = m.Mesh('/Users/ashraov/projects/study/diploma/resources/poly/pond_without_islands.poly.poly')
# mesh.generate()
# print(mesh.splitting)
# mesh.show()
# fem.system(0, 0, mesh)


tri = Triangle(Point(0, 0), Point(0, 1), Point(1, 1))
#x1, x2 = symbols('x_1 x_2')
#print(x1-(pow(x2,3)))
#print(integrate_by_triangle(x1-(pow(x2,3)), tri))
#print(tridblquad(exp(x1), tri))
area, error = tridblquad(lambda x, y: x-y**3, tri)
print(area)
