import unittest
from utils import count
import numpy as np
from random import randrange

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.rows = 5
        self.cols = 8
        # zeros
        self.zgrid = np.zeros((self.rows,self.cols))
        # ones
        self.ogrid = np.ones((self.rows,self.cols))
        # nums
        self.ngrid = np.zeros((5, 5))
        for i in range(5):
            for j in range(5):
                self.ngrid[j,i] = (j*5)+(i+1)

    def test_count(self):
        """test counts on homogeneous grids"""
        result = count(self.zgrid, int(self.rows/2), int(self.cols/2))
        self.assertEqual(result, 0)
        # middle
        result = count(self.ogrid, int(self.rows/2), int(self.cols/2))
        self.assertEqual(result, 8)
        # corners
        result = count(self.ogrid, 0, 0)
        self.assertEqual(result, 8)
        result = count(self.ogrid, self.rows - 1, 0)
        self.assertEqual(result, 8)
        result = count(self.ogrid, 0, self.cols - 1)
        self.assertEqual(result, 8)
        result = count(self.ogrid, self.rows - 1, self.cols - 1)
        self.assertEqual(result, 8)
        # random grid location
        i = randrange(self.cols)
        j = randrange(self.rows)
        result = count(self.ogrid, i, j)
        self.assertEqual(result, 8)

    def test_count_wraparound(self):
        """test counts on grid of numbers"""
        # test wraparound 
        """
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
        result = count(self.ngrid, 0, 0)
        self.assertEqual(result, 25+21+22+5+2+10+6+7)
        result = count(self.ngrid, 1, 3)
        self.assertEqual(result, 3+4+5+8+10+13+14+15)
        result = count(self.ngrid, 3, 4)
        self.assertEqual(result, 14+15+11+19+16+24+25+21)
        result = count(self.ngrid, 4, 0)
        self.assertEqual(result, 20+16+17+25+22+5+1+2)
        result = count(self.ngrid, 2, 2)
        self.assertEqual(result, 7+8+9+12+14+17+18+19)

if __name__ == '__main__':
    unittest.main()
