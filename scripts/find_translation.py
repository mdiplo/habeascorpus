# -*- coding: utf-8 -*-

"""
Ce script prend un texte en entrée, et un fichier contenant les représentations
bag-of-words d'un corpus, puis détermine si le texte possède une traduction dans
le corpus.
Pour cela, on traduit en français le texte spécifié, et on renvoie le plus proche
voisin de la traduction dans le corpus.

"""

import sys
import argparse
import logging
import numpy
import goslate
from gensim import corpora, similarities, models

import utils
    

def find_translation(text, corpus_name):
    dic_path = corpus_name + '_wordids.txt'
    corpus_path = corpus_name + '_tfidf.mm'
    index_file = corpus_name + '_tfidf_index'
    tfidfmodel_path = corpus_name + '_tfidf_model'
    docid_path = corpus_name + '_docid.txt'

    # On traduit en français le texte fourni par l'utilisateur
    # Utilise l'API google qui détexte automatiquement le langage 
    gs = goslate.Goslate(timeout=100)
    text = gs.translate(text, 'fr')
    
    # Chargement du corpus 
    try:
        corpus = corpora.mmcorpus.MmCorpus(corpus_path)
    except Exception:
        raise IOError("""Impossible de charger le fichier %s. Avez-vous bien appliqué le script corpus_to_matrix.py ?""" % (corpus_path))
        
    # Chargement du dictionnaire
    try:
        dico = corpora.Dictionary.load_from_text(dic_path)
    except Exception:
        raise IOError('Impossible de charger le fichier %s' % (dic_path))
      
    # Chargement du modèle  
    try:
        tfidfmodel = models.tfidfmodel.TfidfModel.load(tfidfmodel_path)
    except Exception:
        raise IOError("""Impossible de charger le fichier %s. Avez-vous bien appliqué le script tfidf.py ?""" % (tfidfmodel_path))
     
    # Chargement du fichier d'index   
    try:
        index = similarities.docsim.Similarity.load(index_file)
    except Exception:
        raise IOError("""Impossible de charger le fichier %s. Avez-vous bien appliqué le script tfidf avec l'option --saveindex ?""" % (index_file))

    # On tokenize le texte fourni grâce au dictionnaire
    vec_bow = dico.doc2bow(utils.tokenize(text))
    
    # On applique la transformation tfidf 
    vec_tfidf = tfidfmodel[vec_bow]
    
    # On renvoie le plus proche voisin de la traduction dans le corpus
    sims = index[vec_tfidf]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    return (utils.get_article_by_corpus_number(sims[0][0], docid_path), sims[0][1])
    
if __name__ == '__main__':

    # Les arguments à fournir en ligne de commande
    parser = argparse.ArgumentParser(description="""Vérifie si le texte en entrée standard possède une traduction dans le corpus""")
    parser.add_argument('corpus_name', type=str, help='Le nom du corpus')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Afficher les messages d'information")
    args = parser.parse_args()

    # L'option -v affiche les messages d'information
    if args.verbose:
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO) -v
    
    # Affiche la traduction du texte fourni en entrée standard   
    print find_translation(sys.stdin.read(), args.corpus_name)

