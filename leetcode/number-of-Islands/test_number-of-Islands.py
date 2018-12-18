import unittest
from Solution import Solution


class TestStringMethods(unittest.TestCase):

    sol = Solution()

    def test_required(self):
        self.assertEqual(self.sol.numIslands([['1', '1', '1', '1', '0'],
['1', '1', '0', '1', '0'],
['1', '1', '0', '0', '0'],
['0', '0', '0', '0', '0']]), 1)

    def test_required_2(self):
        self.assertEqual(self.sol.numIslands([['1', '1', '0', '0', '0'],
['1', '1', '0', '0', '0'],
['0', '0', '1', '0', '0'],
['0', '0', '0', '1', '1']]), 3)