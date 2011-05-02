#Rules definition for degrees and majors


class Rules(object):
    def __init__(self):
        self.rules = list()

        
    def add(self, rule):
        self.rules.append(rule)


    def delete(self, rule):
        del self.rules[self.rules.index(rule)]
        




class BScRules(Rules):
    pass

