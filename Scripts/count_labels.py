# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 17:38:31 2015

@author: Niklas Bendixen

It worked yesterday
(http://programmingexcuses.com/)
"""

import os                                       # https://docs.python.org/2/library/os.html
import fnmatch                                  # https://docs.python.org/2/library/fnmatch.html
import re                                       # https://docs.python.org/2/library/re.html
import rdflib                                   # https://rdflib.readthedocs.org/en/stable/
import rdflib.plugins.sparql as sparql          # https://rdflib.readthedocs.org/en/stable/apidocs/rdflib.plugins.sparql.html#module-rdflib.plugins.sparql
from rdflib import Graph                        # https://rdflib.readthedocs.org/en/stable/apidocs/rdflib.html#module-rdflib.graph
from rdflib.namespace import Namespace, SKOS    # https://rdflib.readthedocs.org/en/stable/apidocs/rdflib.html#module-rdflib.namespace


# 5. Processing STW Files to get skos:prefLabel
GBV = Namespace('http://purl.org/ontology/gbv/#')
STW = Namespace('http://zbw.eu/stw/')
ZBWTEXT = Namespace('http://zbw.eu/namespaces/zbw-extensions/')

g = Graph()
# Download Link to the RDF File from the STW Thesaurus for Economics that is used here: http://zbw.eu/stw/versions/latest/download/about.en.html
g.parse('stw.rdf', format='xml')

q_pref = sparql.prepareQuery('SELECT ?o WHERE { ?s ?pref ?o . }')
q_alt= sparql.prepareQuery('SELECT ?x WHERE { ?s ?alt ?o . ?s ?pref ?x . FILTER (lang(?x) = "de")}')

pref = SKOS.prefLabel
alt = SKOS.altLabel

with open('labels_counted.tex', 'w') as texfile:
    for dirpath, dirs, files in os.walk('../Files_Working_Directory'):
        texfile.write('% Beginn Anhang Liste Label\n')
        texfile.write('%\n')
        texfile.write('\\section{Anzahl prefLabel und altLabel bei gecrawlten Websites}\\label{sec:listelabel}\n')
        texfile.write('\\begin{longtable}{|m{0.5cm}|m{6cm}|m{2cm}|m{2cm}|m{2cm}|}\n')
        texfile.write('\t\\caption{Liste prefLabel und altLabel bei gecrawlten Websites}\\label{tbl:label}\\\\%Verweis im Text mittels \\ref{tbl:label}\n')
        texfile.write('\t\\hline\n')
        texfile.write('\t\\textbf{Nr.} & \\textbf{Website} & \\textbf{prefLabel} & \\textbf{altLabel} & \\textbf{Gesamt} \\\\\n')
        texfile.write('\t\hline \\hline\n')
        count_file = 0
        count_nr = 0
        for filename in fnmatch.filter(files, '*_ohne_css_xml_stop_tagged_stw2.xml'):
            count_nr = count_nr+1
        for filename in fnmatch.filter(files, '*_ohne_css_xml_stop_tagged_stw2.xml'):
            with open('../Files_Working_Directory/'+filename, 'r') as openfile:
                count_file = count_file+1
                alt_count = 0
                pref_count = 0
                for n in openfile:
                    n = n.strip().split('\t')
                    if re.match(r'[NN|NE]', n[1]):
                        o = rdflib.Literal(n[0], lang='de')
                        q_pref_res = g.query(q_pref, initBindings={'pref' : pref, 'o' : o})
                        if len(q_pref_res) == 1:
                           for row in g.query(q_pref, initBindings={'pref' : pref, 'o' : o}):
                               pref_count = pref_count+1
                        elif len(q_pref_res) == 0:
                            q_alt_res = g.query(q_alt, initBindings={'alt' : alt, 'o' : o, 'pref' : pref})
                            if len(q_alt_res) == 1:
                                alt_count = alt_count+1

            alt_pref_count = alt_count + pref_count
            # Underscores in the Filename need to be supplemented with a Backslash manually, forgot the if-Sequence ('_' -> '\_')
            texfile.write('\t' + str(count_file) + ' & ' + str(filename[:-34]) + ' & ' + str(pref_count) + ' & ' + str(alt_count) + ' & ' + str(alt_pref_count) + '\\\\\n')
            if count_file < count_nr:
                texfile.write('\t\\hline\n')
            else:
                texfile.write('\t\\lasthline\n')
    texfile.write('\\end{longtable}\n')
    texfile.write('%\n')
    texfile.write('% Ende Anhang Liste Label')