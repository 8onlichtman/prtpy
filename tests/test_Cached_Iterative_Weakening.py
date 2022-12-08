import random
import unittest
import prtpy.partitioning.complete_greedy

from CIW import Cached_Iterative_Weakening
from prtpy import BinnerKeepingContents, BinnerKeepingSums, printbins


class TestCIW(unittest.TestCase):

    def test_different_m_values(self):
        """
        This test passes without implementation of the CIW algorithm
        because they both return an empty list {}
        """
        self.assertEqual(
            Cached_Iterative_Weakening(BinnerKeepingContents(), 3, [127, 125, 122, 105, 87, 75, 68, 64, 30, 22], 3),
            Cached_Iterative_Weakening(BinnerKeepingContents(), 3, [127, 125, 122, 105, 87, 75, 68, 64, 30, 22], 20))
        self.assertEqual(
            Cached_Iterative_Weakening(BinnerKeepingContents(), 5, [27, 23, 20, 19, 13, 9, 9, 5, 4, 3, 1, 1], 1),
            Cached_Iterative_Weakening(BinnerKeepingContents(), 5, [27, 23, 20, 19, 13, 9, 9, 5, 4, 3, 1, 1], 10))
        self.assertEqual(
            Cached_Iterative_Weakening(BinnerKeepingContents(), 2, [270, 150, 111, 98, 80, 77, 63, 26, 40, 33, 21, 10],
                                       5),
            Cached_Iterative_Weakening(BinnerKeepingContents(), 2, [270, 150, 111, 98, 80, 77, 63, 26, 40, 33, 21, 10],
                                       50))

    def test_optimality(self):
        self.assertEqual(
            Cached_Iterative_Weakening(BinnerKeepingContents(), 3, [127, 125, 122, 105, 87, 75, 68, 64, 30, 22], 3),
            prtpy.partitioning.complete_greedy(BinnerKeepingContents(), 3,
                                               [127, 125, 122, 105, 87, 75, 68, 64, 30, 22]))
        self.assertEqual(
            Cached_Iterative_Weakening(BinnerKeepingContents(), 5, [27, 23, 20, 19, 13, 9, 9, 5, 4, 3, 1, 1], 1),
            prtpy.partitioning.complete_greedy(BinnerKeepingContents(), 5, [27, 23, 20, 19, 13, 9, 9, 5, 4, 3, 1, 1]))
        self.assertEqual(
            Cached_Iterative_Weakening(BinnerKeepingContents(), 2, [270, 150, 111, 98, 80, 77, 63, 26, 40, 33, 21, 10],
                                       5),
            prtpy.partitioning.complete_greedy(BinnerKeepingContents(), 2,
                                               [270, 150, 111, 98, 80, 77, 63, 26, 40, 33, 21, 10]))

    def test_large_values(self):
        l1 = {}
        for a in range[100]:
            l1.insert(random.int)
        self.assertEqual(
            Cached_Iterative_Weakening(BinnerKeepingContents(), 3, l1, 6),
            prtpy.partitioning.complete_greedy(BinnerKeepingContents(), 3, l1))
        self.assertEqual(
            Cached_Iterative_Weakening(BinnerKeepingContents(), 3, l1, 6),
            Cached_Iterative_Weakening(BinnerKeepingContents(), 3, l1, 17))
        l2 = {}
        for a in range[1000]:
            l2.insert(random.int)
        self.assertEqual(
            Cached_Iterative_Weakening(BinnerKeepingContents(), 10, l2, 6),
            prtpy.partitioning.complete_greedy(BinnerKeepingContents(), 10, l2))
