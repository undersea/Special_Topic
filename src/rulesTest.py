from unittest import TestCase, main
from rules import Degree

class TestRules(TestCase):
    def setUp(self):
        print "setUp"
        self.rules = Degree()
        pass

    def tearDown(self):
        print "tearDown"
        del self.rules
        pass

    def testAdd(self):
        count = len(self.rules.rules)
        rule = ("one of","one")
        self.rules.add(rule)
        self.assertEqual(count, 0)
        self.assertEqual(len(self.rules.rules), 1)

    def testDelete(self):
        rule = ("one of","one")
        self.rules.rules.append(rule)
        count = len(self.rules.rules)
        self.assertEqual(count, 1)
        self.rules.delete(rule)
        self.assertEqual(len(self.rules.rules), 0)





if __name__ == "__main__":
    main()
