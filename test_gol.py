"""
unit testing of gol class:
    python3 test_gol.py
"""

import unittest
from random import randrange
import numpy as np
import gol


class MyTestCase(unittest.TestCase):
    """setup and tests"""

    def setUp(self):
        self.rows = 25
        self.cols = 13
        # zeros
        self.gol0 = gol.GOL(self.rows, self.cols)
        self.gol0.initialconditions("zeros")
        # ones
        self.gol1 = gol.GOL(self.rows, self.cols)
        self.gol1.initialconditions("ones")
        # nums
        self.res = 5
        self.goln = gol.GOL(self.res, self.res)
        self.goln.initialconditions("numbers")

    def test_count(self):
        """test counts on homogeneous grids"""
        og0 = np.copy(self.gol0.grid)
        og1 = np.copy(self.gol1.grid)
        result = self.gol0.count(og0, int(self.rows/2), int(self.cols/2))
        self.assertEqual(result, 0)
        # middle
        result = self.gol1.count(og1, int(self.rows/2), int(self.cols/2))
        self.assertEqual(result, 8)
        # corners
        result = self.gol1.count(og1, 0, 0)
        self.assertEqual(result, 8)
        result = self.gol1.count(og1, self.rows - 1, 0)
        self.assertEqual(result, 8)
        result = self.gol1.count(og1, 0, self.cols - 1)
        self.assertEqual(result, 8)
        result = self.gol1.count(og1, self.rows - 1, self.cols - 1)
        self.assertEqual(result, 8)
        # random grid location
        randr = randrange(self.rows)
        randc = randrange(self.cols)
        result = self.gol1.count(og1, randr, randc)
        self.assertEqual(result, 8)
        result = self.gol0.count(og0, randr, randc)
        self.assertEqual(result, 0)

    def test_count_wraparound(self):
        """
        test wraparound counts on grid of numbers

         25 21 22 23 24 25 21
           ----------------
         5 | 1  2  3  4  5| 1     1  count(0,0) = 25+21+22+5+2+10+6+7
        10 | 6  7  8  9 10| 6     9  count(1,3) = 3+4+5+8+10+13+14+15
        15 |11 12 13 14 15|11    20  count(3,4) = 14+15+11+19+16+24+25+21
        20 |16 17 18 19 20|16
        25 |21 22 23 24 25|21
           ----------------
         5   1  2  3  4  5  1
        """
        ogn = np.copy(self.goln.grid)
        result = self.goln.count(ogn, 0, 0)
        self.assertEqual(result, 25+21+22+5+2+10+6+7)
        result = self.goln.count(ogn, 1, 3)
        self.assertEqual(result, 3+4+5+8+10+13+14+15)
        result = self.goln.count(ogn, 3, 4)
        self.assertEqual(result, 14+15+11+19+16+24+25+21)
        result = self.goln.count(ogn, 4, 0)
        self.assertEqual(result, 20+16+17+25+22+5+1+2)
        result = self.goln.count(ogn, 2, 2)
        self.assertEqual(result, 7+8+9+12+14+17+18+19)

    def test_oscillators(self):
        """test various oscillators"""
        osc = gol.GOL(self.rows, self.cols)
        osc.initialconditions("oscillator")
        result = osc.alive()
        self.assertEqual(result, 3)
        for _ in range(randrange(20, 60)):
            osc.step()
            result = osc.alive()
            # should just oscillate back and forth, but always 3 alive
            self.assertEqual(result, 3)
        # now check the corners
        osc = gol.GOL(8, 8)
        # bottom right
        osc.initialconditions("oscillator", 7, 7)
        result = osc.alive()
        self.assertEqual(result, 3)
        for _ in range(randrange(20, 60)):
            osc.step()
            result = osc.alive()
            # should just oscillate back and forth, but always 3 alive
            self.assertEqual(result, 3)
            self.assertEqual(osc.grid[7, 7], 1)
        osc = gol.GOL(13, 13)
        # top right
        osc.initialconditions("oscillator", 0, 12)
        result = osc.alive()
        self.assertEqual(result, 3)
        for _ in range(randrange(20, 60)):
            osc.step()
            result = osc.alive()
            # should just oscillate back and forth, but always 3 alive
            self.assertEqual(result, 3)
            # center should always be alive
            self.assertEqual(osc.grid[0, 12], 1)
        # test flip back and forth
        osc = gol.GOL(5, 5)
        osc.initialconditions("oscillator", 2, 2)
        result = osc.alive()
        self.assertEqual(result, 3)
        for i in range(13):
            osc.step()
            result = osc.alive()
            self.assertEqual(result, 3)
            if i % 2 == 0:
                self.assertEqual(osc.grid[1, 1], 0)
                self.assertEqual(osc.grid[2, 1], 0)
                self.assertEqual(osc.grid[3, 1], 0)
                self.assertEqual(osc.grid[1, 2], 1)
                self.assertEqual(osc.grid[2, 2], 1)
                self.assertEqual(osc.grid[3, 2], 1)
                self.assertEqual(osc.grid[1, 3], 0)
                self.assertEqual(osc.grid[2, 3], 0)
                self.assertEqual(osc.grid[3, 3], 0)
            else:
                self.assertEqual(osc.grid[1, 1], 0)
                self.assertEqual(osc.grid[2, 1], 1)
                self.assertEqual(osc.grid[3, 1], 0)
                self.assertEqual(osc.grid[1, 2], 0)
                self.assertEqual(osc.grid[2, 2], 1)
                self.assertEqual(osc.grid[3, 2], 0)
                self.assertEqual(osc.grid[1, 3], 0)
                self.assertEqual(osc.grid[2, 3], 1)
                self.assertEqual(osc.grid[3, 3], 0)

    def test_still_lifes(self):
        """test counts on still lifes"""
        # https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
        gol_still = gol.GOL(self.rows, self.cols)
        gol_still.initialconditions("zeros")
        # block in top left corner
        i = 0
        j = 0
        gol_still.grid[i, j] = 1
        gol_still.grid[i+1, j] = 1
        gol_still.grid[i, j+1] = 1
        gol_still.grid[i+1, j+1] = 1
        # tub in bottom center
        i = self.rows - 1
        j = int(self.cols/2)
        gol_still.grid[i, j+1] = 1
        gol_still.grid[i-1, j] = 1
        gol_still.grid[i-1, j+2] = 1
        gol_still.grid[i-2, j+1] = 1
        howmany = 8
        result = gol_still.alive()
        self.assertEqual(result, howmany)
        for i in range(randrange(5, 30)):
            gol_still.step()
            result = gol_still.alive()
            self.assertEqual(result, howmany)

    def test_glider(self):
        """test counts on a glider"""
        # https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
        gol_still = gol.GOL(self.rows, self.cols)
        gol_still.initialconditions("zeros")
        i = 0
        j = 0
        gol_still.grid[i, j+2] = 1
        gol_still.grid[i+1, j] = 1
        gol_still.grid[i+1, j+2] = 1
        gol_still.grid[i+2, j+1] = 1
        gol_still.grid[i+2, j+2] = 1
        howmany = 5
        result = gol_still.alive()
        self.assertEqual(result, howmany)
        for i in range(randrange(25, 50)):
            gol_still.step()
            result = gol_still.alive()
            self.assertEqual(result, howmany)


if __name__ == '__main__':
    unittest.main()
