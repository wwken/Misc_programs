import unittest
from Solution import Solution

class TestMethods(unittest.TestCase):

    sol = Solution()

    def test_required(self):
        self.assertEqual(self.sol.letterCombinations("23"), ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"])