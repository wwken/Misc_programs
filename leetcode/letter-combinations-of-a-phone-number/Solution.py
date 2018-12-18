class Solution(object):
    m={'1': [], '2': ['a', 'b', 'c'], '3': ['d', 'e', 'f'], '4': ['g', 'h', 'i'],
           '5': ['j', 'k', 'l'], '6': ['m', 'n', 'o'], '7': ['p', 'q', 'r', 's'], '8': ['t', 'u', 'v'], '9': ['w', 'x', 'y', 'z']}

    def buildOutput(self, d, output):
        entry = self.m[d]
        isFirst = len(output) == 0
        originKeys = list(output.keys())
        for e in entry:
            if isFirst:
                output[e] = None
            else:
                newKArray = []
                for o in originKeys:
                    newO = o + e
                    # print "newO: " + o + " " + e
                    newKArray.append(newO)
                    if o in output:
                        del output[o]
                for k in newKArray:
                    output[k] = None
        return output


    def letterCombinations(self, digits):
        """
        :type digits: str
        :rtype: List[str]
        """
        output={}
        for d in digits:
            output = self.buildOutput(d, output)
        return sorted(list(output.keys()))
