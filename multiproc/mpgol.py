"""
gol using multiprocessing

J. Knerr
Dec 2021
"""

#
# https://jonasteuwen.github.io/numpy/python/multiprocessing/2017/01/07/multiprocessing-numpy-array.html
#
import numpy as np
from multiprocessing import Pool 
from multiprocessing import sharedctypes

rows = 10
cols = 6

grid = np.zeros((rows, cols))
grid[0,0]=1
grid[0,1]=1
grid[0,2]=1
grid[3,3]=1
grid[3,4]=1
grid[3,5]=1
result = np.ctypeslib.as_ctypes(np.zeros((rows, cols)))
shared_array = sharedctypes.RawArray(result._type_, result)

def update(row):
    """update one row"""
    tmp = np.ctypeslib.as_array(shared_array)
    for j in range(cols):
        col = j
        #tmp[row, j] = grid[row, j]
        #tmp[row, j] = -1 * grid[row,j]
        pr = row - 1
        pc = col - 1
        nr = (row + 1) % rows 
        nc = (col + 1) % cols
        neighbors = grid[pr, pc] + grid[pr, col] + grid[pr, nc] + \
            grid[row, pc] + grid[row, nc] + \
            grid[nr, pc] + grid[nr, col] + grid[nr, nc]
        print(row, j, neighbors)
        if grid[row, j] == 1:
            if neighbors <= 1 or neighbors >= 4:
                tmp[row, j] = 0
        else:
            if neighbors == 3:
                tmp[row, j] = 1

def main():
    global grid

    print(grid)
    for i in range(2):
        print("=============================>", i)
        rowlist = list(range(rows))
        p = Pool()
        res = p.map(update, rowlist)
        result = np.ctypeslib.as_array(shared_array)
        print(result)
        grid = result
        #print(np.array_equal(grid, result))
        print("-----------------------------")

main()
