# -*- coding: utf-8 -*-
"""
À partir d'un corpus au format bag-of-words sous forme d'un fichier Matrix Market (.mm)
et du dictionnaire associé, ce script applique l'algorithme TFIDF et génère un fichier :

    - nom_du_corpus_tfidf.mm : La représentation matricielle du corpus une fois appliqué
    l'algorithme TFIDF à chaque document

"""

import logging
import os
import argparse
import glob
import json
from gensim import corpora, models, similarities

parser = argparse.ArgumentParser(description="""Applique l'algorithme TFIDF sur un corpus""")
parser.add_argument('corpus_name', type=str,
                    help="Le nom du corpus (i.e le nom du fichier sans l'extension .tsv)")
parser.add_argument('--saveindex', action='store_true',
                    help="Si vrai, le script enregistre l'index de similarité pour le corpus'")
parser.add_argument('-v', '--verbose', action='store_true',
                    help="Afficher les messages d'information")
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

corpus_file = args.corpus_name + '_bow.mm'
dictionary_file = args.corpus_name + '_wordids.txt'

try:
    corpus = corpora.mmcorpus.MmCorpus(corpus_file)
except Exception:
    raise IOError("""Impossible d'ouvrir le fichier %s""" % corpus_file)

try:
    id2word = corpora.dictionary.Dictionary.load_from_text(dictionary_file)
except Exception:
    raise IOError("""Impossible d'ouvrir le fichier %s""" % dictionary_file)

tfidf = models.tfidfmodel.TfidfModel(corpus=corpus, id2word=id2word)
tfidf.save(args.corpus_name + '_tfidf_model')
corpora.mmcorpus.MmCorpus.serialize(args.corpus_name + '_tfidf.mm', tfidf[corpus], progress_cnt=1000)

if args.saveindex:
    corpus = corpora.mmcorpus.MmCorpus(args.corpus_name + '_tfidf.mm')
    index = similarities.docsim.Similarity(os.path.join(os.getcwd(), args.corpus_name + '_tfidf_index'), corpus, num_features=corpus.num_terms)
    index.save(args.corpus_name + '_tfidf_index')
