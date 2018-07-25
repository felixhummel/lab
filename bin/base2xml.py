#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import xml.etree.ElementTree as ET

pool = os.environ['pool']
assert pool, 'need pool in os.environ'

filename = sys.argv[1]
network = sys.argv[2]
name = sys.argv[3]

tree = ET.parse(filename)

domain = tree.getroot()

domain.find('name').text = name
domain.find('devices/disk/source').attrib['dev'] = f'/dev/{pool}/{name}'
domain.find('devices/interface/source').attrib['network'] = network

ET.dump(tree)
