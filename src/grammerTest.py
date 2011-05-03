from unittest import TestCase, main
from grammer import *
from rules import *

class TestGrammer(TestCase):
    def testParse(self):
        result = parse("")

        self.assertTrue(isinstance(result, Rules))


if __name__ == "__main__":
    main()
