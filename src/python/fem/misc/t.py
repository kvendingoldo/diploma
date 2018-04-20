a = ...

for t in time:
    q1_draw = list()

    for (x, y) in points:
        q1 = 0
        q2 = 0
        H = 0

        for element in elements:
            if (x, y) приналежит треугольнику:
                N_i, N_j, N_k = element.get_basic_functions()
                i, j, k = получить_номера_вершин()
                q1 += a[i][t] * N_i(x, y) + a[j][t] * N_j(x, y) + a[k][t] * N_k(x, y)
                q2 += a[i+M][t] * N_i(x, y) + a[j+M][t] * N_j(x, y) + a[k+M][t] * N_k(x, y)

        q1_draw.append([x, y, q1])


    # в момент времени t
    draw(q1_draw)
