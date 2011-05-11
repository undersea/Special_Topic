#Rules definition for degrees and majors


class Degree(object):
    def __init__(self):
        self.rules = list()

        self.name = None

        self.schedule = dict()
        
    def add(self, rule):
        self.rules.append(rule)


    def delete(self, rule):
        del self.rules[self.rules.index(rule)]


    def check_programme(major, programme):
        pass
    

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
            tmp = [x for x in programme if int(float(x)*1000)%1000 == self.level]
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
            tmp = [x for x in programme if int(float(x)*1000)%1000 == self.level]
            #assume all papers are single semester so worth 15 points
            return self.points <= (len(tmp) * 15)
        else:
            if self.inschedule == True and schedule != None:
                tmp = [x for x in programme if int(float(x)*10)%10*100 == self.level]

                if isinstance(schedule, list):
                    tmp2 = [x for x in schedule if x in tmp]
                    return self.points <= (len(tmp2) * 15)
                elif isinstance(schedule, dict):
                    papers = list()
                    for x in schedule.values():
                        papers.extend(x[0])
                    papers.sort()
                    papers = [x[0] for x in papers]

                elif isinstance(schedule, tuple):
                    papers = list()
                    papers = [x[0] for x in schedule]
                    tmp2 = [x for x in papers if x in tmp]

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
                    
    def __or(self, papers, programme):
        results = list()
        for paper in papers:
            if isinstance(paper, tuple):
                if paper[0] == 'and':
                    results.append(self.__and(paper[1:], programme))
                elif paper[0] == 'any':
                    results.append(self.__any(paper[1:], programme))
            else:
                results.append(self.__code(paper, programme))

        

        return any(results)
    

    def __and(self, papers, programme):
        results = list()
        for paper in papers:
            if isinstance(paper, tuple):
                if paper[0] == 'or':
                    results.append(self.__or(paper[1:], programme))
                elif paper[0] == 'any':
                    results.append(self.__any(paper[1:], programme))
            else:
                results.append(self.__code(paper, programme))

        return all(results) and len(results) > 0

    def __code(self, code, programme):
        
        return code in programme or ('x' in code and len([x for x in programme if int(float(code.replace('x', ''))*10) == int(float(x)*10)]) > 0)


    def __oneof(self, papers, programme):
        results = list()
        for paper in papers:
            if isinstance(paper, tuple):
                if paper[0] == 'any':
                    results.append(self.__any(paper[1:], programme))
            else:
                results.append(self.__code(paper, programme))

        return any(results)


    def __any(self, levels, programme):
        results = list()
        for level in levels:
            results.append(int(level) in [int(float(x)*1000%1000) for x in programme])

        return any(results)

    def __rules(self, papers, programme, schedule=None):
        results = list()
        
        if self.inschedule != None and self.inschedule == True:
           if self.points != None:
               pass
           else:
               if schedule != None and isinstance(schedule, dict):
                    tmp = [x[0] for x in schedule.values()]
                    tmp2 = list()
                    for paper in tmp:
                        tmp2.extend(paper)
                    tmp2.sort()
                    tmp3 = [int(float(x[0])) for x in tmp2]
                    inschedule_papers = set([x for x in programme if int(float(x)) in tmp3])

                    return len(inschedule_papers) >= int(papers[0])
        else:
            if isinstance(papers, list):
                for paper in papers:
                    results.append(self.__code(paper, programme))
            else:
                for paper in papers[0]:
                    if isinstance(paper, tuple):
                        if paper[0] == 'and':
                            results.append(self.__and(paper[1:], programme))
                        elif paper[0] == 'any':
                            results.append(self.__any(paper[1:], programme))
                        elif paper[0] == 'oneof':
                            results.append(self.__oneof(paper[1:], programme))
                        elif paper[0] == 'or':
                            results.append(self.__or(paper[1:], programme))
                        
                    else:
                        
                        results.append(self.__code(paper, programme))
        
        return all(results) and len(results) > 0



    def check(self, programme, schedule=None):
        result = False
        if self.inschedule == None or self.inschedule == False:
            # assume have a list of papers to do
            # figure out what these papers are
            result = self.__rules(self.papers, programme)
            pass
        elif self.inschedule != None and self.inschedule == True and schedule != None:
            result = self.__rules(self.papers, programme, schedule)
        return result
        #raise NotImplementedError("Not Implemented check in Required rule")
