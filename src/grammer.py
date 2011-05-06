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
            pass

    rules.name = tree.find('./name').text
    rules.points = int(tree.find('./points').text)
    rules.rules = parserules(tree)
    rules.schedule = parseschedule(tree)
    
    return rules

def parserules(tree):
    rules = list()
    for rule in tree.findall('./rules/rule'):
        limit = rule.find('./limit')
        atleast = rule.find('./atleast')
        required = rule.find('./required')
        if limit != None:
            rules.append(parselimit(limit))
        elif atleast != None:
            rules.append(parseatleast(atleast))
        elif required != None:
            rules.append(parserequired(required))
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
            rule.papers.append(code.text)
        
    andpaper = required.findall('./and')
    if andpaper != None:
        tmp = list()

    orpaper = required.findall('./or')
    oneof = required.findall('./oneof')
    anypaper = required.findall('./any')
    
    return rule




def parseand(andpaper):
    tmp = ['and']
    
    code = andpapers.findall('./code')
    if code != None:
        for x in code:
            tmp.append(x.text)
            
    orpapers = andpapers.findall('./or')
    if orpapers != None:
        tmp.append(parseor(orpapers))
        
    anypapers = andpapers.findall('./any')
    if anypapers != None:
        tmp.append(parseany(anypapers))

    return tuple(tmp)



def parseor(orpapers):
    tmp = ['or']

    code = orpapers.findall('./code')
    if code != None:
        for x in code:
            tmp.append(x.text)

    andpapers = orpapers.findall('./and')
    if andpapers != None:
        parseand(andpapers)
    
    anypapers = orpapers.findall('./any')
    if anypapers != None:
        tmp.append(parseany(anypapers))

    return tuple(tmp)

def parseany(anypapers):
    tmp = ['any']

    code = anypapers.findall('./level')
    if code != None:
        for x in code:
            tmp.append(x.text)

    return tuple(tmp)



def parseschedule(tree):
    schedule = dict()
    for schedule in tree.findall('./degree/schedule/major'):
        pass

    return schedule

if __name__ == "__main__":
    for rule in parse("BSc.xml").rules:
        print rule
