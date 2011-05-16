import sys

Xpath = False

try:
    from lxml import etree
    Xpath = True
except:
    import xml.etree.ElementTree as etree

from to_tag import get_xml

if __name__ == '__main__' and len(sys.argv) > 1:
    root = etree.XML(get_xml(sys.argv[1]))
    for code in root.findall('./tag/code'):
        if code.text.startswith('p'):
            ncode = code.text[1:]
            ocode = code.text
            code.text = ncode
            print 'change %s to %s' % (ocode, ncode)

    with open(sys.argv[1], 'w') as out:
        out.write(etree.tostring(root))
        
