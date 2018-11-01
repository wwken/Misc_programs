class Solution(object):
    def _permute(self, nums, pos, output):
        if pos >= len(nums):
            return output
        element = nums[pos]
        if len(output) == 0:
            output.append([element])
        else:
            tOutput = []
            for o in output:
                for i in range(len(o)+1):
                    oo = o[:]
                    oo.insert(i, element)
                    tOutput.append(oo)
            output = []
            for oo in tOutput:
                output.append(oo)
        return self._permute(nums, pos+1, output)

    def permute(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        output = self._permute(nums, 0, [])
        output.sort()
        return output