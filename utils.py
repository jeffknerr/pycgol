#! /usr/bin/python3

"""
game of life program utilities

J. Knerr Fall 2021
"""

import numpy as np


def count(grid, row, col):
    """given a grid location, count and return number of alive neighbors"""
    maxrow = grid.shape[0]
    maxcol = grid.shape[1]
    pr = row - 1     # previous row (using python negative indexing here)
    pc = col - 1     # previous col (using python negative indexing here)
    nr = (row + 1) % maxrow     # next row
    nc = (col + 1) % maxcol     # next col
    return grid[pr,pc]+grid[pr,col]+grid[pr,nc]+\
            grid[row,pc]+grid[row,nc]+\
           grid[nr,pc]+grid[nr,col]+grid[nr,nc]



def npcount(grid, row, col):
    """given a grid location, count and return number of alive neighbors"""
    # https://stackoverflow.com/questions/54690743/compare-neighbours-boolean-numpy-array-in-grid
    rows = np.array([-1, -1, -1,  0,  0,  1,  1,  1])
    cols = np.array([-1,  0,  1, -1,  1, -1,  0,  1])
    # negative indeces work, but can't go past end of array??? need to wrap??
    maxrow = grid.shape[0]
    maxcol = grid.shape[1]
    for i in range(len(rows)):
        if rows[i] + row >= maxrow:
            rows[i] = rows[i] - maxrow   # manual wraparound
    for j in range(len(cols)):
        if cols[j] + col >= maxcol:
            cols[j] = cols[j] - maxcol   # manual wraparound
    return sum(grid[rows+row,cols+col])
    # note: this works, but is 6* slower than above count()
