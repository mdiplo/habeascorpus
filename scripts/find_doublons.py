# -*- coding: utf-8 -*-

"""
Ce script prend un corpus en entrée et détermine les documents doublons

"""

import argparse
import logging
import sys, os
from gensim import corpora, similarities, models

import utils

import habeascorpus as hc

# Les arguments à fournir en ligne de commande
parser = argparse.ArgumentParser(description="""Ce script prend un corpus en entrée et détermine les documents doublons""")
parser.add_argument('corpus', type=str, help='Le nom du corpus')
parser.add_argument('-v', '--verbose', action='store_true',
                    help="Afficher les messages d'information")
args = parser.parse_args()

# L'option -v affiche les messages d'information
if args.verbose:
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    
corpus_file = os.path.join(hc.modelsdir, args.corpus + '_tfidf.mm')
index_file = os.path.join(hc.modelsdir, args.corpus + '_tfidf_index')
docid_file = os.path.join(hc.modelsdir, args.corpus + '_docid.txt')
doublons_file = os.path.join(hc.modelsdir, 'doublons_' + args.corpus + '.txt')

# Chargement du corpus     
try:
    corpus = corpora.mmcorpus.MmCorpus(corpus_file)
except Exception:
    raise IOError("""Impossible de charger le fichier %s. Avez-vous bien appliqué le script corpus_to_matrix.py""" % (corpus_file))

# Chargement du fichier d'index     
try:
    index = similarities.docsim.Similarity.load(index_file)
except Exception:
    raise IOError("""Impossible de charger le fichier %s. Avez-vous bien appliqué le script tfidf.py avec l'option --saveindex ?"""% (index_file))

# Les doublons sont enregistrés
with open(doublons_file, 'w') as o:
    
    for i, doc in enumerate(corpus):

        # Pour chaque article, on trie ses voisins et on s'intéresse au deuxième plus proche
        # (le premier plus proche est l'article lui-même')
        # Si le deuxième voisin a un score de proximité supérieur à une certaine valeur,
        # Il s'agit d'un doublon
        sims = index[doc]   
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        second_neighbour, score = sims[1]
        
        if score > 0.8:
            o.write(str(utils.get_article_by_corpus_number(i, docid_file)) + '\t' + str(utils.get_article_by_corpus_number(second_neighbour, docid_file)) + '\n')
        
        if args.verbose:
            print ("Document n°%d traité" % i)
