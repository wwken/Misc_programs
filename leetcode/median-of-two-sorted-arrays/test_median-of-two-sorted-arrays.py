import unittest
from Solution import Solution

# 4. Median of Two Sorted Arrays
#
# There are two sorted arrays nums1 and nums2 of size m and n respectively.
#
# Find the median of the two sorted arrays. The overall run time complexity should be O(log (m+n)).
#
# You may assume nums1 and nums2 cannot be both empty.
#
# Example 1:
#
# nums1 = [1, 3]
# nums2 = [2]
#
# The median is 2.0
# Example 2:
#
# nums1 = [1, 2]
# nums2 = [3, 4]
#
# The median is (2 + 3)/2 = 2.5


class TestMethods(unittest.TestCase):

    sol = Solution()

    def test_required(self):
        self.assertEqual(self.sol.findMedianSortedArrays([1, 3], [2]), 2.0)
        self.assertEqual(self.sol.findMedianSortedArrays([1, 2], [3, 4]), 2.5)
        self.assertEqual(self.sol.findMedianSortedArrays([], [1]), 0.5)

    def test_tricky1(self):
        self.assertEqual(self.sol.findMedianSortedArrays([1, 12, 15, 26, 38], [2, 13, 17, 30, 45]), 16)