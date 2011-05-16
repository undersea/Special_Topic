"""
Takes a papers xml file and outputs a tags xml file
"""

import sys

Xpath = False

try:
    from lxml import etree
    Xpath = True
except:
    import xml.etree.ElementTree as etree


print Xpath

def get_xml(f):
    with open(f) as inp:
        return inp.read()


if __name__ == '__main__' and len(sys.argv) > 3:
    from_root = etree.XML(get_xml(sys.argv[1]))
    to_root = etree.XML(get_xml(sys.argv[2]))
    if Xpath:
        to_tag = to_root.find('./tag[@name="%s"]' % (sys.argv[3]))
    else:
        try:
            to_tag = [x for x in to_root.findall('./tag') if x.get('name') == sys.argv[3]][0]
        except:
            to_tag = None

    if to_tag is None:
        to_tag = etree.Element('tag')
        to_tag.set('name', sys.argv[3])
        descrip = etree.Element('description')
        descrip.text = sys.argv[3]
        to_tag.append(descrip)
        to_root.append(to_tag)
        

    for paper in from_root.findall('./paper'):
        code = paper.get('code')
        to_tag.append(etree.XML('<code>%s</code>\n' % (code)))
        
    with open(sys.argv[2], 'w') as out:
        out.write(etree.tostring(to_root))
        print 'done'
