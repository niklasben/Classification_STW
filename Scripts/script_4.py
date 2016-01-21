# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 22:14:13 2016

@author: Niklas Bendixen

We spent three months debugging it because we only had one month to build it
(http://programmingexcuses.com/)
"""

import os                                       # https://docs.python.org/2/library/os.html
import fnmatch                                  # https://docs.python.org/2/library/fnmatch.html
import re                                       # https://docs.python.org/2/library/re.html
import shutil                                   # https://docs.python.org/2/library/shutil.html
import treetaggerwrapper as ttw                 # https://treetaggerwrapper.readthedocs.org/en/latest/
import rdflib                                   # https://rdflib.readthedocs.org/en/stable/
import rdflib.plugins.sparql as sparql          # https://rdflib.readthedocs.org/en/stable/apidocs/rdflib.plugins.sparql.html#module-rdflib.plugins.sparql
from rdflib import Graph                        # https://rdflib.readthedocs.org/en/stable/apidocs/rdflib.html#module-rdflib.graph
from rdflib.namespace import Namespace, SKOS    # https://rdflib.readthedocs.org/en/stable/apidocs/rdflib.html#module-rdflib.namespace


# Check if Working File Directory exists. If not, create it.
if not os.path.exists('../Files_Working_Directory'):
    os.makedirs('../Files_Working_Directory')
# Check if Files_4  Directory exists. If not, create it.
if not os.path.exists('../Files_4'):
    os.makedirs('../Files_4')


# Removing XML-Structure and CSSfrom crawled Files.
replacements = {
                '<?xml version="1.0" encoding="utf-8"?>':'',
                '<root>':'',
                '<item>':'',
                '<fragment>':'',
                '</fragment>':'',
                '</item>':'',
                '</root>':''
                }

for dirpath, dirs, files in os.walk('../Files_Crawled'):
    for filename in fnmatch.filter(files, '*_crawled.xml_clean.xml'):
        with open('../Files_Crawled/'+filename, 'r') as originalfile, 
        open('../Files_Working_Directory/'+filename[:-21]+'ohne_css_test.xml', 'w') as testfile, #### ?????????
        open('../Files_Working_Directory/'+filename[:-21]+'ohne_css_stw.xml', 'w') as stwfile:
            for line in originalfile:
                if line.strip():
                    line = re.sub(r'[\w]*[:|.|#][\w]*[ ]?{[\w\W]*}', '', line, re.M)
                    testfile.write(line)
                    stwfile.write(line)

for dirpath, dirs, files in os.walk('../Files_Working_Directory'):
    for filename in fnmatch.filter(files, '*_ohne_css_stw.xml'):
        with open('../Files_Working_Directory/'+filename, 'r') as originalfile, 
        open('../Files_Working_Directory/'+filename[:-7]+'xml_stw.xml', 'w') as stwfile:
                for line in originalfile:
                    for src, target in replacements.iteritems():
                        line = line.replace(src, target)
                    stwfile.write(line)


# Removing German Stopwords from the Files.
stopwords = []
# Download Link to the German Stopword List that is used here:
# http://members.unine.ch/jacques.savoy/clef/germanST.txt
with open('stopwords_german.txt', 'r') as stopwords_file:
    for line in stopwords_file:
        stopwords.append(line.strip())

for dirpath, dirs, files in os.walk('../Files_Working_Directory'):
    for filename in fnmatch.filter(files, '*_ohne_css_test.xml'):
        with open('../Files_Working_Directory/'+filename, 'r') as originalfile, 
        open('../Files_Working_Directory/'+filename[:-8]+'stop_test.xml', 'w') as testfile:
                for line in originalfile:
                    line = line.split()
                    for n in line:
                        if n in stopwords:
                            pass
                        else:
                            testfile.write(n + ' ')

for dirpath, dirs, files in os.walk('../Files_Working_Directory'):
    for filename in fnmatch.filter(files, '*_ohne_css_xml_stw.xml'):
        with open('../Files_Working_Directory/'+filename, 'r') as originalfile, 
        open('../Files_Working_Directory/'+filename[:-7]+'stop_stw.xml', 'w') as stwfile:
            for line in originalfile:
                line = line.split()
                for n in line:
                    if n in stopwords:
                        pass
                    else:
                        stwfile.write(n + ' ')


# Lemmatizing and Tagging German Words.
tagger = ttw.TreeTagger(TAGLANG='de')

for dirpath, dirs, files in os.walk('../Files_Working_Directory'):
    for filename in fnmatch.filter(files, '*_ohne_css_xml_stop_stw.xml'):
        tagger.tag_file_to('../Files_Working_Directory/'+filename, 
        '../Files_Working_Directory/'+filename[:-7]+'tagged_stw.xml')


replace = re.compile(r'^replaced-email|^replaced-dns|^<repemail|^<repdns')
for dirpath, dirs, files in os.walk('../Files_Working_Directory'):
    for filename in fnmatch.filter(files, '*_ohne_css_xml_stop_tagged_stw.xml'):
        with open('../Files_Working_Directory/'+filename, 'r') as originalfile, 
        open('../Files_Working_Directory/'+filename[:-4]+'2.xml', 'w') as stwfile:
            for line in originalfile:
                line = line.strip()
                if replace.search(line) is not None:
                    pass
                else:
                    line = line.split('\t')
                    if len(line) != 3:
                        pass
                    else:
                        stwfile.write(line[0] + '\t' + line[1] + '\t' + line[2] + '\n')


############################

# Processing STW Files to get skos:prefLabel.
GBV = Namespace('http://purl.org/ontology/gbv/#')
STW = Namespace('http://zbw.eu/stw/')
ZBWTEXT = Namespace('http://zbw.eu/namespaces/zbw-extensions/')

g = Graph()
# Download Link to the RDF File from the STW Thesaurus for Economics that is used here: 
# http://zbw.eu/stw/versions/latest/download/about.en.html
g.parse('stw.rdf', format='xml')

q_pref = sparql.prepareQuery('SELECT ?o WHERE { ?s ?pref ?o . }')
q_alt= sparql.prepareQuery('SELECT ?x WHERE { ?s ?alt ?o . ?s ?pref ?x . FILTER (lang(?x) = "de")}')

pref = SKOS.prefLabel
alt = SKOS.altLabel

for dirpath, dirs, files in os.walk('../Files_Working_Directory'):
    for filename in fnmatch.filter(files, '*_ohne_css_xml_stop_tagged_stw2.xml'):
        with open('../Files_Working_Directory/'+filename, 'r') as openfile, 
        open('../Files_Working_Directory/'+filename[:-33]+'nur_pref_stw.xml', 'w') as preffile, 
        open('../Files_Working_Directory/'+filename[:-33]+'tag_und_pref_stw.xml', 'w') as tagfile:
            for n in openfile:
                n = n.strip().split('\t')
                if re.match(r'[NN|NE]', n[1]):
                    o = rdflib.Literal(n[0], lang='de')

                    q_pref_res = g.query(q_pref, initBindings={'pref' : pref, 'o' : o})

                    if len(q_pref_res) == 1:
                       for row in g.query(q_pref, initBindings={'pref' : pref, 'o' : o}):
                            preffile.write(n[0] + '\n')
                            tagfile.write(n[0] + '\t' + n[1] + '\t' + str(row) + '\n')
                    elif len(q_pref_res) == 0:
                        q_alt_res = g.query(q_alt, initBindings={'alt' : alt, 'o' : o, 'pref' : pref})
                        if len(q_alt_res) == 1:
                            for row in g.query(q_alt, initBindings={'alt' : alt, 'o' : o, 'pref' : pref}):
                                preffile.write(str(row) + '\n')
                                tagfile.write(n[0] + '\t' + n[1] + '\t' + str(row) + '\n')


# Remove Strings from STW Files to get only skos:prefLabel in the Files.
replacements_stw = {
                    '(rdflib.term.Literal(u\'': '',
                    '\', lang=u\'de\'),)': '',
                    '\', lang=\'de\'),)': ''
                    }
replacements_stw = dict((re.escape(k), v) for k, v in replacements_stw.iteritems())
pattern = re.compile('|'.join(replacements_stw.keys()))

for dirpath, dirs, files in os.walk('../Files_Working_Directory'):
    for filename in fnmatch.filter(files, '*_nur_pref_stw.xml'):
        with open('../Files_Working_Directory/'+filename, 'r') as openfile, 
        open('../Files_Working_Directory/'+filename[:-7]+'clean_stw.xml', 'w') as newfile:
            for line in openfile:
                line = pattern.sub(lambda m: replacements_stw[re.escape(m.group(0))], line)
                newfile.write(line)

for dirpath, dirs, files in os.walk('../Files_Working_Directory'):
    for filename in fnmatch.filter(files, '*_tag_und_pref_stw.xml'):
        with open('../Files_Working_Directory/'+filename, 'r') as openfile, 
        open('../Files_Working_Directory/'+filename[:-7]+'clean_stw.xml', 'w') as newfile:
            for line in openfile:
                line = pattern.sub(lambda m: replacements_stw[re.escape(m.group(0))], line)
                newfile.write(line)



# # # ADD skos:prefLabel to every Label with an added $pref_ in front of it # # #

# Replace skos:altLabel with skos:prefLabel in the Files.
for dirpath, dirs, files in os.walk('../Files_Working_Directory'):
    for filename in fnmatch.filter(files, '*_ohne_css_stop_test.xml'):
        with open('../Files_Working_Directory/'+filename, 'r') as openfile, 
        open('../Files_Working_Directory/'+filename[:-22]+'pref_ersetzt.xml', 'w') as newfile:
            for dirpath2, dirs2, files2 in os.walk('../Files_Working_Directory'):
                for filename2 in fnmatch.filter(files2, filename[:-22]+'tag_und_pref_clean_stw.xml'):
                    prefLabel = {}
                    with open('../Files_Working_Directory/'+filename2, 'r') as prefLabelFile:
                        for line in prefLabelFile:
                            line = line.split()
                            prefLabel[line[0]] = line[2]
            for line in openfile:
                line = line.split()
                for i in line:
                    for key, value in prefLabel.items():
                        if i in key:
                            i = value
                    newfile.write(i + ' ')


# Replace whatever is written for German Umlaute with the correct German Letter.
replacements_uml = {
                    '\\xe4': 'ä',
                    '\\xfc': 'ü',
                    '\\xf6': 'ö',
                    '\\xdf': 'ß'
                    }

for dirpath, dirs, files in os.walk('../Files_Working_Directory'):
    for filename in fnmatch.filter(files, '*_pref_ersetzt.xml'):
        with open('../Files_Working_Directory/'+filename, 'r') as openfile, 
        open('../Files_Machine_Learning/fulltext/'+filename[:-16]+'fulltext.xml', 'w') as newfile:
            for line in openfile:
                for src, target in replacements_uml.iteritems():
                    line = line.replace(src, target)
                newfile.write(line)

for dirpath, dirs, files in os.walk('../Files_Working_Directory'):
    for filename in fnmatch.filter(files, '*_nur_pref_clean_stw.xml'):
        with open('../Files_Working_Directory/'+filename, 'r') as openfile, 
        open('../Files_Working_Directory/'+filename[:-22]+'_nur_pref_clean_uml_stw.xml', 'w') as newfile:
            for line in openfile:
                for src, target in replacements_uml.iteritems():
                    line = line.replace(src, target)
                newfile.write(line)

# Restructuring the Files with the skos:prefLabel only to make them readable by RapidMiner.
for dirpath, dirs, files in os.walk('../Files_Working_Directory'):
    for filename in fnmatch.filter(files, '*_nur_pref_clean_uml_stw.xml'):
        with open('../Files_Working_Directory/'+filename, 'r') as openfile, 
        open('../Files_4/'+filename[:-26]+'test_four.xml', 'w') as newfile:
            newfile.write('<?xml version="1.0" encoding="utf-8"?>\n <root>\n')
            for line in openfile:
                line = line.strip()
                newfile.write('<item> ' + line + ' </item>\n')
            newfile.write('</root>')


##################################


# Remove unnecessary Working Files including Directory.
shutil.rmtree('../Files_Working_Directory')