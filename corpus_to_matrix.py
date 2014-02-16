# -*- coding: utf-8 -*-
"""
À partir d'un corpus de textes donné sous la forme d'un fichier csv 
contenant un texte par ligne, on génère trois fichiers :

    - nom_du_corpus_wordids.txt : un tableau associant à chaque mot du corpus
    un identifiant entier.
    
    - nom_du_corpus_bow.mm : la représentation matricielle du corpus, où chaque
    document est vu comme un vecteur de taille N = le nombre de mots dans le corpus.
    La coordonnée i du vecteur indique le nombre de fois que le mot d'identifiant i
    apparaît dans le document.
    
    - nom_du_corpus_docnums.txt : un fichier contenant un entier par ligne.
    L'entier à la ligne i est l'id_article (donné dans le fichier csv) du document
    n°i du corpus.
"""

import logging  
import os
import argparse

import utils
import habeascorpus
from gensim import corpora

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

parser = argparse.ArgumentParser(description="""Génère la représentation matricielle 
associée à un corpus""");
parser.add_argument('file_path', type=str, help='Le fichier .csv contenant le corpus')
arg = parser.parse_args()

input_file = utils.split_path(arg.file_path)

if (os.path.isfile(input_file['name'] + '_bow.mm')):
    raise IOError("Le corpus existe déjà sous forme matricielle")

with open(input_file['path'], 'r') as f, open(input_file['name'] + '_docnums.txt', 'w') as num_articles:
    f.readline() #On passe la première ligne qui contient le nom des colonnes
    for i, raw_line in enumerate(f):
        try : 
            id_article = raw_line.split('\t')[0]
        except Exception: 
            raise ValueError("La ligne n°%d n'est pas au bon format" % (i+1))
        
        num_articles.write(id_article + '\n')
        
corpus = habeascorpus.HabeasCorpus(input_file['path'])
corpus.dictionary.filter_extremes(no_below=3, no_above=0.5)
corpus.dictionary.save_as_text(input_file['name'] + '_wordids.txt')
corpora.mmcorpus.MmCorpus.serialize(input_file['name'] + '_bow.mm', corpus, progress_cnt=1000)
