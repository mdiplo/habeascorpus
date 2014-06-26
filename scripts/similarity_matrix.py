# -*- coding: utf-8 -*-

"""
Ce script prend un corpus en entrée et génère la matrice de similarité pour
ce corpus : pour chaque article du corpus, on enregistre les 5 articles les plus
proches et le score de proximité.

"""

import argparse
import logging
import sys
from gensim import corpora, similarities, models

import utils

# Les arguments à fournir en ligne de commande
parser = argparse.ArgumentParser(description="""Ce script prend un corpus en entrée et génère la matrice de similarité pour ce corpus.""")
parser.add_argument('corpus_name', type=str, help='Le nom du corpus')
parser.add_argument('method', type=str, help="La méthode utilisée (lda, lsi, tfidf)")
parser.add_argument('-v', '--verbose', action='store_true',
        help="Afficher les messages d'information")
args = parser.parse_args()

# L'option -v affiche les messages d'information
if args.verbose:
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        
corpus_file = args.corpus_name + '_' + args.method + '.mm'
index_file = args.corpus_name + '_' + args.method + '_index'
docid_file = args.corpus_name + '_docid.txt'

# Chargement du corpus
try:
    corpus = corpora.mmcorpus.MmCorpus(corpus_file)
except Exception:
    raise IOError("""Impossible de charger le fichier %s. Avez-vous bien appliqué le script %s ?""" % (args.method, corpus_file))

# Chargement du fichier d'index
try:
    index = similarities.docsim.Similarity.load(index_file)
except Exception:
    raise IOError("""Impossible de charger le fichier %s. Avez-vous bien appliqué le script %s avec l'option --saveindex ?""" % (index_file, method))
    
with open(args.corpus_name + '_' + args.method + '_similarity_matrix.csv', 'w') as o:

    for i, document in enumerate(corpus):
    
        # Pour chaque article d, on trie les autres articles par proximité décroissante
        # avec d, et on écrit dans un fichier l'id et le score de proximité pour les 5
        # plus proches
        sims = index[document]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        
        o.write(str(utils.get_article_by_corpus_number(i, docid_file)) + '\t')
        o.write('\t'.join([str((utils.get_article_by_corpus_number(x[0], docid_file), x[1])) for x in sims[1:6]]))
        o.write('\n')
        
        if args.verbose:
            print """Article n°%d traité""" % (i)

        

