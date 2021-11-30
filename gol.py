"""
game of life class

J. Knerr
November 2021
"""

import random
import numpy as np


class GOL():
    """game of life object"""

    def __init__(self, rows=10, cols=10):
        """construct GOL object, given rows and columns"""
        self.grid = np.zeros((rows, cols))
        self.rows = rows
        self.cols = cols

    def __repr__(self):
        """every class should have a repr"""
        # thanks to Dan Bader for this!
        return "%s(%d, %d)" % (self.__class__.__name__, self.rows, self.cols)

    def __str__(self):
        """need an str, too???"""
        if self.rows*self.cols > 100:
            return self.__repr__()
        output = self.__repr__()
        output += "\n"
        for i in range(self.rows):
            for j in range(self.cols):
                output += "%2d" % self.grid[i, j]
            output += "\n"
        return output

    def step(self):
        """update the grid one time step, according to the game rules"""
        origgrid = np.copy(self.grid)
        # use copy of grid so counts aren't messed up as we go
        for i in range(self.rows):
            for j in range(self.cols):
                neighbors = self.count(origgrid, i, j)
                if self.grid[i, j] == 1:
                    if neighbors <= 1 or neighbors >= 4:
                        self.grid[i, j] = 0
                else:
                    if neighbors == 3:
                        self.grid[i, j] = 1

    def count(self, og, row, col):
        """given a grid location, count and return number of alive neighbors"""
        pr = row - 1     # previous row (using python negative indexing here)
        pc = col - 1     # previous col (using python negative indexing here)
        nr = (row + 1) % self.rows     # next row
        nc = (col + 1) % self.cols     # next col
        return og[pr, pc] + og[pr, col] + og[pr, nc] + \
            og[row, pc] + og[row, nc] + \
            og[nr, pc] + og[nr, col] + og[nr, nc]

    def initialconditions(self, how="random", i=None, j=None):
        """set up the initial grid cells"""
        if how == "oscillator":
            self._oscillator(i, j)
        elif how == "zeros":
            self._zeros()
        elif how == "ones":
            self._ones()
        elif how == "numbers":
            self._numbers()
        else:
            self._randomstart()

    def _randomstart(self):
        """randomly placed 1s and 0s"""
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i, j] = random.randrange(2)

    def _oscillator(self, i=None, j=None):
        """line of 3 in the middle, or at i,j"""
        if i is None and j is None:
            halfrow = int(self.rows/2)
            halfcol = int(self.cols/2)
            self.grid[halfrow, halfcol] = 1
            self.grid[halfrow+1, halfcol] = 1
            self.grid[halfrow-1, halfcol] = 1
        else:
            # put horizontal oscillator at i,j (row,col)
            self.grid[i, j-1] = 1
            self.grid[i, j] = 1
            jplus = (j+1) % self.cols
            self.grid[i, jplus] = 1

    def _zeros(self):
        """all 0s"""
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i, j] = 0

    def _ones(self):
        """all 1s"""
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i, j] = 1

    def _numbers(self):
        """numbers in each cell, for testing corners"""
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i, j] = (i*5) + (j+1)

    def alive(self):
        """return number alive on grid"""
        return np.sum(self.grid)

    def dead(self):
        """return number dead on grid"""
        return (self.rows * self.cols) - np.sum(self.grid)


def main():
    """simple test code here"""
    goltest = GOL(5, 8)
    goltest.initialconditions("random")
    print(goltest)
    print("alive:", goltest.alive())
    print(" dead:", goltest.dead())
    goltest2 = GOL(15, 18)
    print(goltest2)
    print("alive:", goltest2.alive())
    print(" dead:", goltest2.dead())
    gosc = GOL(5, 5)
    gosc.initialconditions("oscillator", 0, 0)
    print(gosc)
    gosc.step()
    print(gosc)


if __name__ == '__main__':
    main()
