# -*- coding: utf-8 -*-

"""
Construit "en perspective"

"""

import argparse
import logging
import sys
import json
import glob
import os
from gensim import corpora, similarities, models

import utils
import similar_articles

parser = argparse.ArgumentParser(description="""Ce script construit « en perspective »""")
parser.add_argument('corpus_name', type=str, help="Le nom du corpus contenant les articles")
parser.add_argument('directory', type=str, help='Le nom du dossier contenant les articles')
parser.add_argument('method', type=str, help="La méthode utilisée (lda, lsi, tfidf)")
parser.add_argument('-v', '--verbose', action='store_true',
                    help="Afficher les messages d'information")
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    
results = []

articles = glob.glob(os.path.join(args.directory, '*.txt'))

for article in articles:
    article_content = unicode(open(article).read(), 'utf8')
    similar = similar_articles.find_similar_articles(args.corpus_name, args.method, content=article_content)
    
    results.append(similar)
    
print results
    

