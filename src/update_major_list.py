#!/usr/bin/env python

import sys
try:
    from lxml import etree
except:
    import xml.etree.ElementTree as etree

def get_xml(filename):
    return etree.parse(filename)

def add_major(schedule, major, major_id):
    """
    @param schedule - the schedule element from the degree element
    @param major - the name of the major to add
    @param major_id - the id used to identify the major in the tags xml file
    """
    major_tag = etree.Element('major')

    name = etree.Element('name')
    name.text = major

    major_tag.append(name)

    tag = etree.Element('tag')
    tag.set('name', major_id)
    
    major_tag.append(tag)

    schedule.append(major_tag)



def has_major(schedule, major_id):
    for tag in schedule.findall('./major/tag'):
        if tag.get('name') == major_id:
            return True

    return False


if __name__ == '__main__' and len(sys.argv) > 2:
    degree = get_xml(sys.argv[1])
    schedule = degree.find('./schedule')
    tags = get_xml(sys.argv[2])
    for tag in tags.findall('./tag'):
        if tag.get('type') != 'template' and not has_major(schedule, tag.get('name')):
            add_major(schedule, tag.find('./name').text, tag.get('name'))

    print etree.tostring(degree)
