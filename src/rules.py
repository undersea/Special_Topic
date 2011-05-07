#Rules definition for degrees and majors


class Degree(object):
    def __init__(self):
        self.rules = list()

        self.name = None
        
        
    def add(self, rule):
        self.rules.append(rule)


    def delete(self, rule):
        del self.rules[self.rules.index(rule)]


    def check_programme(major, programme):
        pass
    

    def __str__(self):
        return str(self.rules)



class LimitRule(object):
    def __init__(self):
        self.points = None
        self.level = None
        self.inschedule = None

    def __str__(self):
        out = "Limit of %d points" % (self.points)
        
        if not self.inschedule and self.inschedule == False:
            out = "%s not in the schedule" % (out)
        elif self.level != None:
            out = "%s at %d level" % (out, self.level)

        return out

class AtLeastRule(LimitRule):
    def __str__(self):
        return "At least %d points at %d level" % (self.points, self.level)


class RequiredRule(object):
    def __init__(self):
        self.inschedule = False
        self.papers = list()
        self.points = None
        self.level = None


    def __papers(self, papers):
        tmp = ""
        
        for paper in papers:
            if isinstance(paper, tuple) and len(paper) > 0:
                tmp2 = list(list(paper).pop())
                tmp2.reverse()
                operator = tmp2.pop()
                tmp2.reverse()
        
                try:
                    tmp = tmp2.pop()
                except:
                    continue
                else:
                    for x in tmp2:
                        if isinstance(x, tuple) and len(x) > 0:
                            tmp = "%s %s %s" % (tmp, operator, self.__papers([x]))
                        elif len(x) > 0:
                            if isinstance(operator, tuple):
                                tmp = "%s %s" % (tmp, x)
                            else:
                                tmp = "%s %s %s" % (tmp, operator, x)
            else:
                tmp = "%s %s" % (tmp, paper)

        return tmp
                    

    def __str__(self):
        import copy
        out = "Required"
        if self.inschedule:
            out = "%s %s papers of different subjects from the degree schedule" % (out, self.papers[0])
        else:
            out = "%s %s" % (out, self.__papers(self.papers))

        return out
                    




