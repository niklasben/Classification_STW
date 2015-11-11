# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 21:38:24 2015

@author: Niklas Bendixen

Even though it doesn't work, how does it feel?
(http://programmingexcuses.com/)
"""

import os       # https://docs.python.org/2/library/os.html
import fnmatch  # https://docs.python.org/2/library/fnmatch.html

replacements = {
                '<root>':'<root>',
                '<item>':'\n<item>',
                '<fragment>':'\n<fragment>\n',
                '</fragment>':'\n</fragment>',
                '</item>':'\n</item>',
                '</root>':'\n</root>'
                }

for dirpath, dirs, files in os.walk('../Crawler/output'):
    for filename in fnmatch.filter(files, '*.xml'):
        with open('../Crawler/output/'+filename, 'r') as originalfile, open('../Files_Crawled/'+filename+'_clean.xml', 'w') as newfile:
            for line in originalfile:
                for src, target in replacements.iteritems():
                    line = line.replace(src, target)
                newfile.write(line)