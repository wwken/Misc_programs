class Solution(object):
    hasBeenProcessedSubStrs = {}

    def extractPattern(self, p, startPos):
        r = ""
        while startPos < len(p):
            if p[startPos] != "?" and p[startPos] != "*":
                r += p[startPos]
            else:
                break
            startPos += 1
        return r

    def _numOfSpecialCharacter(self, x, sc):
        num=0
        for xx in x:
            if xx == sc:
                num += 1
        return num

    def _isMatch(self, s, p, startI, startJ):
        key = s + "|||||##!#|||||##!#||" + p
        if not key in self.hasBeenProcessedSubStrs:
            self.hasBeenProcessedSubStrs[key] = 1
        else:
            return False
        j=startJ
        i=startI
        hasNormalCharacterInP=False
        while i < len(p):
            if p[i] == '?':
                j += 1
                if j > len(s):
                    return False
            elif p[i] == '*':
                if i == len(p) - 1:  # if last character
                    return True
                else:
                    nextC = p[i+1]
                    if nextC == '*' or nextC == '?':
                        if nextC == '?':
                            jj = j
                            while jj < len(s):
                                result = self._isMatch(s[jj:], p[i+1:], 0, 0)
                                if result:
                                    return True
                                jj += 1
                    else:
                        # Now it looks for the match character in s
                        goodJs = []
                        patternToFound = self.extractPattern(p, i+1)
                        # while(j<= (len(s) - len(p[i+1:]))+1):
                        #     if j < len(s) and s[j] == nextC:   #all good, found match
                        #
                        #         # Very important, look ahead of the pattern
                        #         goodJs.append(j)
                        #     j+=1
                        start=0
                        while True:
                            found = s.find(patternToFound, start)
                            if found > -1:
                                if found <= (len(s) - len(p[i+1:]))+1:
                                    goodJs.append(found)
                                else:
                                    break
                                start = found + 1
                            else:
                                break
                        for goodJ in goodJs:
                            ss = s[goodJ:]
                            pp = p[i+1:]
                            result = self._isMatch(ss, pp, 0, 0)
                            if result:
                                return True
            else:
                hasNormalCharacterInP=True
                if j >= len(s) or p[i] != s[j]: # character not equal!
                    return False
                else:
                    j += 1
            i += 1

        if j < len(s):  # If there are some letters left in s!
            if i == len(p) and i>0: # last charactger in P
                if p[i-1] == '?':
                    if j == i-1:
                        pass
                    if not hasNormalCharacterInP:
                        numQ = self._numOfSpecialCharacter(p, '?')
                        numS = self._numOfSpecialCharacter(p, '*')
                        if numS == 0:
                            if numQ == len(s):
                                return True
                        if numS > 0:
                            return True
                        else:
                            return False
                if p[i-1] == '*':
                    if j <= i or j==len(s)-1:
                        return True
            return False
        return True

    def isMatch(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: bool
        """
        def beautify(p):
            while True:
                pp = p.replace("**", "*")
                if pp == p:
                    return pp
                p = pp

        p = beautify(p)
        self.hasBeenProcessedSubStrs = {}
        return self._isMatch(s, p, 0, 0)
