#
# https://jonasteuwen.github.io/numpy/python/multiprocessing/2017/01/07/multiprocessing-numpy-array.html
#

import numpy as np
import itertools

X = np.random.random((100, 100)) #  A random 100x100 matrix
tmp = np.zeros((100, 100)) #  Placeholder


def fill_per_window(args):
    print(X)
    print(args)
    window_x, window_y = args

    for i in range(window_x, window_y + 2):
        for j in range(window_x, window_y + 2):
            tmp[i, j] = X[i, j]


window_idxs = [(i, j) for i, j in
               itertools.product(range(0, 100, 2), range(0, 100, 2))]

for idx in window_idxs:
    print(idx)
    fill_per_window(idx)

print(np.array_equal(X, tmp))
