# -*- coding: utf-8 -*-
"""
À partir d'un corpus de textes donné sous la forme d'un fichier tsv
contenant un texte par ligne, on génère trois fichiers :

    - nom_du_corpus_wordids.txt : un tableau associant à chaque mot du corpus
    un identifiant entier.

    - nom_du_corpus_bow.mm : la représentation matricielle du corpus, où chaque
    document est vu comme un vecteur de taille N = le nombre de mots dans le corpus.
    La coordonnée i du vecteur indique le nombre de fois que le mot d'identifiant i
    apparaît dans le document.

    - nom_du_corpus_docid.txt : un fichier contenant un entier par ligne.
    L'entier à la ligne i est l'id_article (donné dans le fichier tsv) du document
    n°i du corpus.
"""

import logging
import os
import argparse

import utils
import habeascorpus
from gensim import corpora, similarities


# Les arguments à fournir en ligne de commande
parser = argparse.ArgumentParser(description="""Génère la représentation matricielle
associée à un corpus""")
parser.add_argument('file_path', type=str, help='Le fichier .tsv(.gz) contenant le corpus')
parser.add_argument('--stopwords', type=str, help='Un fichier contenant un stopword par ligne')
parser.add_argument('-v', '--verbose', action='store_true',
                    help="Afficher les messages d'information")
args = parser.parse_args()

# L'option -v affiche les messages d'information
if args.verbose:
    logging.basicConfig(asctime='%(s)levelname : %(format)s : %(message)s', level=logging.INFO)

input_file = utils.split_path(args.file_path)
if (os.path.isfile(input_file['name'] + '_bow.mm')):
    raise IOError("Le corpus existe déjà sous forme matricielle")

# Les stopwords qui doivent être ignorés lors de la tokenization
if args.stopwords:
    with open(args.stopwords) as f:
        stopwords = [line.rstrip() for line in f]
else:
    stopwords = []

corpus = habeascorpus.HabeasCorpus(input_file['path'], stopwords)

# Suppression des mots pas assez/trop fréquents
corpus.dictionary.filter_extremes(no_below=5, no_above=0.5)

# Enregistrement du dictionnaire de mots
corpus.dictionary.save_as_text(input_file['name'] + '_wordids.txt')

# Enregistrement du corpus au format bag-of-words
corpora.mmcorpus.MmCorpus.serialize(input_file['name'] + '_bow.mm', corpus, progress_cnt=1000)

# Création d'un fichier qui à la ligne n°i affiche l'id du document corpus[i]
with open(input_file['path']) as f:
    o = open(input_file['name'] + '_docid.txt', 'w')
    f.readline()
    for raw_line in f:
        doc = utils.Document(raw_line)
        o.write(doc.id + '\t' + doc.title + '\n')
    o.close()
