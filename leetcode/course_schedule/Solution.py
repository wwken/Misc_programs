class Solution(object):
    def testCycles(self, pre, startingCourse, currentCourse, wholeRoutes, allFinalCycles):
        if startingCourse == currentCourse:
            # print("There is a cycles....")
            for c in wholeRoutes:
                allFinalCycles.add(c)
            return True
        if currentCourse == None:
            currentCourse = startingCourse
        if currentCourse not in pre:
            return False
        if currentCourse in wholeRoutes:
            # print("There is a cycles....")
            for c in wholeRoutes:
                allFinalCycles.add(c)
            return True
        else:
            wholeRoutes.add(currentCourse)
        allPres = pre[currentCourse]

        isThereCycles = False
        for p in allPres:
            # now try to see if there is cycles
            thisCycles = self.testCycles(pre, startingCourse, p, wholeRoutes.copy(), allFinalCycles)
            isThereCycles = isThereCycles or thisCycles
        return isThereCycles


    def canFinish(self, numCourses, prerequisites):
        """
        :type numCourses: int
        :type prerequisites: List[List[int]]
        :rtype: bool
        """
        pre = {}

        # build the prerequisites
        for e in prerequisites:
            c = e[0]
            p = e[1]
            if c in pre:
                pre[c].append(p)
            else:
                pre[c] = [p]

        allFinalCycles = set()
        for c in pre:
            self.testCycles(pre, c, None, set(), allFinalCycles)

        if len(allFinalCycles):
            # There is cycles
            for c in allFinalCycles:
                pre.pop(c, None)

        totalCoursesCount = len(pre)

        if totalCoursesCount == 1:
            totalCoursesCount = 2

        if numCourses <= totalCoursesCount:
            # print("numCourses <= totalCoursesCount, Good")
            return True
        else:
            # print("numCourses > totalCoursesCount, bad")
            return False





