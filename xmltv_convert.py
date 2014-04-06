#-*- coding: utf-8 -*-

__author__ = 'Andrey Smirnov'
__email__ = 'mail@ansmirnov.ru'

import sys
import cElementTree as ET
from jinja2 import Template
from datetime import datetime
from dateutil.parser import parse

if len(sys.argv) != 3:
    print "USAGE: python xmltv_convert.py input_filename.xml output_filename"
    sys.exit()

input_file = sys.argv[1]
output_file = sys.argv[2]


class Channel():
    def __init__(self, elem):
        self.elem = elem

    def __getattr__(self, item):
        try:
            if item == 'id':
                return self.elem.get('id')
            if item == 'display_name':
                return self.elem.find('display-name').text
            if item == 'icon':
                return self.elem.find('display-name').get('icon')
        except:
            return ''


class Programme():
    def __init__(self, elem):
        self.elem = elem

    def __getattr__(self, item):
        try:
            if item == 'start':
                return parse(self.elem.get('start'))
            if item == 'stop':
                return parse(self.elem.get('stop'))
            if item == 'duration':
                return self['stop'] - self['start']
            if item == 'channel':
                return self.elem.get('channel')
            if item == 'title':
                return self.elem.find('title').text
            if item == 'category':
                return self.elem.find('category').text
            if item == 'desc':
                return self.elem.find('desc').text
        except:
            return ''


def channels():
    for event, elem in ET.iterparse(input_file):
        if event == "end" and elem.tag == 'channel':
            yield Channel(elem)


def programmes():
    for event, elem in ET.iterparse(input_file):
        if event == "end" and elem.tag == 'programme':
            yield Programme(elem)

template = Template(open('output.tpl', 'rt').read())
open(output_file, 'wt').write(template.render({'channels': channels(), 'programmes': programmes()}).encode('utf8'))
