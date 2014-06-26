# -*- coding: utf-8 -*-

"""
Ce script prend en entrée un contenu (sous la forme d'un id d'article ou 
d'un texte en entrée standard) et renvoie les 5 articles les plus proches
dans une base donnée.

"""

import argparse
import logging
import sys
from gensim import corpora, similarities, models

import utils

def find_similar_articles(corpus_name, method, id=None, content=None):

    """
    - corpus_name : Le nom du corpus sur lequel on travaille (fichier .tsv 
        sans l'extension .tsv)
        
    - method : ldan (n = le nombre de topics), lsin ou tfidf
    
    - id : l'id d'un article du corpus corpus_name
    
    - content : un texte
    
    Renvoie les 5 articles de corpus_name les plus proches du contenu spécifié 
    via l'id ou via un contenu
    
    """

    corpus_file = corpus_name + '_' + method + '.mm'
    index_file = corpus_name + '_' + method + '_index'
    docid_file = corpus_name + '_docid.txt'

    # Chargement du corpus
    try:
        corpus = corpora.mmcorpus.MmCorpus(corpus_file)
    except Exception:
        raise IOError('Impossible de charger le fichier %s. Avez-vous bien appliqué le script corpus_to_matrix.py ?' % (corpus_file))

    # Chargement du fichier d'index
    try:
        index = similarities.docsim.Similarity.load(index_file)
    except Exception:
        raise IOError("""Impossible de charger le fichier %s. Avez-vous bien appliqué le script %s avec l'option --saveindex ?""" % (method, index_file))

    # L'utilisateur veut connaitre les articles proches d'un article spécifié via son id
    if id is not None:  
        corpus_id = utils.get_article_by_id(id, docid_file)
        tokens = corpus[corpus_id]

    # L'utilisateur veut connaitre les articles proches d'un article spécifié via son contenu
    elif content is not None:
        dico_file = corpus_name + '_wordids.txt'

    # Chargement du dictionnaire
        try:
            id2word = corpora.dictionary.Dictionary.load_from_text(dico_file)
        except Exception:
            raise IOError("Impossible de charger le fichier %s" % (dico_file))

        # Chargement du modèle correspondant à la méthode voulue par l'utilisateur
        if method == 'tfidf':
            model_file = corpus_name + '_tfidf_model'
            model = models.tfidfmodel.TfidfModel.load(model_file)

        elif method.startswith('lsi'):
            model_file = corpus_name + '_' + args.method + '_model'
            model = models.lsimodel.LsiModel.load(model_file)

        elif method.startswith('lda'):
            model_file = corpus_name + '_' + args.method + '_model'
            model = models.ldamodel.LdaModel.load(model_file)

        tokens = model[id2word.doc2bow(utils.tokenize(content))]

    # L'utilisateur doit spécifier du contenu
    else:
        raise Exception("Il faut fournir un id ou un contenu")

    # Renvoi des 5 articles les plus proches 
    sims = index[tokens]   
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    return [(utils.get_article_by_corpus_number(x[0], docid_file), x[1]) for x in sims[:5]]

if __name__ == '__main__':

    # Les arguments à fournir en ligne de commande
    parser = argparse.ArgumentParser(description="""Ce script prend l'id d'un article en entrée, et renvoie 5 articles proches""")
    parser.add_argument('corpus_name', type=str, help='Le nom du corpus')
    parser.add_argument('method', type=str, help="La méthode utilisée (lda, lsi, tfidf)")
    parser.add_argument('--id', type=int, help="L'id de l'article")
    parser.add_argument('-v', '--verbose', action='store_true',
            help="Afficher les messages d'information")
    args = parser.parse_args()

    # L'option -v affiche les messages d'information
    if args.verbose:
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    if args.id:
        print find_similar_articles(args.corpus_name, args.method, id=args.id)
        
    # Si aucun id n'est fourni, le script assume que le contenu est l'entrée standard
    else:
        content = unicode(sys.stdin.read(), 'utf8')
        print content
        print find_similar_articles(args.corpus_name, args.method, content=content)

