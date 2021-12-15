#! /usr/bin/python3
"""
version of pycgol.py that uses multiprocessing

algorithm: given N rows and M processors, send N/M to each processor
example: 100 rows, 2 processors, send 50 rows to each processor

J. Knerr
Dec 2021
"""

# this one really helped me understand shared memory:
# https://stackoverflow.com/questions/34824382/sharing-numpy-arrays-between-multiple-processes-without-inheritance

import time
import random
import multiprocessing as mp
from multiprocessing import shared_memory
import numpy as np
import click
import pygame
from pygame.locals import (KEYDOWN, K_ESCAPE, K_q)
# stop the "welcome to pygame" message from being displayed
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


@click.command()
@click.option("--res", default=18, help="grid resolution")
@click.option("--nts", default=10, help="number of time steps")
@click.option("--procs", default=2,
              help="num of processors to use (e.g., 1, 2, 4)")
def main(res, nts, procs):
    """main function for mp app"""
    if res < 1:
        res = 10
    if nts < 1:
        nts = 10
    if procs not in [1, 2, 4, 8]:
        procs = 2
    rows = res
    cols = res
    grid = np.zeros((rows, cols))
    oldgrid = np.zeros((rows, cols))
    initrandom(grid)
    oldgrid[:] = grid[:]
    shm = shared_memory.SharedMemory(create=True, size=grid.nbytes)
    shgrid = np.ndarray(grid.shape, dtype=grid.dtype, buffer=shm.buf)
    shgrid[:] = grid[:]
    shm2 = shared_memory.SharedMemory(create=True, size=oldgrid.nbytes)
    sholdgrid = np.ndarray(oldgrid.shape, dtype=oldgrid.dtype, buffer=shm2.buf)
    sholdgrid[:] = oldgrid[:]

    pygame.init()
    pgdisplay = pygame.display.set_mode((rows, cols))

    step = int(rows/procs) + 1
    timestep = 0
    display(pgdisplay, shgrid, timestep)
    tstart = time.time()
    running = True
    while running:
        # check for quit early
        for event in pygame.event.get():
            if event.type == KEYDOWN and \
              (event.key == K_ESCAPE or event.key == K_q):
                running = False
            if event.type == pygame.QUIT:
                running = False
        # send grid and row start/end to processors
        start = 0
        aprocs = []
        while start < rows:
            end = (start + step)
            if end > rows:
                end = rows
            p = mp.Process(target=update,
                    args=(shgrid, sholdgrid, start, end, cols))
            p.start()
            aprocs.append(p)
            start = end
        # wait for them all to finish
        for p in aprocs:
            p.join()
        timestep += 1
        display(pgdisplay, shgrid, timestep)
        if timestep >= nts:
            running = False
        # copy to oldgrid to set up for next time step
        sholdgrid[:] = shgrid[:]
    tfinish = time.time()
    endstats(shgrid, timestep, tfinish - tstart, procs)
    pygame.quit()
    # close it all down...
    shm.close()
    shm.unlink()
    shm2.close()
    shm2.unlink()


def display(pgdisplay, grid, timestep):
    """show how the game is progressing"""
#   print(timestep)
    # change value so we can see it in pygame
    new = grid*255
    pygame.surfarray.blit_array(pgdisplay, new)
    pygame.display.flip()


def update(mygrid, og, start, stop, cols):
    """update grid rows from start to stop"""
    maxrow = mygrid.shape[0]
    maxcol = mygrid.shape[1]
    # NOTE: each process updates only a portion of the grid,
    # from row=start to (but not including) stop
    for i in range(start, stop):
        for j in range(cols):
            pr = i - 1
            pc = j - 1
            nr = (i + 1) % maxrow
            nc = (j + 1) % maxcol
            neighbors = (og[pr, pc] + og[pr, j] + og[pr, nc]
                    + og[i, pc] + og[i, nc]
                    + og[nr, pc] + og[nr, j] + og[nr, nc])
            if mygrid[i, j] == 1:
                if neighbors <= 1 or neighbors >= 4:
                    mygrid[i, j] = 0
            else:
                if neighbors == 3:
                    mygrid[i, j] = 1


def osc(grid):
    """oscillator on initial conditions"""
    grid[1, 1] = 1
    grid[1, 2] = 1
    grid[1, 3] = 1
    grid[4, 5] = 1
    grid[5, 5] = 1
    grid[6, 5] = 1


def initrandom(grid):
    """random initial conditions"""
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            grid[i, j] = random.randrange(2)


def endstats(mygrid, timestep, totaltime, procs):
    """show stats at the end"""
    rows = mygrid.shape[0]
    cols = mygrid.shape[1]
    print("resolution: %d x %d" % (rows, cols))
    print(" timesteps: %d" % (timestep))
    print("processors: %d" % (procs))
    print("      time: %.2f sec" % (totaltime))
    alive = np.count_nonzero(mygrid == 1)
    dead = np.count_nonzero(mygrid == 0)
    print("     alive: %3d" % (alive))
    print("      dead: %3d" % (dead))


if __name__ == '__main__':
    main()
