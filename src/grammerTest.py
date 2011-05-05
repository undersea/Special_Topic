from unittest import TestCase, main
from grammer import *
from rules import *

class TestGrammer(TestCase):
    def testParseString(self):
        result = parse('BSc.xml')

        self.assertTrue(isinstance(result, Degree))
        


if __name__ == "__main__":
    main()
