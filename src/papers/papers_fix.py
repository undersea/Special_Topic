#!/usr/bin/env python

import sys

try:
    from lxml import etree
    Xpath = True
except:
    import xml.etree.ElementTree as etree

from to_tag import get_xml

if __name__ == '__main__' and len(sys.argv) > 1:
    root = etree.XML(get_xml(sys.argv[1]))
    for paper in root.findall('./paper'):
        code = etree.Element('code')
        code.text = paper.attrib['code'][1:]
        paper.insert(0, code)
        paper.insert(3, etree.Element('campus'))
        paper.insert(4, etree.Element('semester'))
        
    with open(sys.argv[1], 'w') as out:
        if Xpath:
            out.write(etree.tostring(root, encoding='utf-8', xml_declaration=True, pretty_print=True, doctype='<!DOCTYPE papers SYSTEM "papers.dtd">'))
        else:
            out.write(etree.tostring(root))
