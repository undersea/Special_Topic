from lxml import etree

from paper_rules import PrerequisiteRule, CorequisiteRule, RestrictedRule

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
