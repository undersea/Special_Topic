#Rules definition for degrees and majors

from operators import check, set_inschedule

class Degree(object):
    def __init__(self):
        self.rules = list()

        self.name = None

        self.schedule = dict()
        
    def add(self, rule):
        self.rules.append(rule)


    def delete(self, rule):
        del self.rules[self.rules.index(rule)]


    def check_programme(self, major, programme):
        results = list()
        print self.name, 'rules'
        for rule in self.rules:
            print rule
            result = rule.check(programme, self.schedule)
            print result
            results.append(result)

        print major, 'rules'
        for rule in self.schedule[major][1]:
            print rule
            result = rule.check(programme, self.schedule[major][0])
            print result
            results.append(result)
            
        return all(results) and len(result) > 0

    def __str__(self):
        return str(self.rules)


class Rule(object):
    def __init__(self):
        self.t = None
    
    def check(self, programme, schedule=None):
        raise NotImplementedError("Rule.check has not been implemented")
    





class LimitRule(Rule):
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

    def check(self, programme, schedule=None):
        
        if self.inschedule == None:
            #assuming all items are papers codes
            tmp = [x for x in programme if int(float(x)*10)%10*100 == self.level]
            #assume all papers are single semester so worth 15 points
            return self.points >= (len(tmp) * 15)
        else:
            if self.inschedule == False and schedule != None:
                if isinstance(schedule, dict):
                    tmp = [x[0] for x in schedule.values()]
                    tmp2 = list()
                    for papers in tmp:
                        tmp2.extend(papers)
                    tmp2.sort()
                    tmp3 = [x[0] for x in tmp2]
                    not_inschedule_papers = [x for x in programme if x not in tmp3]

                    return self.points >= (len(not_inschedule_papers) * 15)
                else:
                    raise NotImplementedError("Not done schedule that is a list yet")





class AtLeastRule(LimitRule):
    def __str__(self):
        return "At least %d points at %d level" % (self.points, self.level)


    def check(self, programme, schedule=None):
        if self.inschedule == None:
            #assuming all items are papers codes
            tmp = [x for x in programme if int(float(x)*10)%10*100 == self.level]
            #assume all papers are single semester so worth 15 points
            return self.points <= (len(tmp) * 15)
        else:
            if self.inschedule == True and schedule != None:
                tmp = [x for x in programme if int(float(x)*10)%10*100 == self.level]

                if isinstance(schedule, list) or isinstance(schedule, tuple):
                    tmp2 = [x for x in schedule if x in tmp]
                    return self.points <= (len(tmp2) * 15)
                elif isinstance(schedule, dict):
                    papers = list()
                    for x in schedule.values():
                        papers.extend(x)
                    papers.sort()
                    papers = [x for x in papers]

                    return self.points <= (len(tmp2) * 15)
                    
                else:
                    raise NotImplementedError("Not done schedule that is a dict yet")



class RequiredRule(Rule):
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
                    


    def check(self, programme, schedule=None):
        result = False
        if self.inschedule == None or self.inschedule == False:
            # assume have a list of papers to do
            # figure out what these papers are
            result = check(self.papers, programme)
            pass
        elif self.inschedule != None and self.inschedule == True and schedule != None:
            set_inschedule(True)
            result = check(self.papers, programme, schedule)
            set_inschedule(None)
        return result
        #raise NotImplementedError("Not Implemented check in Required rule")
