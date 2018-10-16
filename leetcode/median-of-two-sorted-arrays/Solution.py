import math


class Solution(object):
    def mergeValueIntoArray(self, v, a):
        def _mergeValueIntoArray(v, a, left, right):
            if right >= len(a):
                right = len(a) - 1
            if left == right:
                if a[left] > v:
                    return left - 1
                else:
                    return left
            if right - left == 1:
                if left == len(a) - 1: #right most already
                    return max(left, 0)
                elif a[left] >= v:
                    if a[left] == v:
                        return max(left, 0)
                    else:
                        return max(left-1, 0)
                elif a[right] <= v:
                    return right + 1
                elif a[left] < v and a[right] > v:
                    return left+1
                else:
                    return left
            midElement = int((left + right) / 2)
            ha = 0
            if v > a[midElement] and v < a[midElement+1]:
                ha = midElement + 1
            elif v < a[midElement]:
                ha = _mergeValueIntoArray(v, a, 0, midElement)
            else:
                if len(a) % 2 == 1:
                    ha = _mergeValueIntoArray(v, a, midElement, right)
                else:
                    ha = _mergeValueIntoArray(v, a, midElement+1, right)
            return ha

        insertIndex = _mergeValueIntoArray(v, a, 0, len(a)-1)
        a.insert(insertIndex, v)
        return a

    def findCloset(self, aa, m):
        def _findCloset(aa, m, start, end):
            if end-start == 1:
                if aa[start] >= m:
                    return start
                elif aa[start] < m:
                    return end
                else:
                    return end
            else:
                mid = int((end+start)/2)
                if m > aa[mid]:
                    return _findCloset(aa, m, mid, end)
                else:
                    return _findCloset(aa, m, start, mid)
        index = _findCloset(aa, m, 0, len(aa)-1)
        return index

    def half(self, a, m, firstHalf=True):
        aa = None
        if firstHalf:
            closetIndex = self.findCloset(a, m)
            aa = a[0:closetIndex+1]
        else:
            closetIndex = self.findCloset(a, m)
            if closetIndex == 0:
                if a[closetIndex] == a[int(len(a)/2)]:
                    closetIndex=int(len(a)/2)
            aa =a[closetIndex:]
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
        if len(nums1) == 0:
            return self.median(nums2)
        elif len(nums2) == 0:
            return self.median(nums1)

        if len(nums1) == 2 and len(nums2) == 2:
            return (max(nums1[0], nums2[0]) + min(nums1[1], nums2[1]))/2

        if len(nums1) == 1:
            numss = self.mergeValueIntoArray(nums1[0], nums2)
            return self.median(numss)
        elif len(nums2) == 1:
            numss = self.mergeValueIntoArray(nums2[0], nums1)
            return self.median(numss)

        if len(nums1) == len(nums2):
            if self.median(nums1) == self.median(nums2):
                return self.median(nums1)

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
                nums11 = self.half(nums1, m1, False)
                nums22 = self.half(nums2, m2)
                return self.findMedianSortedArrays(nums11, nums22)
            else:
                if (nums1[0] < nums2[0] and nums1[len(nums1)-1] > nums2[len(nums2)-1] and len(nums1) < len(nums2))\
                        or (nums2[0] < nums1[0] and nums2[len(nums2)-1] > nums1[len(nums1)-1] and len(nums1) < len(nums2)):
                    nums11 = self.half(nums1, m1, False)
                    nums22 = self.half(nums2, m2)
                    return self.findMedianSortedArrays(nums11, nums22)
                else:
                    nums11 = self.half(nums1, m1)
                    nums22 = self.half(nums2, m2, False)
                    return self.findMedianSortedArrays(nums11, nums22)
        else:
            pass

        return (m1 + m2) / 2.0

