# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def _kthSmallest(self, n, k, c, answer):
        if n is None:
            return c
        a = self._kthSmallest(n.left, k, c, answer)
        if a + 1 == k:
            answer['ans'] = n.val
        a = self._kthSmallest(n.right, k, a+1, answer)
        return a

    def kthSmallest(self, root, k):
        """
        :type root: TreeNode
        :type k: int
        :rtype: int
        """
        answer = {'ans': "?"}
        self._kthSmallest(root, k, 0, answer)
        return answer['ans']
        