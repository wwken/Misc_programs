# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def pathSum(self, root, sum):

        def pathSumFrom (n, sum):
            if n is None:
                return 0
            total = 0
            if n.val == sum:
                total = 1
            total = total + pathSumFrom(n.left, sum - n.val) + pathSumFrom(n.right, sum - n.val)
            return total

        if root is None:
            return 0
        return pathSumFrom(root, sum) + self.pathSum(root.left, sum) + self.pathSum(root.right, sum)