class Solution(object):
    def _isMatch(self, s, p, startI, startJ):
        j=startJ
        for i in range(startI, len(p)):
            if p[i] == '?':
                j += 1
                if j > len(s):
                    return False
            elif p[i] == '*':
                if i == len(p) - 1:  # if last character
                    return True
                else:
                    nextC = p[i+1]
                    # Now it looks for the match character in s
                    goodJs = []
                    while(j<len(s)):
                        if s[j] == nextC:   #all good, found match
                            goodJs.append(j)
                        j+=1
                    for goodJ in goodJs:
                        ss = s[goodJ:]
                        pp = p[i+1:]
                        result = self._isMatch(ss, pp, 0, 0)
                        if result:
                            return True
            else:
                if j >= len(s) or p[i] != s[j]: # character not equal!
                    return False
                else:
                    j += 1

        if j < len(s):  # If there are some letters left in s!
            return False
        return True

    def isMatch(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: bool
        """
        return self._isMatch(s, p, 0, 0)
