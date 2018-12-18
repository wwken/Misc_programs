class Solution:
    def uniquePathsWithObstacles(self, grid):
        """
        :type obstacleGrid: List[List[int]]
        :rtype: int
        """
        dp = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]

        if grid[0][0] == 0:
            dp[0][0] = 1

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if not grid[i][j] and (i or j):
                    if grid[i-1][j] or i == 0:
                        dp[i][j] = dp[i][j-1]
                    elif grid[i][j-1] or j == 0:
                        dp[i][j] = dp[i-1][j]
                    else:
                        dp[i][j] = dp[i-1][j] + dp[i][j-1]

        return dp[-1][-1]