class Solution:
    def subarraySum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        sum = 0
        result = 0
        preSum = {}
        preSum[0] = 1

        for i in range(len(nums)):
            sum += nums[i]
            if sum - k in preSum:
                result += preSum[sum - k]
            if sum not in preSum:
                preSum[sum] = 1
            else:
                preSum[sum] = preSum[sum] + 1

        return result