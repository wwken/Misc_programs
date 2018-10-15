import math


class Solution(object):
    def half(self, a, firstHalf=True):
        aa = None
        if firstHalf:
            aa = a[0:int(math.floor(len(a)/2))+1]
        else:
            aa =a[int(math.floor(len(a)/2)):]
        return aa

    def median(self, a):
        if len(a) == 0:
            return 0
        if len(a) == 1:
            return a[0]
        n = int(len(a) / 2)
        if len(a) % 2 == 0:
            return float(a[n] + a[n-1]) / 2.0
        else:
            return float(a[n]+a[n]) / 2.0

    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """

        if len(nums1) == 2 and len(nums2) == 2:
            return (max(nums1[0], nums2[0]) + min(nums1[1], nums2[1]))/2

        m1 = None
        m2 = None
        if len(nums1) == 1:
            m1 = nums1[0]
        else:
            m1 = self.median(nums1)

        if len(nums2) == 1:
            m2 = nums2[0]
        else:
            m2 = self.median(nums2)

        if len(nums1) > 2 or len(nums2) > 2:
            if m1 < m2:
                nums11 = self.half(nums1, False)
                nums22 = self.half(nums2)
                return self.findMedianSortedArrays(nums11, nums22)
            else:
                nums11 = self.half(nums1)
                nums22 = self.half(nums2, False)
                return self.findMedianSortedArrays(nums11, nums22)
        else:
            pass

        return (m1 + m2) / 2.0

