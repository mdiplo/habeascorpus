# -*- coding: utf-8 -*-
"""
À partir d'un corpus au format bag-of-words sous forme d'un fichier Matrix Market (.mm)
et du dictionnaire associé, ce script applique l'algorithme LSI et génère :

    - nom_du_corpus_lsi_nbtopics.mm : La représentation matricielle du corpus une fois appliqué
    l'algorithme LSI à chaque document
"""

import logging
import os
import argparse
import glob
import json
from gensim import corpora, models, similarities

import habeascorpus as hc

# Les arguments à fournir en ligne de commande
parser = argparse.ArgumentParser(description="""Applique l'algorithme LSI sur un corpus""")
parser.add_argument('corpus', type=str,
                    help="Le nom du corpus (i.e le nom du fichier sans l'extension .tsv)")
parser.add_argument('nb_topics', type=int,
                    help="Le nombre de topics voulus")
parser.add_argument('--saveindex', action='store_true',
                    help="Si vrai, le script enregistre l'index de similarité pour le corpus")
parser.add_argument('-v', '--verbose', action='store_true',
                    help="Afficher les messages d'information")
args = parser.parse_args()

# L'option -v affiche les messages d'information
if args.verbose:
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    
corpus_file = os.path.join(hc.modelsdir, args.corpus + '_bow.mm')
dictionary_file = os.path.join(hc.modelsdir, args.corpus + '_wordids.txt')
lsi_file = os.path.join(hc.modelsdir, args.corpus + '_lsi')

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

# Application de l'algorithme LSI
lsi = models.lsimodel.LsiModel(corpus=corpus, id2word=id2word, num_topics=args.nb_topics)

# Enregistrement du modèle
lsi.save(lsi_file  + str(args.nb_topics) + '_model')

# Enregistrement du corpus LSI-ifié
corpora.mmcorpus.MmCorpus.serialize(lsi_file + str(args.nb_topics) + '.mm', lsi[corpus], progress_cnt=1000)

# L'option --saveindex enregistre un fichier d'index qui permet de faire de la
# recherche de similarité entre les articles
if args.saveindex:
    corpus = corpora.mmcorpus.MmCorpus(lsi_file + str(args.nb_topics) + '.mm')
    index = similarities.docsim.Similarity(lsi_file + str(args.nb_topics) + '_index', corpus, num_features=corpus.num_terms)
    index.save(lsi_file + str(args.nb_topics) + '_index')
