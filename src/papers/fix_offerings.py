import sys
from lxml import etree
from lxml import html
#from urllib2 import urlopen

URL = 'http://www.massey.ac.nz/massey/learning/programme-course-paper/paper.cfm?paper_code=%s'

if __name__ == '__main__' and len(sys.argv) > 0:
    papers = etree.parse(sys.argv[0])
    for paper in papers.findall('./paper'):
        paper.remove(paper.find('./campus'))
        paper.remove(paper.find('./semester'))
        root = html.parse(URL % (paper.find('./code').text))
        table = root.find('.//table[@class="tbloffering"]')
        for tr in table.findall('./tr')[1:]:
            offering = etree.Element('offering')
            tds = tr.findall('./td')
            mode = etree.Element('mode')
            mode.text = tds[1].text
            offering.append(mode)
            
