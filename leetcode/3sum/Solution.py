class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        nums.sort()
        print("nums: {}".format(nums))
        output = []
        numXD = {}
        for x in range(len(nums)-1):
            numX = nums[x]
            d = {}
            for y in range(x+1, len(nums)):
                numY = nums[y]
                if numY in d:
                    if numX in numXD and numY in numXD[numX]:
                        continue
                    else:
                        # print("numX: {}, numY: {}, d: {}, x: {}, y: {}".format(numX, numY, d, x, y))
                        output.append([numX, nums[d[numY]], numY])
                        if not numX in numXD:
                            numXD[numX] = set()
                        numXD[numX].add(numY)
                else:
                    expected = 0 - numX - numY
                    d[expected] = y
        return output

