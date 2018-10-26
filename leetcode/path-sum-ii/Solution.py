# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def _pathSum(self, n, sum, all, ans):
        if n == None:
            return
        all.append(n.val)
        if n.val == sum:
            if n.left == None and n.right == None:
                ans.append(all)
        self._pathSum(n.left, sum - n.val, all[:], ans)
        self._pathSum(n.right, sum - n.val, all[:], ans)

    def pathSum(self, root, sum):
        """
        :type root: TreeNode
        :type sum: int
        :rtype: List[List[int]]
        """
        ans = []
        self._pathSum(root, sum, [], ans)
        return ans