class Solution(object):

    def stepsOn(self, grid, i, j):
        if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]) or grid[i][j] == '0':
            return
        grid[i][j] = '0'
        self.stepsOn(grid, i-1, j)
        self.stepsOn(grid, i, j-1)
        self.stepsOn(grid, i+1, j)
        self.stepsOn(grid, i, j+1)

    def numIslands(self, grid):
        """
        :type grid: List[List[str]]
        :rtype: int
        """
        count = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == '1':
                    self.stepsOn(grid, i, j)
                    count += 1
        return count
