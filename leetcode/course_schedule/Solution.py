class Solution(object):
    def canFinish(self, numCourses, prerequisites):
        """
        :type numCourses: int
        :type prerequisites: List[List[int]]
        :rtype: bool
        """
        class DiGraph:
            def __init__(self, prereqs):
                self.data = {}
                for v, k in prereqs:
                    if k not in self.data:
                        self.data[k] = []
                    self.data[k].append(v)

            def is_cyclic(self):
                path = set()
                visited = set()

                def visit_vertex(v):
                    if v in visited:
                        return False
                    path.add(v)
                    visited.add(v)
                    for neighbor in self.data.get(v, ()):
                        if neighbor in path or visit_vertex(neighbor):
                            return True
                    path.remove(v)
                    return False
                return any(visit_vertex(v) for v in self.data)

        return not DiGraph(prerequisites).is_cyclic()