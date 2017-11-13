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

import habeascorpus as hc

# Les arguments à fournir en ligne de commande
parser = argparse.ArgumentParser(description="""Applique l'algorithme TFIDF sur un corpus""")
parser.add_argument('corpus', type=str,
                    help="Le nom du corpus (i.e le nom du fichier sans l'extension .tsv)")
parser.add_argument('--saveindex', action='store_true',
                    help="Si vrai, le script enregistre l'index de similarité pour le corpus'")
parser.add_argument('-v', '--verbose', action='store_true',
                    help="Afficher les messages d'information")
args = parser.parse_args()

# L'option -v affiche les messages d'information
if args.verbose:
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

corpus_file = os.path.join(hc.modelsdir, args.corpus + '_bow.mm')
dictionary_file = os.path.join(hc.modelsdir, args.corpus + '_wordids.txt')
tfidf_file = os.path.join(hc.modelsdir, args.corpus + '_tfidf_model')
tfidfmm_file = os.path.join(hc.modelsdir, args.corpus + '_tfidf.mm')
tfidfindex_file = os.path.join(hc.modelsdir, args.corpus + '_tfidf_index')

# Chargement du corpus
try:
    corpus = corpora.mmcorpus.MmCorpus(corpus_file)
except Exception:
    raise IOError("""Impossible d'ouvrir le fichier %s. Avez-vous bien appliqué le script corpus_to_matrix.py ?""" % corpus_file)

# Chargement du dictionnaire
try:
    id2word = corpora.dictionary.Dictionary.load_from_text(dictionary_file)
except Exception:
    raise IOError("""Impossible d'ouvrir le fichier %s""" % dictionary_file)

# Application de l'algorithme TFIDF
tfidf = models.tfidfmodel.TfidfModel(corpus=corpus, id2word=id2word)

# Enregistrement du modèle
tfidf.save(tfidf_file)

# Enregistrement du corpus TFIDF-ifié
corpora.mmcorpus.MmCorpus.serialize(tfidfmm_file, tfidf[corpus], progress_cnt=1000)

# L'option --saveindex enregistre un fichier d'index qui permet de faire de la
# recherche de similarité entre les articles
if args.saveindex:
    corpus = corpora.mmcorpus.MmCorpus(tfidfmm_file)
    index = similarities.docsim.Similarity(tfidfindex_file, corpus, num_features=corpus.num_terms)
    index.save(tfidfindex_file)
