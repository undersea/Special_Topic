"""
Given a Template decide on what papers need doing and print out a suggestion as to what they need to do.
"""
import operators as op
from grammar import *

def suggest(programme, template):
    parse_tags('papers/tags.xml')
    templates = dict([(x, tagsdict[x]) for x in tagsdict if tagsdict[x][2] == 'template'])
    print templates[template]



def get_required(paper, programme):
    '''
    returns the required papers a student has to do in order to do a paper
    '''
    print paper['prerequisites'].check(programme)
    missing = [x for x in op.missing]
    while not paper['prerequisites'].check(programme):
        try:
            tmp = missing.pop()
        
            if 'x' not in tmp:
                programme.append(tmp)
            else:
                
        except:
            break
        
    op.reset_missing()
    print paper['prerequisites'].check(programme)
    


if __name__ == '__main__':
    papers = parse_papers('papers/papers.xml')
    programme = []
    suggest(programme, 'programming')
    get_required(papers['161.326'], [])
    print op.missing
    print programme
