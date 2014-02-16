# -*- coding: utf-8 -*-
"""
Génère une page HTML qui affiche les topics d'un corpus
"""
import os
import sys
root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(root_dir) #TODO : faire fonctionner les import relatif (from .. import utils)

import re
import argparse
from django.template import Context, loader
from django.conf import settings

import utils

cur_path = os.path.realpath(os.path.dirname(__file__))
settings.configure(TEMPLATE_DEBUG=True, TEMPLATE_DIRS=([cur_path + '/templates']))

parser = argparse.ArgumentParser(description="""Génère une page HTML qui
affiche les topics du corpus""");
parser.add_argument('topics_file', type=str,
                    help="""Le fichier qui contient les topics. Ce fichier est 
                    généré par le script lda.py""")
arg = parser.parse_args()

corpus_name = re.split(r'_topics', utils.split_path(arg.topics_file)['name'])[0]

topics = []
with open(arg.topics_file) as f:
    for line in f:
        topics.append([eval(x) for x in line[:-1].split('\t')])

template = loader.get_template('topics.html')
context = Context({'corpus': {'name': corpus_name},
                  'topics': topics})

with open(corpus_name + '_topics.html', 'w') as f:
    f.write(template.render(context))