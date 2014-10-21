#!/usr/bin/env python

import os
import sys

from urlparse import urljoin
from os.path import join, abspath, dirname, isfile

from xml.etree import ElementTree as etree

def get_notebooks(tei_data_dir):
    for filename in os.listdir(tei_data_dir):
        filename = join(tei_data_dir, filename)
        if isfile(filename): 
            yield filename

def get_surfaces(path):
    doc = etree.parse(path)
    for inc in doc.findall('.//{http://www.w3.org/2001/XInclude}include'):
        yield urljoin(path, inc.attrib['href'])
    

def main():
    tei_data_dir = sys.argv[1]
    for notebook_path in get_notebooks(tei_data_dir):
        for surface in get_surfaces(notebook_path):
            print surface

# /sga/data/tei/ox/ox-ms_abinger_c56/ox-ms_abinger_c56-0011.xml
# http://shelleygodwinarchive.org/sc/oxford/frankenstein/notebook/a#n=11

if __name__ == "__main__":
    main()
        
