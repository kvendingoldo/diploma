import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from sympy import integrate, symbols, diff, Float
from scipy import ndimage


M = 10
A = 0
B = 0
C = 1


def mesh():
    x, y = np.meshgrid(np.arange(M + 1), np.arange(M + 1))
    x = x.flatten()
    y = y.flatten()
    triangulation = tri.Triangulation(x, y)
    triangles = triangulation.triangles
    number_of_triangles = triangles.shape[0]
    vertexes = np.vstack((triangulation.x, triangulation.y)).T
    # number of vertexes and elements
    N = vertexes.shape[0]
    E = triangles.shape[0]

    matrix_of_triangles = list()

    for triangle in triangles:
        tmp = list()
        for vertex in triangle:
            tmp.append((vertex, vertexes[vertex]))
        matrix_of_triangles.append(tmp)

    #plt.triplot(triangulation)
    #plt.show()

    return matrix_of_triangles, number_of_triangles


def boundary_condition_1(vertex):
    if vertex[1] == 0 or vertex[0] == 0:
        return True
    else:
        return False


def boundary_condition_2(vertex):
    if vertex[1] == M or vertex[0] == M:
        return True
    else:
        return False


def area_of_triangle(triangle):
    a = np.sqrt((triangle[1][1][0] - triangle[0][1][0]) ** 2 + (triangle[1][1][1] - triangle[0][1][1]) ** 2)
    b = np.sqrt((triangle[2][1][0] - triangle[1][1][0]) ** 2 + (triangle[2][1][1] - triangle[1][1][1]) ** 2)
    c = np.sqrt((triangle[0][1][0] - triangle[2][1][0]) ** 2 + (triangle[0][1][1] - triangle[2][1][1]) ** 2)
    p = (a + b + c) / 2.0
    return np.sqrt(p * (p - a) * (p - b) * (p - c))


def get_basis_functions(triangle):
    A = [[triangle[0][1][0], triangle[0][1][1], 1],
         [triangle[1][1][0], triangle[1][1][1], 1],
         [triangle[2][1][0], triangle[2][1][1], 1]]

    x, y = symbols('x y')

    f = [1, 0, 0]
    solution = np.linalg.solve(A, f)
    N_i = solution[0] * x + solution[1] * y + solution[2]

    f = [0, 1, 0]
    solution = np.linalg.solve(A, f)
    N_j = solution[0] * x + solution[1] * y + solution[2]

    f = [0, 0, 1]
    solution = np.linalg.solve(A, f)
    N_k = solution[0] * x + solution[1] * y + solution[2]

    return N_i, N_j, N_k


def integrate_by_triangle(func, triangle):
    x, y = symbols('x y')
    s = area_of_triangle(triangle)

    # коэффициент при x * прощадь треугольника * (x_i + x_j + x_k)
    integral_x = func.coeff(x) * s/3 * (triangle[0][1][0] + triangle[1][1][0] + triangle[2][1][0])
    # коэффициент при y * прощадь треугольника * (y_i + y_j + y_k)
    integral_y = func.coeff(y) * s/3 * (triangle[0][1][1] + triangle[1][1][1] + triangle[2][1][1])
    # коэффициент при константе * прощадь треугольника
    integral_s = func.subs(x, 0).subs(y, 0) * s

    print(Float(integral_s + integral_x + integral_y))

    return Float(integral_s + integral_x + integral_y)


def main():
    K = np.zeros(shape=((M + 1) ** 2, (M + 1) ** 2))

    f = np.zeros(shape=((M + 1) ** 2))

    fe, number_of_fe = mesh()

    for e in fe:

        N_i, N_j, N_k = get_basis_functions(e)
        x, y = symbols('x y')

        for l in range(0, (M + 1) ** 2):

            if e[0][0] == l:
                f[l] = integrate_by_triangle(C * N_i, e)
            elif e[1][0] == l:
                f[l] = integrate_by_triangle(C * N_j, e)
            elif e[2][0] == l:
                f[l] = integrate_by_triangle(C * N_k, e)

            for m in range(0, (M + 1) ** 2):

                if e[0][0] == l:
                    if e[0][0] == m:
                        K[l][m] += (diff(N_i, x) * diff(N_i, x) + diff(N_i, y) + diff(N_i, y)) * area_of_triangle(e)
                    elif e[1][0] == m:
                        K[l][m] += (diff(N_i, x) * diff(N_j, x) + diff(N_i, y) + diff(N_j, y)) * area_of_triangle(e)
                    elif e[2][0] == m:
                        K[l][m] += (diff(N_i, x) * diff(N_k, x) + diff(N_i, y) + diff(N_k, y)) * area_of_triangle(e)

                elif e[1][0] == l:
                    if e[0][0] == m:
                        K[l][m] += (diff(N_j, x) * diff(N_i, x) + diff(N_j, y) + diff(N_i, y)) * area_of_triangle(e)
                    elif e[1][0] == m:
                        K[l][m] += (diff(N_j, x) * diff(N_j, x) + diff(N_j, y) + diff(N_j, y)) * area_of_triangle(e)
                    elif e[2][0] == m:
                        K[l][m] += (diff(N_j, x) * diff(N_k, x) + diff(N_j, y) + diff(N_k, y)) * area_of_triangle(e)

                elif e[2][0] == l:
                    if e[0][0] == m:
                        K[l][m] += (diff(N_k, x) * diff(N_i, x) + diff(N_k, y) + diff(N_i, y)) * area_of_triangle(e)
                    elif e[1][0] == m:
                        K[l][m] += (diff(N_k, x) * diff(N_j, x) + diff(N_k, y) + diff(N_j, y)) * area_of_triangle(e)
                    elif e[2][0] == m:
                        K[l][m] += (diff(N_k, x) * diff(N_k, x) + diff(N_k, y) + diff(N_k, y)) * area_of_triangle(e)
                else:
                    K[l][m] += 0

    print(np.linalg.det(K))
    print(K)

    for e in fe:
        for vertex in e:
            if boundary_condition_1(vertex[1]):
                K[vertex[0]] = np.zeros(shape=((M + 1) ** 2))
                K[vertex[0]][vertex[0]] = 1
                f[vertex[0]] = 0
            elif boundary_condition_2(vertex[1]):
                K[vertex[0]] = np.zeros(shape=((M + 1) ** 2))
                K[vertex[0]][vertex[0]] = 1
                f[vertex[0]] = 1

    solution = np.linalg.solve(K, f)

    print("K = ", K)
    print("f = ", f)
    print("a = ", solution)

    N = M + 1
    func = np.zeros(shape=(N, N))
    index = 0
    for i in range(0, N):
        for j in range(0, N):
            func[i][j] = solution[index]
            index += 1

    fig = plt.figure()
    ax = fig.gca()
    #ax.set_xticks(np.arange(0.1, M, 0.1))
    #ax.set_yticks(np.arange(0.1, M, 0.1))
    plt.grid()

    # Resample data grid by a factor of 3 using cubic spline interpolation
    # ndimage.zoom(func, 3)
    CS = plt.contour(func)
    plt.clabel(CS, fontsize=9, inline=10)
    plt.show()


if __name__ == '__main__':
    main()
