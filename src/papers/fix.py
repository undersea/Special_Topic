import sys
try:
    from lxml import etree
except:
    import xml.etree.ElementTree as etree

def get_xml():
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as inp:
            return inp.read()
    else:
        return ""

if __name__ == '__main__':
    root = etree.XML(get_xml())
    print root.tag
    for paper in root.findall('./paper'):
        code = paper.find('./code')
        if code != None:
            paper.set('code', 'p%s' % (code.text))
            paper.remove(code)
            print 'Fixed', code.text
        else:
            tmp = paper.get('code')
            if not tmp.startswith('p'):
                paper.set('code', 'p%s' % (tmp))
                print 'fixed %s to %s' % (tmp, paper.get('code'))

    if len(sys.argv) == 2:
        with open(sys.argv[1], 'w') as out:
            out.write(etree.tostring(root, encoding='utf-8', pretty_print=True, xml_declaration=True, doctype='<!DOCTYPE papers SYSTEM "papers.dtd">'))

