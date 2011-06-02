from xml.etree.ElementTree import ElementTree, fromstring
from rules import Degree, LimitRule, AtLeastRule, RequiredRule
from paper_rules import *
#from paper_grammer import parseretrictions, parsecorequisites, parseprerequisites

class UnknownElementException(Exception):
    pass


tagsdict = dict()

def parse_tags(source):
    global tagsdict
    tagstree = None
    try:
        tagstree = ElementTree()
        tagstree.parse(source)
    except IOError, e:
        try:
            tagstree = fromstring(source)
        except Exception, er:
            print e
            print er
            return
    for tag in tagstree.findall('./tag'):
        description = tag.find('./description').text
        papers = [paper.text for paper in tag.findall('./code')]
        tagsdict[tag.attrib['name']] = (description, papers)


def parse(source):
    rules = None
    tree = None
    try:
        tree = ElementTree()
        tree.parse(source)
        rules = Degree()
    except IOError, e:
        try:
            tree = fromstring(source)
            rules = Degree()
            
        except Exception, er:
            print e
            print er
            return None

    rules.name = tree.find('./name').text
    rules.points = int(tree.find('./points').text)
    rules.rules = parserules(tree)
    rules.schedule = parseschedule(tree)
    
    return rules

def parserules(tree):
    rules = list()
    inschedule = False
    if not isinstance(tree, ElementTree) and tree.tag == 'major':
        inschedule = True
    for rule in tree.findall('./rules/rule'):
        limit = rule.find('./limit')
        atleast = rule.find('./atleast')
        required = rule.find('./required')
        if limit != None:
            rule = parselimit(limit)
            if inschedule:
                rule.inschedule = True
            rules.append(rule)
        elif atleast != None:
            rule = parseatleast(atleast)
            if inschedule:
                rule.inschedule = True
            rules.append(rule)
        elif required != None:
            rule = parserequired(required)
            
            rules.append(rule)
        else:
            raise UnknownElementException()
        
            

    return rules



def parselimit(limit):
    rule = LimitRule()
    rule.points = int(limit.find('./points').text)
    notinschedule = limit.find('./notinschedule')
    if notinschedule != None:
        rule.inschedule = False
    else:
        rule.level = int(limit.find('./level').text)
    
    return rule

def parseatleast(atleast):
    rule = AtLeastRule()
    rule.points = int(atleast.find('./points').text)
    rule.level = int(atleast.find('./level').text)
    
    return rule


def parserequired(required):
    rule = RequiredRule()

    inschedule = required.find('./inschedule')
    if inschedule != None:
        rule.inschedule = True
        points = required.find('./points')
        if points != None:
            rule.points = int(points.text)
        else:
            orcode = required.find('./or')
            if orcode != None and 'required' in orcode.keys():
                rule.papers.append(int(orcode.get('required')))
                return rule
                
    
    code = required.findall('./code')
    if code != None:
        tmp = list()
        for x in code:
            rule.papers.append(x.text)
        
    andpaper = required.findall('./and')
    if andpaper != None:
        t = parseand(andpaper)
        if len(t) > 0:
            rule.papers.append(t)

    orpaper = required.findall('./or')
    if orpaper != None:
        t = parseor(orpaper)
        if len(t) > 0:
            rule.papers.append(t)
        
    oneof = required.findall('./oneof')
    
    anypaper = required.findall('./any')
    
    return rule




def parseand(andpaper):
    tmp = []
    if isinstance(andpaper, list):
        for x in andpaper:
            tmp.append(parseand(x))
            
        return tuple(tmp)

    tmp.append('and')
    
    code = andpaper.findall('./code')
    if code != None:
        for x in code:
            tmp.append(x.text)
            
    orpapers = andpaper.findall('./or')
    if orpapers != None:
        tmp.append(parseor(orpapers))
        
    anypapers = andpaper.findall('./any')
    if anypapers != None:
        tmp.append(parseany(anypapers))

    return tuple(tmp)



def parseor(orpapers):
    tmp = []

    if isinstance(orpapers, list):
        for x in orpapers:
            tmp.append(parseor(x))
        return tuple(tmp)

    tmp.append("or")
    code = orpapers.findall('./code')
    if code != None:
        for x in code:
            tmp.append(x.text)

    andpapers = orpapers.findall('./and')
    if andpapers != None and len(andpapers) > 0:
        parseand(andpapers)
    
    anypapers = orpapers.findall('./any')
    if anypapers != None and len(anypapers) > 0:
        tmp.append(parseany(anypapers))

    return tuple(tmp)

def parseany(anypapers):
    tmp = []

    if isinstance(anypapers, list):
        for x in anypapers:
            tmp.append(parseany(x))
        return tuple(tmp)

    tmp.append('any')
    code = anypapers.findall('./level')
    if code != None:
        for x in code:
            tmp.append(x.text)

    return tuple(tmp)



def parseschedule(tree):
    schedule = dict()
    for major in tree.findall('./schedule/major'):
        name = major.find('./name').text

        tagname = major.find('./tag').attrib['name']
        papers = tagsdict[tagname][1]        
        rules = parserules(major)
        

        schedule[name] = (tuple(papers), rules)

    return schedule



def get_paper_offerings(paper):
    return [(offering.find('./mode').text,
             offering.find('./campus').text,offering.find('./semester').text) for offering in paper.findall('./offering')]



def paper_code_name_points(paper):
    code = paper.find('./code').text
    name = paper.find('./name').text
    points = float(paper.find('./points').text)
    offerings = get_paper_offerings(paper)
    
    prerequisites = paper.find('./prerequisite') and parseprerequisites(code, paper.find('./prerequisite'))
    corequisites = paper.find('./corequisite') and parsecorequisites(code, paper.find('./corequisite'))
    restriction = paper.find('./restriction') and parseretrictions(code, paper.find('./restriction'))
    
    

    return code, name, points, offerings, prerequisites, corequisites, restriction


def parse_papers(source):
    tagstree = None
    paperdict = dict()
    try:
        tagstree = ElementTree()
        tagstree.parse(source)
    except IOError, e:
        try:
            tagstree = fromstring(source)
        except Exception, er:
            print e
            print er
            return None

    for paper in tagstree.findall('./paper'):
        tmp = paper_code_name_points(paper)
        paperdict[tmp[0]] = tmp

    return paperdict



def parseprerequisites(id, required):
    rule = PrerequisiteRule(id)
    code = required.findall('./code')
    if code != None:
        tmp = list()
        for x in code:
            rule.papers.append(x.text)
        
    andpaper = required.findall('./and')
    if andpaper != None:
        t = parseand(andpaper)
        if len(t) > 0:
            rule.papers.append(t)

    orpaper = required.findall('./or')
    if orpaper != None:
        t = parseor(orpaper)
        if len(t) > 0:
            rule.papers.append(t)
        
    oneof = required.findall('./oneof')
    
    anypaper = required.findall('./any')
    
    return rule



def parsecorequisites(id, required):
    rule = CorequisiteRule(id)
    code = required.findall('./code')
    if code != None:
        tmp = list()
        for x in code:
            rule.papers.append(x.text)
        
    andpaper = required.findall('./and')
    if andpaper != None:
        t = parseand(andpaper)
        if len(t) > 0:
            rule.papers.append(t)

    orpaper = required.findall('./or')
    if orpaper != None:
        t = parseor(orpaper)
        if len(t) > 0:
            rule.papers.append(t)
        
    oneof = required.findall('./oneof')
    
    anypaper = required.findall('./any')
    
    return rule


def parseretrictions(id, required):
    rule = RestrictedRule(id)
    code = required.findall('./code')
    if code != None:
        tmp = list()
        for x in code:
            rule.papers.append(x.text)
        
    return rule


if __name__ == "__main__":
    parse_tags('papers/tags.xml')
    print tagsdict['compsci']
    degree = parse("BSc.xml")
    print degree.name
    print degree.points
    programme = ['117.152', '119.258', '189.251', '119.177', '159.201', '159.202', '159.233', '159.253']
    result = degree.check_programme('Computer Science', programme)
    print 'passed rules =', result

    papers = parse_papers('papers/papers.xml')
    for paper in papers:
        print paper, papers[paper][5] == None or papers[paper][4].check(programme[2:])

    print
    #print papers['161.326']
    print papers['161.326'][4].papers#.check(['161.201', '159.201'])
    #print papers['161.326'][5]
    #print papers['161.326'][6]
    
