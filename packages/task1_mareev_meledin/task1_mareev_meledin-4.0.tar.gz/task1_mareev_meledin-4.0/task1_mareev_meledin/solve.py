import numpy as np
from scipy.optimize import linprog


def nash_equilibrium(in_matrix):
    a = np.matrix(in_matrix)
    n = len(a)

    row_min = np.min(a, 1)
    col_max = np.max(a.T, 1)

    # Проверка игры на равновесие Нэша.
    for i in range(0, n):
        for j in range(0, n):
            if (a[i, j] == row_min[i] and a[i, j] == col_max[j]):
                p = np.zeros(n)
                q = np.zeros(n)
                p[i] = 1
                q[j] = 1
                return {'f': a[i, j], 'p': p.tolist(), 'q': q.tolist()}

    # Делаем так, чтобы минимальный элемент матрицы был неотрицательным.
    sub = min(0, np.min(a))
    a -= sub

    # Формулировка ЗЛП.
    c = np.ones(n)
    a_ub = np.vstack((-a.T, -np.identity(n)))
    b_ub = np.hstack((np.full(n, -1), np.zeros(n)))

    # Поиск спектра стратегии первого игрока и значения игры.
    res = linprog(c, a_ub, b_ub)
    f = 1 / res.fun + sub
    p = res.x * res.fun

    # Формулировка ЗЛП.
    c = np.full(n, -1)
    a_ub = np.vstack((a, -np.identity(n)))
    b_ub = np.hstack((np.ones(n), np.zeros(n)))

    # Поиск спектра стратегии второго игрока.
    res = linprog(c, a_ub, b_ub)
    q = res.x * -res.fun

    return {'f': f, 'p': p.tolist(), 'q': q.tolist()}
