# -*- coding: utf-8 -*-

"""
Ce script prend un texte en entrée, et un fichier contenant les représentations
bag-of-words d'un corpus, puis détermine si le texte possède une traduction dans
le corpus

"""

import sys
import argparse
import logging
import numpy
from gensim import corpora, similarities, models

import utils

parser = argparse.ArgumentParser(description="""Vérifie si le texte en entrée standard possède une traduction dans le corpus""")
parser.add_argument('corpus_name', type=str, help='Le nom du corpus')
parser.add_argument('-v', '--verbose', action='store_true',
                    help="Afficher les messages d'information")
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO) -v
    

dic_path = args.corpus_name + '_wordids.txt'
corpus_path = args.corpus_name + '_tfidf.mm'
index_path = args.corpus_name + '_index'
tfidfmodel_path = args.corpus_name + '_tfidfmodel'
docid_path = args.corpus_name + '_docid.txt'

text = sys.stdin.read()

try:
    dico = corpora.Dictionary.load_from_text(dic_path)
except Exception:
    raise IOError('Impossible de charger le fichier %s' % (dic_path))
    
try:
    corpus = corpora.mmcorpus.MmCorpus(corpus_path)
except Exception:
    raise IOError('Impossible de charger le fichier %s' % (corpus_path))
    
try:
    tfidfmodel = models.tfidfmodel.TfidfModel.load(tfidfmodel_path)
except Exception:
    raise IOError('Impossible de charger le fichier %s' % (tfidfmodel_path))

document = utils.Document(text)
vec_bow = dico.doc2bow(document.get_text_tokens())
vec_tfidf = tfidfmodel[vec_bow]

distance = lambda vec1, vec2 : vec1 + vec2 

neighbour_index = -1
max_similarity = -1
best_vec = []

print vec_tfidf

for i, document in enumerate(corpus):
    distance_from_vec_tfidf = utils.similarity_measure(vec_tfidf, document, distance)
    print (utils.get_article_by_corpus_number(i+1, docid_path), distance_from_vec_tfidf)
    if distance_from_vec_tfidf > max_similarity:
        neighbour_index = i
        max_similarity = distance_from_vec_tfidf
        best_vec = document
        
print (utils.get_article_by_corpus_number(neighbour_index, docid_path), max_similarity)

