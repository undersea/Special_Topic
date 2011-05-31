import operators as op
from rules import *
import grammer as gr


class PrerequisiteRule(RequiredRule):
    def __init__(self, paper):
        super(PrerequisiteRule, self).__init__()
        self.paper = paper

    def __str__(self):
        return '%s %s' % (self.paper, super(PrerequisiteRule, self).__str__())


class CorequisiteRule(PrerequisiteRule):
    pass


class RestrictedRule(Rule):
    pass

if __name__ == '__main__':
    rule = PrerequisiteRule('117.254')
    rule.papers.extend([tuple([tuple(['or', tuple(['and', '194.101', '199.101']), '117.152'])])])
    print rule.papers
    print rule
    print rule.check(['161.101', '159.201', '199.101',])
    print op.missing
