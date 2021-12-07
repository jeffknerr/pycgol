
# https://stackoverflow.com/questions/34824382/sharing-numpy-arrays-between-multiple-processes-without-inheritance

import numpy as np
from multiprocessing import shared_memory
import multiprocessing 

RED   = u"\033[1;31m"
BLUE  = u"\033[1;34m"
RESET = u"\033[0;0m"
CIRCLE = u"\u25CF"

RED_DISK = RED + CIRCLE + RESET
BLUE_DISK = BLUE + CIRCLE + RESET
RED_BORDER = RED + "-" + RESET
BLUE_BORDER = BLUE + "\\" + RESET

def update(mylist, og, start, stop, cols):
#   print(">>>", start, stop)
#   print(">>>", mylist.shape, og.shape)
    maxrow = mylist.shape[0]
    maxcol = mylist.shape[1]
    for i in range(start, stop):
        for j in range(cols):
            pr = i - 1
            pc = j - 1 
            nr = (i + 1) % maxrow 
            nc = (j + 1) % maxcol 
            neighbors = og[pr,pc]+og[pr,j]+og[pr,nc]+\
               og[i,pc]+og[i,nc]+\
               og[nr,pc]+og[nr,j]+og[nr,nc]
            before = mylist[i,j]
            if mylist[i,j] == 1:
                if neighbors <= 1 or neighbors >= 4:
                    mylist[i,j] = 0
            else:
                if neighbors == 3:
                    mylist[i,j] = 1
#           print(":::", i,j,before,neighbors,mylist[i,j])

def osc(grid, rows, cols):
    grid[1,1]=1
    grid[1,2]=1
    grid[1,3]=1
    grid[4,5]=1
    grid[5,5]=1
    grid[6,5]=1

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

def main():
    rows = 10
    cols = 8
    grid = np.zeros((rows,cols))
    oldgrid = np.zeros((rows,cols))
    osc(grid, rows, cols)
    oldgrid[:] = grid[:]
    shm = shared_memory.SharedMemory(create=True, size=grid.nbytes)
    shgrid = np.ndarray(grid.shape, dtype=grid.dtype, buffer=shm.buf)
    shgrid[:] = grid[:]
    shm2 = shared_memory.SharedMemory(create=True, size=oldgrid.nbytes)
    sholdgrid = np.ndarray(oldgrid.shape, dtype=oldgrid.dtype, buffer=shm2.buf)
    sholdgrid[:] = oldgrid[:]
    print("-"*40)
    print("-"*40)
    print(shm.name)
    print(shm2.name)
    prettyprint(shgrid)

    nts = 5
    rowhalf = int(rows/2)
    for ts in range(nts):
        print("-"*40, " ts:", ts)
        p1 = multiprocessing.Process(target=update, args=(shgrid,sholdgrid,0,rowhalf,cols))
        p2 = multiprocessing.Process(target=update, args=(shgrid,sholdgrid,rowhalf,rows,cols))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        sholdgrid[:] = shgrid[:]
        prettyprint(shgrid)

    shm.close()
    shm.unlink()
    shm2.close()
    shm2.unlink()

main()
