# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

from sympy import *
from numpy import array, abs, zeros
from scipy.integrate import solve_ivp

from geometry.point import Point
from fe.triangle import Triangle

# CONSTANTS
###########################
# плотность воды [кг / м^3]
rho = 1000
# плотность воздуха [кг / м^3]
rho_a = 1.2754
# давление на поверхности воды [Па]
P_a = 10 ** 5
# скорость ветра [м / c]
W = 1
# gamma ^ 2
gamma = 0.002
# ускорение свободного падения [м * c^2]
g = 9.832
# g / c^2
gc2 = 0.002
# коэффициент трения Шэззи [м^{1/2} * c^{-1}]
C = 40
# начальное возвышение
H0 = 0.01
###########################


def solve(time, mesh):
    M = mesh.quantity
    print('Number of elements = %d' % M)
    elements = mesh.splitting
    x1, x2 = symbols('x_1 x_2')

    def check_boundary(element, number):
        if element[1].number == number:
            x, y = element[1].x, element[1].y
        elif element[2].number == number:
            x, y = element[2].x, element[2].y
        elif element[3].number == number:
            x, y = element[3].x, element[3].y
        else:
            return False

        # print('x = %f, y = %f' % (x, y))

        for point in mesh.contour:
            if (abs(float(point[0] - x)) < 1e-6) and (abs(float(point[1] - y)) < 1e-6):
                return True
        return False

    def system(time, variables):
        print('time=%s' % time)
        sysfun = zeros(shape=(3 * M))

        for element in elements:
            f_eq1 = 0
            f_eq2 = 0
            f_eq3 = 0
            for k in range(0, M):
                N_k = element.get_basic_function_by_number(k)
                weight_functions = 0
                for l in range(0, M):
                    W_l = element.get_basic_function_by_number(l)
                    weight_functions += W_l

                    f_eq1 += \
                        + element.integrate(W_l * diff(-P_a * H0 - P_a * variables[2 * M + k] * N_k - ((g * rho / 2) * H0 ** 2) - g * rho * H0 *variables[2 * M + k] * N_k - g * rho / 2 * variables[2 * M + k] ** 2 * N_k ** 2, x1)) \
                        + element.integrate(P_a * W_l * diff(H0 + variables[2 * M + k] * N_k, x1)) \
                        + element.integrate(sqrt(2) / 2 * W ** 2 * gamma * rho_a * W_l) \
                        - element.integrate((gc2 * W_l * variables[k] / (rho * H0 ** 2) * variables[2 * M + k] ** 2 * N_k) * sqrt(variables[k] ** 2 * N_k ** 2 + variables[M + k] ** 2 * N_k ** 2))

                    f_eq2 += \
                        + element.integrate(W_l * diff(-P_a * H0 - P_a * variables[2 * M + k] * N_k - ((g * rho / 2) * H0 ** 2) - g * rho * H0 * variables[2 * M + k] * N_k - g * rho / 2 * variables[2 * M + k] ** 2 * N_k ** 2, x2)) \
                        + element.integrate(P_a * W_l * diff(H0 + variables[2 * M + k] * N_k, x2)) \
                        + element.integrate(sqrt(2) / 2 * W ** 2 * gamma * rho_a * W_l) \
                        - element.integrate((gc2 * W_l * variables[M + k] / (rho * H0 ** 2) * variables[2 * M + k] ** 2 * N_k) * sqrt(variables[k] ** 2 * N_k ** 2 + variables[M + k] ** 2 * N_k ** 2))

                    f_eq3 += \
                        - element.integrate(W_l * diff(N_k, x1)) * variables[k] \
                        - element.integrate(W_l * diff(N_k, x2)) * variables[M + k]

                coefficient_of_d_eq1 = element.integrate(weight_functions * N_k)
                coefficient_of_d_eq2 = element.integrate(weight_functions * N_k)
                coefficient_of_d_eq3 = element.integrate(rho * weight_functions * N_k)

                if coefficient_of_d_eq1 != 0:
                    if check_boundary(element, k):
                        sysfun[k] = 0
                    else:
                        sysfun[k] = (f_eq1 / coefficient_of_d_eq1)

                if coefficient_of_d_eq2 != 0:
                    if check_boundary(element, k):
                        sysfun[M + k] = 0
                    else:
                        sysfun[M + k] = (f_eq2 / coefficient_of_d_eq2)

                if coefficient_of_d_eq3 != 0:
                    if check_boundary(element, k):
                        sysfun[2 * M + k] = 0
                    else:
                        sysfun[2 * M + k] = (f_eq3 / coefficient_of_d_eq3)

        print('sysfun=%s\n' % sysfun)
        return sysfun

    y0 = zeros(3 * M)
    #solution = solve_ivp(system, time, y0, method='RK45', rtol=1e-3, atol=1e-3)

    #a = solution.y

    a = a = [[ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00,  2.70553197e-06,  2.97608516e-05,
     3.00314048e-04,  3.00584601e-03,  1.90182151e-02,
     2.70553197e-02],
   [ 0.00000000e+00,  3.24663838e-06,  3.57130538e-05,
     3.60409600e-04,  3.63986398e-03,  3.15429353e-02,
     6.56067708e-02],
   [ 0.00000000e+00,  3.78774484e-06,  4.16653038e-05,
     4.20554265e-04,  4.32314804e-03,  5.69885237e-02,
     1.49953542e-01],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00,  2.70553201e-06,  2.97609047e-05,
     3.00368619e-04,  3.06058788e-03,  3.34174470e-02,
     7.90478939e-02],
   [ 0.00000000e+00,  3.24663835e-06,  3.57130060e-05,
     3.60360487e-04,  3.59059083e-03,  1.84613195e-02,
     1.58961900e-02],
   [ 0.00000000e+00,  3.78774477e-06,  4.16652162e-05,
     4.20464224e-04,  4.23281746e-03,  3.30859353e-02,
     6.07751076e-02],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00, -4.05829795e-13, -4.91054191e-11,
    -5.00038391e-09, -5.02490952e-07, -2.37375659e-05,
    -7.02422840e-05],
   [ 0.00000000e+00, -2.43497877e-13, -2.94632535e-11,
    -3.00025360e-09, -3.01729625e-07, -1.48051267e-05,
    -4.72978444e-05],
   [ 0.00000000e+00,  6.08744692e-13,  7.36581296e-11,
     7.50058749e-09,  7.53853937e-07,  3.58838478e-05,
     1.07660784e-04],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
     0.00000000e+00]]

    print(a)

    #times = solution.t
    times = [3., 3.0001, 3.0011, 3.0111, 3.1111, 3.7029381, 4.]

    q1_data = list()
    q2_data = list()
    H_data = list()

    psi1_data = list()
    psi2_data = list()

    for ind in range(0, len(times)):
        q1_plt = list()
        q2_plt = list()
        H_plt = list()

        # q1 = dψ/dx2
        psi1_plt = list()
        # q2 = - dψ/dx1
        psi2_plt = list()

        for point in mesh.points:
            x, y = point[0], point[1]
            q1 = 0
            q2 = 0
            H = 0

            psi1 = 0
            psi2 = 0

            for element in elements:
                if element.contain(Point(x, y)):
                    i, j, k = element.vertices_number

                    sub = {
                        symbols('x_1'): x,
                        symbols('x_2'): y
                    }

                    N_i = (element.get_basic_function_by_number(i)).subs(sub)
                    N_j = (element.get_basic_function_by_number(j)).subs(sub)
                    N_k = (element.get_basic_function_by_number(k)).subs(sub)

                    q1 += a[i][ind] * N_i + a[j][ind] * N_j + a[k][ind] * N_k
                    q2 += a[i + M][ind] * N_i + a[j + M][ind] * N_j + a[k + M][ind] * N_k
                    H += a[i + 2 * M][ind] * N_i + a[j + 2 * M][ind] * N_j + a[k + 2 * M][ind] * N_k

            q1_plt.append([x, y, q1])
            q2_plt.append([x, y, q2])
            H_plt.append([x, y, H])

            psi1_plt.append([x, y, integrate(q1, x2).subs(Symbol('x_2'), y)])
            psi2_plt.append([x, y, -integrate(q1, x1).subs(Symbol('x_1'), x)])

        q1_data.append(array(q1_plt))
        q2_data.append(array(q2_plt))
        H_data.append(array(H_plt))

        psi1_data.append(array(psi1_plt))
        psi2_data.append(array(psi2_plt))

    return q1_data, q2_data, H_data, psi1_data, psi2_data, a, times
