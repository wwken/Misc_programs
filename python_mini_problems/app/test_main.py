import unittest
from app.main3 import MainObj

# This variable is set to True if the unit tests are run using real dev database
# USE_REAL_DEV_DATABASE = True
USE_REAL_DEV_DATABASE = False

DRY_RUN = True


class TestUM(unittest.TestCase):
    mainObj = None
    def setUp(self):
        self.mainObj = MainObj()

class TestUMNoDB(TestUM):
    def test_0_basic_elements(self):
        a = [1, 5, 3, 3, 7]
        aas = self.mainObj.solution(a)
        self.assertTrue(aas)

        a = [1, 3, 5, 3, 4]
        aas = self.mainObj.solution(a)
        self.assertFalse(aas)

        a = [7, 3, 5, 3, 4]
        aas = self.mainObj.solution(a)
        self.assertFalse(aas)

        a = [7, 8, 5, 8, 9]
        aas = self.mainObj.solution(a)
        self.assertFalse(aas)

        a = [8, 8, 5, 8, 9]
        aas = self.mainObj.solution(a)
        self.assertTrue(aas)

        a = [8, 8, 5, 8, 0]
        aas = self.mainObj.solution(a)
        self.assertFalse(aas)

        a = [3, 8, 5, 8, 0]
        aas = self.mainObj.solution(a)
        self.assertFalse(aas)

        a = [3, 8, 5, 8, 9]
        aas = self.mainObj.solution(a)
        self.assertTrue(aas)

        a = [1, 8, 3, 2, 9]
        aas = self.mainObj.solution(a)
        self.assertTrue(aas)

        a = [1, 8, 2, 3, 9]
        aas = self.mainObj.solution(a)
        self.assertFalse(aas)

        a = [1, 8, 2, 3, 5]
        aas = self.mainObj.solution(a)
        self.assertFalse(aas)

if __name__ == '__main__':
    unittest.main()