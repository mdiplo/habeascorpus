# -*- coding: utf-8 -*-

"""
Ce script prend l'id d'un article en entrée, et renvoie 5 articles proches

"""

import argparse
import logging
from gensim import corpora, similarities, models

import utils

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="""Ce script prend l'id d'un article en entrée, et renvoie 5 articles proches""")
    parser.add_argument('corpus_name', type=str, help='Le nom du corpus')
    parser.add_argument('method', type=str, help="La méthode utilisée (lda, lsi, tfidf)")
    parser.add_argument('id', type=int, help="L'id de l'article")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Afficher les messages d'information")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        

    tfidf_corpus_file = args.corpus_name + '_' + args.method + '.mm'
    index_file = args.corpus_name + '_' + args.method + '_index'

    docid_file = args.corpus_name + '_docid.txt'

def find_similar_articles(corpus_name, method, id):

    corpus_file = corpus_name + '_' + method + '.mm'
    index_file = corpus_name + '_' + method + '_index'
    docid_file = corpus_name + '_docid.txt'
    
    try:
        corpus = corpora.mmcorpus.MmCorpus(corpus_file)
    except Exception:
        raise IOError('Impossible de charger le fichier %s' % (corpus_file))
        
    try:
        index = similarities.docsim.Similarity.load(index_file)
    except Exception:
        raise IOError('Impossible de charger le fichier %s' % (index_file))
        
    corpus_id = utils.get_article_by_id(id, docid_file)

    sims = index[corpus[corpus_id]]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])

    return [(utils.get_article_by_corpus_number(x[0], docid_file), x[1]) for x in sims[:5]]
