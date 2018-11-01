import unittest
from Solution import Solution

class TestStringMethods(unittest.TestCase):

    sol = Solution()

    def test_required(self):
        self.assertEqual(self.sol.permute([1,2,3]), [
  [1,2,3],
  [1,3,2],
  [2,1,3],
  [2,3,1],
  [3,1,2],
  [3,2,1]])