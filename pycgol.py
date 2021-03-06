#! /usr/bin/python3

"""
game of life program

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
import random
import utils
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from pygame.locals import (KEYDOWN, K_ESCAPE, K_q, QUIT)

@click.command()
@click.option("--res", default=5, help="grid resolution")
@click.option("--nts", default=10, help="number of time steps")
def main(res,nts):
    pygame.init()
    rows = res
    cols = res
    grid = np.zeros((rows,cols))
    ts = 0
    initialconditions(grid)
#   prettyprint(grid)
    display = pygame.display.set_mode((rows, cols))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q):
                running = False
            if event.type == pygame.QUIT:
                running = False
        if ts >= nts:
            running = False
        update(grid)
        ts += 1
        print(ts)
        new = grid*255
        pygame.surfarray.blit_array(display, new)
        pygame.display.flip()

    pygame.quit()

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
    maxrow = grid.shape[0]
    maxcol = grid.shape[1]
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            pr = i - 1     # previous row (using python negative indexing here)
            pc = j - 1     # previous col (using python negative indexing here)
            nr = (i + 1) % maxrow     # next row
            nc = (j + 1) % maxcol     # next col
            neighbors = origgrid[pr,pc]+origgrid[pr,j]+origgrid[pr,nc]+\
               origgrid[i,pc]+origgrid[i,nc]+\
               origgrid[nr,pc]+origgrid[nr,j]+origgrid[nr,nc]
#           neighbors = utils.count(origgrid,i,j)
#           calling function adds 15% to cputime???
            if grid[i,j] == 1:
                if neighbors <= 1 or neighbors >= 4:
                    grid[i,j] = 0
            else:
                if neighbors == 3:
                    grid[i,j] = 1


def initialconditions(grid):
    """set up the initial grid cells"""
    #oscillator(grid)
    randomstart(grid)


def randomstart(grid):
    """randomly placed 1s and 0s"""
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            grid[i,j] = random.randrange(2)


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
