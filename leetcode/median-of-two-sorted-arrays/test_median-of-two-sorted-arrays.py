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

    def test_findCloset(self):
        self.assertEqual(self.sol.findCloset([3,4,5,6], 2.5), 0)
        self.assertEqual(self.sol.findCloset([3,4,5,6], 3), 0)
        self.assertEqual(self.sol.findCloset([3,4,5,6], 3.5), 1)
        self.assertEqual(self.sol.findCloset([3,4,5,6], 4), 1)
        self.assertEqual(self.sol.findCloset([3,4,5,6], 4.5), 2)
        self.assertEqual(self.sol.findCloset([3,4,5,6], 5), 2)
        self.assertEqual(self.sol.findCloset([3,4,5,6], 5.5), 3)
        self.assertEqual(self.sol.findCloset([3,4,5,6], 6), 3)
        self.assertEqual(self.sol.findCloset([3,4,5,6], 7), 3)

        self.assertEqual(self.sol.findCloset([3,4,5], 2), 0)
        self.assertEqual(self.sol.findCloset([3,4,5], 3), 0)
        self.assertEqual(self.sol.findCloset([3,4,5], 3.5), 1)
        self.assertEqual(self.sol.findCloset([3,4,5], 4), 1)
        self.assertEqual(self.sol.findCloset([3,4,5], 4.5), 2)
        self.assertEqual(self.sol.findCloset([3,4,5], 5), 2)
        self.assertEqual(self.sol.findCloset([3,4,5], 5.5), 2)
        self.assertEqual(self.sol.findCloset([3,4,5], 6), 2)

    def test_mergeValueIntoArray(self):
        self.assertEqual(self.sol.mergeValueIntoArray(1, [2,3,4]), [1,2,3,4])
        self.assertEqual(self.sol.mergeValueIntoArray(2, [2,3,4]), [2,2,3,4])
        self.assertEqual(self.sol.mergeValueIntoArray(3, [2,3,4]), [2,3,3,4])
        self.assertEqual(self.sol.mergeValueIntoArray(4, [2,3,4]), [2,3,4,4])
        self.assertEqual(self.sol.mergeValueIntoArray(3, [-2,-1]), [-2,-1,3])
        self.assertEqual(self.sol.mergeValueIntoArray(2, [1,3]), [1,2,3])
        self.assertEqual(self.sol.mergeValueIntoArray(5, [1,3]), [1,3,5])
        self.assertEqual(self.sol.mergeValueIntoArray(0, [1,3]), [0,1,3])
        self.assertEqual(self.sol.mergeValueIntoArray(3, [1,2,4,5,6]), [1,2,3,4,5,6])

    def test_mergeValueIntoArray1(self):
        self.assertEqual(self.sol.mergeValueIntoArray(3, [1,2,4,5]), [1,2,3,4,5])

    def test_required(self):
        self.assertEqual(self.sol.findMedianSortedArrays([1, 3], [2]), 2.0)
        self.assertEqual(self.sol.findMedianSortedArrays([1, 2], [3, 4]), 2.5)
        self.assertEqual(self.sol.findMedianSortedArrays([], [1]), 1)

    def test_tricky1(self):
        self.assertEqual(self.sol.findMedianSortedArrays([1, 12, 15, 26, 38], [2, 13, 17, 30, 45]), 16)

    def test_tricky2(self):
        self.assertEqual(self.sol.findMedianSortedArrays([1,2], [3,4]), 2.5)

    def test_tricky3(self):
        self.assertEqual(self.sol.findMedianSortedArrays([3], [-2, -1]), -1.0)

    def test_tricky4(self):
        self.assertEqual(self.sol.findMedianSortedArrays([1,1,3,3], [1,1,3,3]), 2.0)

    def test_tricky5(self):
        self.assertEqual(self.sol.findMedianSortedArrays([1], [2,3,4]), 2.5)

    def test_tricky6(self):
        self.assertEqual(self.sol.findMedianSortedArrays([3], [1,2,4,5,6]), 3.5)

    def test_tricky7(self):
        self.assertEqual(self.sol.findMedianSortedArrays([1,2], [3,4,5,6]), 3.5)

    def test_tricky8(self):
        self.assertEqual(self.sol.findMedianSortedArrays([1,1,1,1,1,1,1,1,1,1,4,4], [1,3,4,4,4,4,4,4,4,4,4]), 3.0)

    def test_tricky9(self):
        self.assertEqual(self.sol.findMedianSortedArrays([1,5], [2,3,4]), 3.0)