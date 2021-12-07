

import numpy as np
from multiprocessing import Pool

def update(subgrid):
    print("update called with subgrid = ", subgrid)
    n = subgrid.shape[0]
    for i in range(n):
        subgrid[i] = subgrid[i]*2
    print(subgrid)
    return subgrid

if __name__ == '__main__':
    grid = np.zeros((15,10))
    grid[2,4] = 3
    grid[2,5] = 9
    print(grid)
    with Pool(5) as p:
        newrow = p.map(update, grid, grid.shape[0])
        print(newrow)
        # how to put them back into rows of grid???
    print(grid)
