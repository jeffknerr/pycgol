#! /usr/bin/python3

"""
game of life program utilities

J. Knerr Fall 2021
"""

import numpy as np


def count(grid, row, col):
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
