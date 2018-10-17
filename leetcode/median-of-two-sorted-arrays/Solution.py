import math
import sys

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
            if a[closetIndex] > m:
                aa = a[0:closetIndex]
            else:
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

    def findKth(self,k, nums1, nums2, s1, s2):
        if s1>=len(nums1):
            return nums2[s2+k-1]

        if s2>=len(nums2):
            return nums1[s1+k-1]

        if k==1:
            return min(nums1[int(s1)], nums2[int(s2)])

        m1 = s1+int(k/2)-1
        m2 = s2+int(k/2)-1

        mid1 = sys.maxsize
        if m1 <len(nums1):
            mid1 = nums1[int(m1)]

        mid2 = sys.maxsize
        if m2 <len(nums2):
            mid2 = nums2[int(m2)]

        if (mid1 < mid2):
            return self.findKth(k-int(k/2), nums1, nums2, m1+1, s2)
        else:
            return self.findKth(k-int(k/2), nums1, nums2, s1, m2+1)



    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        total = len(nums1) + len(nums2);
        if (total%2==0):
            return (self.findKth(int(total/2)+1, nums1, nums2, 0, 0) + self.findKth(int(total/2), nums1, nums2, 0, 0))/2.0;
        else:
            return self.findKth(int(total/2)+1, nums1, nums2, 0, 0);


