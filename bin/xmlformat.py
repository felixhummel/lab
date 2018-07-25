#!/usr/bin/env python
# encoding: utf-8
import sys
import xml.etree.ElementTree as ET

filename = sys.argv[1]

ET.parse(filename).write(filename)
