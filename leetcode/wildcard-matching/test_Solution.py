import unittest
from Solution import Solution

# Given an input string (s) and a pattern (p), implement wildcard pattern matching with support for '?' and '*'.
#
# '?' Matches any single character.
# '*' Matches any sequence of characters (including the empty sequence).
# The matching should cover the entire input string (not partial).
#
# Note:
#
# s could be empty and contains only lowercase letters a-z.
# p could be empty and contains only lowercase letters a-z, and characters like ? or *.
# Example 1:
#
# Input:
# s = "aa"
# p = "a"
# Output: false
# Explanation: "a" does not match the entire string "aa".
# Example 2:
#
# Input:
# s = "aa"
# p = "*"
# Output: true
# Explanation: '*' matches any sequence.
# Example 3:
#
# Input:
# s = "cb"
# p = "?a"
# Output: false
# Explanation: '?' matches 'c', but the second letter is 'a', which does not match 'b'.
# Example 4:
#
# Input:
# s = "adceb"
# p = "*a*b"
# Output: true
# Explanation: The first '*' matches the empty sequence, while the second '*' matches the substring "dce".
# Example 5:
#
# Input:
# s = "acdcb"
# p = "a*c?b"
# Output: false

class TestStringMethods(unittest.TestCase):

    sol = Solution()

    def test_required(self):
        self.assertEqual(self.sol.isMatch('aa', 'a'), False)
        self.assertEqual(self.sol.isMatch('aa', '*'), True)
        self.assertEqual(self.sol.isMatch('cb', '?a'), False)
        self.assertEqual(self.sol.isMatch('adceb', '*a*b'), True)
        self.assertEqual(self.sol.isMatch('acdcb', 'a*c?b'), False)

    def test_basic(self):
        self.assertEqual(self.sol.isMatch('c', 'ca'), False)

    def test_question_mark(self):
        self.assertEqual(self.sol.isMatch('cb', 'c?'), True)
        self.assertEqual(self.sol.isMatch('cb', '??'), True)
        self.assertEqual(self.sol.isMatch('cb', '?b'), True)
        self.assertEqual(self.sol.isMatch('cb', '?'), False)
        self.assertEqual(self.sol.isMatch('cb', 'b'), False)
        self.assertEqual(self.sol.isMatch('cb', 'cb?'), False)
        self.assertEqual(self.sol.isMatch('??a?', 'bbab'), False)

    def test_star_mark(self):
        self.assertEqual(self.sol.isMatch('cac', 'c*'), True)
        self.assertEqual(self.sol.isMatch('cac', 'c**'), True)
        self.assertEqual(self.sol.isMatch('cac', 'c***'), True)
        self.assertEqual(self.sol.isMatch('cac', 'c****'), True)
        self.assertEqual(self.sol.isMatch('cac', 'c*****'), True)
        self.assertEqual(self.sol.isMatch('cac', 'c*****c'), True)
        self.assertEqual(self.sol.isMatch('cac', 'c*****ac'), True)
        self.assertEqual(self.sol.isMatch('cac', 'c*****?c'), True)
        self.assertEqual(self.sol.isMatch('cac', '*cac'), True)
        self.assertEqual(self.sol.isMatch('cacc', '*cc'), True)
        self.assertEqual(self.sol.isMatch('cacc', '*c'), True)
        self.assertEqual(self.sol.isMatch('cacc', '*ca'), False)
        self.assertEqual(self.sol.isMatch('cacc', '*cac'), False)
        self.assertEqual(self.sol.isMatch('cacc', '*cacc'), True)
        self.assertEqual(self.sol.isMatch('ba', '*a*'), True)

    def test_tricky(self):
        self.assertEqual(self.sol.isMatch('aaaa', '***a'), True)

    def test_tricky2(self):
        self.assertEqual(self.sol.isMatch('c', '*?*'), True)

    def test_tricky3(self):
        self.assertEqual(self.sol.isMatch('hi', '*?'), True)

    def test_tricky4(self):
        self.assertEqual(self.sol.isMatch('a', ''), False)

    def test_tricky5(self):
        self.assertEqual(self.sol.isMatch('abcde', '*?*?*?*?'), True)

    def test_tricky6(self):
        self.assertEqual(self.sol.isMatch('bbbab', '*??a?'), True)

    def test_tricky7(self):
        self.assertEqual(self.sol.isMatch('baabba', '?*?a??'), False)

    def test_tricky8(self):
        self.assertEqual(self.sol.isMatch('babbbbaabababaabbababaababaabbaabababbaaababbababaaaaaabbabaaaabababbabbababbbaaaababbbabbbbbbbbbbaabbb',
                                          'b**bb**a**bba*b**a*bbb**aba***babbb*aa****aabb*bbb***a'), False)

    def test_tricky9(self):
        self.assertEqual(self.sol.isMatch('bba', '*a**'), True)

    def test_tricky10(self):
        self.assertEqual(self.sol.isMatch('aac', '*c****'), True)

    def test_tricky11(self):
        self.assertEqual(self.sol.isMatch('abbabaaabbabbaababbabbbbbabbbabbbabaaaaababababbbabababaabbababaabbbbbbaaaabababbbaabbbbaabbbbababababbaabbaababaabbbababababbbbaaabbbbbabaaaabbababbbbaababaabbababbbbbababbbabaaaaaaaabbbbbaabaaababaaaabb',
                                          '**aa*****ba*a*bb**aa*ab****a*aaaaaa***a*aaaa**bbabb*b*b**aaaaaaaaa*a********ba*bbb***a*ba*bb*bb**a*b*bb'), False)

    def test_tricky12(self):
        self.assertEqual(self.sol.isMatch('mississippi',
                                          'm??*ss*?i*pi'), False)
