# -*- coding: utf-8 -*-

"""
Ce script prend en entrée un contenu (sous la forme d'un id d'article ou 
d'un texte en entrée standard) et renvoie les 5 articles les plus proches
dans une base donnée.

"""

import argparse
import os
import logging
import sys
import json
import time
from gensim import corpora, similarities, models

import utils

def find_similar_articles(corpus_name, method, content, n=5, data_dir=os.getcwd(), index=None, id2word=None, corpus=None, model=None):

    """
    - corpus_name : Le nom du corpus sur lequel on travaille (fichier .tsv 
        sans l'extension .tsv)
        
    - method : ldan (n = le nombre de topics), lsin ou tfidf
    
    - content : un texte
    
    - n: le nombre d'articles proches voulus
    
    Renvoie les n articles de corpus_name les plus proches du contenu spécifié 
    
    """
    
    debut = time.clock()
    print ("Début %f" %(debut))
    
    corpus_file = os.path.join(data_dir, corpus_name + '_' + method + '.mm')
    index_file = os.path.join(data_dir, corpus_name + '_' + method + '_index')
    docid_file = os.path.join(data_dir, corpus_name + '_docid.txt')
    
    # Chargement du corpus
    if not corpus:
        try:
            corpus = corpora.mmcorpus.MmCorpus(corpus_file)
        except Exception:
            raise IOError('Impossible de charger le fichier %s. Avez-vous bien appliqué le script corpus_to_matrix.py ?' % (corpus_file))
            
        print ("Après chargement du corpus %f" %(time.clock()))

    # Chargement du fichier d'index, s'il n'est pas fourni en argument
    if not index:
        try:
            index = similarities.docsim.Similarity.load(index_file)
        except Exception:
            raise IOError("""Impossible de charger le fichier %s. Avez-vous bien appliqué le script %s avec l'option --saveindex ?""" % (method, index_file))
            
        print ("Après chargement du fichier d'index %f" %(time.clock()))

    dico_file = os.path.join(data_dir, corpus_name + '_wordids.txt')

    # Chargement du dictionnaire
    if not id2word:
        try:
            id2word = corpora.dictionary.Dictionary.load_from_text(dico_file)
        except Exception:
            raise IOError("Impossible de charger le fichier %s" % (dico_file))
            
        print ("Après chargement du dictionnaire %f" %(time.clock()))

    # Chargement du modèle correspondant à la méthode voulue par l'utilisateur
    if not model:
        if method == 'tfidf':
            model_file = os.path.join(data_dir, corpus_name + '_tfidf_model')
            model = models.tfidfmodel.TfidfModel.load(model_file)

        elif method.startswith('lsi'):
            model_file = os.path.join(data_dir, corpus_name + '_' + args.method + '_model')
            model = models.lsimodel.LsiModel.load(model_file)

        elif method.startswith('lda'):
            model_file = os.path.join(data_dir, corpus_name + '_' + args.method + '_model')
            model = models.ldamodel.LdaModel.load(model_file)
            
        print ("Après chargement du modèle %f" %(time.clock()))

    tokens = model[id2word.doc2bow(utils.tokenize(content))]

    # Renvoi des 5 articles les plus proches 
    sims = index[tokens]
    print ("Après sims= %f" %(time.clock()))
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    print ("Après le tri %f" %(time.clock()))
    
    fin = time.clock()
    print ("Temps d'éxécution total %f" %(fin - debut))
    
    return [{'id': utils.get_article_by_corpus_number(x[0], docid_file), 'score': round(x[1], 2)} for x in sims[:n]]  # faut-il vérifier que sims[:n] est licite ?

if __name__ == '__main__':

    # Les arguments à fournir en ligne de commande
    parser = argparse.ArgumentParser(description="""Ce script prend l'id d'un article en entrée, et renvoie 5 articles proches""")
    parser.add_argument('corpus_name', type=str, help='Le nom du corpus')
    parser.add_argument('method', type=str, help="La méthode utilisée (lda, lsi, tfidf)")
    parser.add_argument('-v', '--verbose', action='store_true',
            help="Afficher les messages d'information")
    args = parser.parse_args()

    # L'option -v affiche les messages d'information
    if args.verbose:
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        
    content = utils.textimport(sys.stdin.read())
    print (find_similar_articles(args.corpus_name, args.method, content=content))

