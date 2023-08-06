import numpy as np
import scipy as sc
from scipy.optimize import linprog


def nash_equilibrium(a):
    n = len(a)

    row_min = []
    for i in range(0, n):
        row_min.append(np.min(a[i]))

    a_tr = sc.transpose(a)
    col_max = []
    for i in range(0, n):
        col_max.append(np.max(a_tr[i]))

    print(row_min)
    print(col_max)
    for i in range(0, n):
        for j in range(0, n):
            if (a[i][j] == row_min[i] and a[i][j] == col_max[j]):
                f = a[i][j]
                p = [0] * n
                p[i] = 1
                q = [0] * n
                q[j] = 1
                return {'f': f, 'p': p, 'q': q}

    add = 0
    if (np.min(a) < 0):
        add = -np.min(a)

    for i in range(0, n):
        for j in range(0, n):
            a[i][j] += add

    c = []
    for i in range(0, n):
        c.append(1)

    a_ub = [[0] * n for i in range(n + n)]
    b_ub = [0] * (n + n)
    for i in range(0, n):
        for j in range(0, n):
            a_ub[i][j] = -a[j][i]
        b_ub[i] = -1

        a_ub[n + i][i] = -1
        b_ub[n + i] = 0

    res = linprog(c, a_ub, b_ub)
    f = 1 / res.fun - add

    p = []
    for i in range(0, n):
        p.append(res.x[i] * res.fun)

    c = []
    for i in range(0, n):
        c.append(-1)

    a_ub = [[0] * n for i in range(n + n)]
    b_ub = [0] * (n + n)
    for i in range(0, n):
        for j in range(0, n):
            a_ub[i][j] = a[i][j]
        b_ub[i] = 1

        a_ub[n + i][i] = -1
        b_ub[n + i] = 0

    res = linprog(c, a_ub, b_ub)

    q = []
    for i in range(0, n):
        q.append(res.x[i] * -res.fun)

    return {'f': f, 'p': p, 'q': q}
