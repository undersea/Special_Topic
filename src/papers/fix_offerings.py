import sys
from lxml import etree
from lxml import html
#from urllib2 import urlopen

URL = 'http://www.massey.ac.nz/massey/learning/programme-course-paper/paper.cfm?paper_code=%s'

if __name__ == '__main__' and len(sys.argv) > 1:
    papers = etree.parse(sys.argv[1])
    for paper in papers.findall('./paper'):
        paper.remove(paper.find('./campus'))
        paper.remove(paper.find('./semester'))
        root = html.parse(URL % (paper.find('./code').text))
        table = root.find('.//table[@class="tbloffering"]')
        try:
            for tr in table.findall('./tr')[1:]:
                offering = etree.Element('offering')
                tds = tr.findall('./td')
                mode = etree.Element('mode')
                mode.text = str(tds[1].text != None).replace('False', '') and tds[1].text.replace('\n', '').strip()
                offering.append(mode)
                campus = etree.Element('campus')
                campus.text = str(tds[3].text != None).replace('False', '') and tds[3].text.replace('\r', '').strip()
                offering.append(campus)
                semester = etree.Element('semester')
                semester.text = str(tds[2].text != None).replace('False', '') and tds[2].text.replace('\r', '').strip()
                offering.append(semester)
                paper.find('./points').addnext(offering)
        except:
            pass
    print etree.tostring(papers)
