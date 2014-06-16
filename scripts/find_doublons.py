# -*- coding: utf-8 -*-

"""
Ce script prend un corpus en entrée et détermine les doublons

"""

import argparse
import logging
import sys
from gensim import corpora, similarities, models

import utils

parser = argparse.ArgumentParser(description="""Ce script prend un corpus en entrée et détermine les doublons""")
parser.add_argument('corpus_name', type=str, help='Le nom du corpus')
parser.add_argument('-v', '--verbose', action='store_true',
                    help="Afficher les messages d'information")
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    
corpus_file = args.corpus_name + '_tfidf.mm'
index_file = args.corpus_name + '_tfidf_index'
docid_file = args.corpus_name + '_docid.txt'
        
try:
    corpus = corpora.mmcorpus.MmCorpus(corpus_file)
except Exception:
    raise IOError('Impossible de charger le fichier %s' % (corpus_file))
        
try:
    index = similarities.docsim.Similarity.load(index_file)
except Exception:
    raise IOError('Impossible de charger le fichier %s' % (index_file))
    
o = open('doublons_' + args.corpus_name + '.txt', 'w')
    
for i, doc in enumerate(corpus):
    sims = index[doc]   
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    
    second_neighbour, score = sims[1]
    
    if score > 0.8:
        o.write(str(utils.get_article_by_corpus_number(i, docid_file)) + '\t' + str(utils.get_article_by_corpus_number(second_neighbour, docid_file)) + '\n')
        
    print i
    
o.close()
