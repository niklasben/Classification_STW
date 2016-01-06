# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 11:29:09 2015

@author: Niklas Bendixen

Why do you want to do it that way?
(http://programmingexcuses.com/)
"""

import os                                       # https://docs.python.org/2/library/os.html
import fnmatch                                  # https://docs.python.org/2/library/fnmatch.html
import re                                       # https://docs.python.org/2/library/re.html
import shutil                                   # https://docs.python.org/2/library/shutil.html


# Check if Working File Directory exists. If not, create it.
if not os.path.exists('../Files_Working_Directory'):
    os.makedirs('../Files_Working_Directory')
# Check if Files_3  Directory exists. If not, create it.
if not os.path.exists('../Files_3'):
    os.makedirs('../Files_3')

# Removing CSS from the crawled Files
for dirpath, dirs, files in os.walk('../Files_Crawled'):
    for filename in fnmatch.filter(files, '*_crawled.xml_clean.xml'):
        with open('../Files_Crawled/'+filename, 'r') as originalfile, 
        open('../Files_Working_Directory/'+filename[:-21]+'ohne_css_test.xml', 'w') as testfile:
            for line in originalfile:
                if line.strip():
                    line = re.sub(r'[\w]*[:|.|#][\w]*[ ]?{[\w\W]*}', '', line, re.M)
                    testfile.write(line)


# Removing German Stopwords from the Files.
stopwords = []
# Download Link to the German Stopword List that is used here:
# http://members.unine.ch/jacques.savoy/clef/germanST.txt
with open('stopwords_german.txt', 'r') as stopwords_file:
    for line in stopwords_file:
        stopwords.append(line.strip())

# Check if Saving File Directory 3 exists. If not, create it.
if not os.path.exists('../Files_3'):
    os.makedirs('../Files_3')

for dirpath, dirs, files in os.walk('../Files_Working_Directory'):
    for filename in fnmatch.filter(files, '*_ohne_css_test.xml'):
        with open('../Files_Working_Directory/'+filename, 'r') as originalfile, 
        open('../Files_3/'+filename[:-8]+'ohne_stop.xml', 'w') as testfile:
                for line in originalfile:
                    line = line.split()
                    for n in line:
                        if n in stopwords:
                            pass
                        else:
                            testfile.write(n + ' ')


# Replace whatever is written for German Umlaute with the correct German Letter.
replacements_uml = {
                    '\\xe4': 'ä',
                    '\\xfc': 'ü',
                    '\\xf6': 'ö',
                    '\\xdf': 'ß'
                    }

for dirpath, dirs, files in os.walk('../Files_Working_Directory'):
    for filename in fnmatch.filter(files, '*_ohne_css_test_ohne_stop.xml'):
        with open('../Files_Working_Directory/'+filename, 'r') as openfile, 
        open('../Files_3/'+filename[:-27]+'test_three.xml', 'w') as newfile:
            for line in openfile:
                for src, target in replacements_uml.iteritems():
                    line = line.replace(src, target)
                newfile.write(line)


# Remove unnecessary Working Files including Directory.
shutil.rmtree('../Files_Working_Directory')