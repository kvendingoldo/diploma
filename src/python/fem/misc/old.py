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


x1, x2 = symbols('x_1 x_2')
tri = Triangle(Point(0, 0),Point(2, 0),Point(1, 1))


print(tri.integrate(x1 * x2))
