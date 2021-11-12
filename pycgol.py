#! /usr/bin/python3

"""
the game of life...

1 = alive
0 = dead

J. Knerr Fall 2021
"""

RED   = u"\033[1;31m"
BLUE  = u"\033[1;34m"
RESET = u"\033[0;0m"
CIRCLE = u"\u25CF"

RED_DISK = RED + CIRCLE + RESET
BLUE_DISK = BLUE + CIRCLE + RESET
RED_BORDER = RED + "-" + RESET
BLUE_BORDER = BLUE + "\\" + RESET

def print_char(i):
    if i > 0:
        return BLUE_DISK
    if i < 0:
        return RED_DISK
    return u'\u00B7' # empty cell


import numpy as np
import click

@click.command()
@click.option("--res", default=5, help="grid resolution")
@click.option("--nts", default=10, help="number of time steps")
def main(res,nts):
    rows = res
    cols = res
    grid = np.zeros((rows,cols))
    ts = 0
    initialconditions(grid)
    prettyprint(grid)
    while ts < nts:
        update(grid)
        ts += 1
        print("===> ", ts)
        prettyprint(grid)

def prettyprint(grid):
    """function to output board to screen"""
    for i in range(grid.shape[0]):
        line = ""
        for j in range(grid.shape[1]):
            if grid[i,j] == 0:
                line += BLUE_DISK
            else:
                line += RED_DISK
        print(line)



def update(grid):
    """update the grid according to the game rules"""
    # make a copy so we can update grid without affecting the live/dead calculations
    origgrid = np.copy(grid)                  
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            neighbors = count(origgrid,i,j)
#           print(i,j,grid[i,j],neighbors,"======")
            if grid[i,j] == 1:
                if neighbors <= 1 or neighbors >= 4:
                    grid[i,j] = 0
            else:
                if neighbors == 3:
                    grid[i,j] = 1

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


def initialconditions(grid):
    """set up the initial grid cells"""
    oscillator(grid)


def oscillator(grid):
    """line of 3 in the middle"""
    maxrow = grid.shape[0]
    maxcol = grid.shape[1]
    halfrow = int(maxrow/2)
    halfcol = int(maxcol/2)
    grid[halfrow,halfcol] = 1
    grid[halfrow+1,halfcol] = 1
    grid[halfrow-1,halfcol] = 1


if __name__ == '__main__':
    main()