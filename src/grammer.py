'''

'''

from xml.etree.ElementTree import ElementTree, fromstring
from rules import Degree, LimitRule, AtLeastRule, RequiredRule

class UnknownElementException(Exception):
    pass

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
        tmp.append(parseor(orpaper))
        
    anypapers = andpaper.findall('./any')
    if anypapers != None:
        tmp.append(parseany(anypaper))

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
        papers = list()
        for x in major.findall('./paper'):
            papers.append(paper_code_name_points(x))

        rules = parserules(major)
        

        schedule[name] = (tuple(papers), rules)

    return schedule


def paper_code_name_points(paper):
    code = paper.find('./code').text
    name = paper.find('./name').text
    points = float(paper.find('./points').text)

    return code, name, points

if __name__ == "__main__":
    degree = parse("BSc.xml")
    print degree.name
    print degree.points
    for rule in degree.rules:
        print rule
        
        print rule.check(['159.101', '161.101','117.152', '119.258', '189.251', '119.177'], degree.schedule)



    for major in degree.schedule:
        print
        print major
        for paper in degree.schedule[major][0]:
            print paper
        print major, "rules"
        for rule in degree.schedule[major][1]:
            print rule
            
            print rule.check(['159.101', '159.102', '161.101','117.152', '119.258', '189.251', '119.177', '159.201', '159.202', '159.233', '159.253'], degree.schedule[major][0])
