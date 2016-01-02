# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 22:14:13 2016

@author: Niklas Bendixen

It works for me
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

