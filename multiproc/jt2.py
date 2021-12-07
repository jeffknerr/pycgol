#
# https://jonasteuwen.github.io/numpy/python/multiprocessing/2017/01/07/multiprocessing-numpy-array.html
#
import numpy as np
import itertools
from multiprocessing import Pool #  Process pool
from multiprocessing import sharedctypes

rows = 10
cols = 5

X = np.random.random((rows, cols))
result = np.ctypeslib.as_ctypes(np.zeros((rows, cols)))
shared_array = sharedctypes.RawArray(result._type_, result)


def fill_per_window(args):
    row = args
    tmp = np.ctypeslib.as_array(shared_array)

    for j in range(cols):
        tmp[row, j] = X[row, j]

rowlist = list(range(rows))
print(rowlist)
for t in range(3):
    print("===== %d =====================" % t)
    print(X)
    p = Pool()
    res = p.map(fill_per_window, rowlist)
    result = np.ctypeslib.as_array(shared_array)
    print(np.array_equal(X, result))
    X = result + 1.5
