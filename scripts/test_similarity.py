# -*- coding: utf-8 -*-

import logging
import os
import argparse
import glob
import json
import csv
from gensim import corpora, models, similarities

import utils 
import similar_articles

parser = argparse.ArgumentParser(description="""Test""")
parser.add_argument('corpus_name', type=str, 
                    help="Le nom du corpus")
parser.add_argument('method', type=str, 
                    help="lda, lsi, tfidf")
parser.add_argument('-v', '--verbose', action='store_true',
                    help="Afficher les messages d'information")
args = parser.parse_args()

corpus_file = args.corpus_name + '_' + args.method + '.mm'
index_file = args.corpus_name + '_' + args.method + '_index'
docid_file = args.corpus_name + '_docid.txt'

tested_articles = [utils.get_article_by_corpus_number(x, docid_file) for x in range(0, 18000, 1000)]

c = csv.writer(open(args.corpus_name + '_' + args.method + '_test', 'wb'))

c.writerow(['Article_de_référence', 'Voisin_n°1', 'Voisin_n°2', 'Voisin_n°3', 'Voisin_n°4', 'Voisin_n°5'])

for id in tested_articles:
    similar = similar_articles.find_similar_articles(args.corpus_name, args.method, id)
    l = [utils.get_article_title_by_id(id, docid_file)]
    l.extend([(utils.get_article_title_by_id(x[0], docid_file), x[1], x[0]) for x in similar])
    c.writerow(l)
    


