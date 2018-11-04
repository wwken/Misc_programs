class Solution:
    def maxArea(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        left,right,mArea=0,len(height)-1,0
        while (left<right):
            if height[left]>=height[right]:
                mArea = max(mArea,(right-left)*height[right])
                right-=1
            else:
                mArea = max(mArea,(right-left)*height[left])
                left+=1
        return mArea