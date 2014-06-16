# -*- coding: utf-8 -*-

"""
Ce script prend un texte en entrée, et un fichier contenant les représentations
bag-of-words d'un corpus, puis détermine si le texte possède une traduction dans
le corpus

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


    gs = goslate.Goslate(timeout=100)
    text = gs.translate(text, 'fr')
    #text = unicode(text, 'utf8')
    
    try:
        dico = corpora.Dictionary.load_from_text(dic_path)
    except Exception:
        raise IOError('Impossible de charger le fichier %s' % (dic_path))
        
    try:
        corpus = corpora.mmcorpus.MmCorpus(corpus_path)
    except Exception:
        raise IOError('Impossible de charger le fichier %s' % (corpus_path))
        
    try:
        tfidfmodel = models.tfidfmodel.TfidfModel.load(tfidfmodel_path)
    except Exception:
        raise IOError('Impossible de charger le fichier %s' % (tfidfmodel_path))
        
    try:
        index = similarities.docsim.Similarity.load(index_file)
    except Exception:
        raise IOError('Impossible de charger le fichier %s' % (index_file))

    vec_bow = dico.doc2bow(utils.tokenize(text))
    vec_tfidf = tfidfmodel[vec_bow]

    sims = index[vec_tfidf]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    
    return (utils.get_article_by_corpus_number(sims[0][0], docid_path), sims[0][1])
    
    #distance = lambda vec1, vec2 : vec1 + vec2 

    #neighbour_index = -1
    #max_similarity = -1
    #best_vec = []

    #print vec_tfidf

    #for i, document in enumerate(corpus):
    #    distance_from_vec_tfidf = utils.similarity_measure(vec_tfidf, document, distance)
    #    print (utils.get_article_by_corpus_number(i+1, docid_path), distance_from_vec_tfidf)
    #    if distance_from_vec_tfidf > max_similarity:
    #        neighbour_index = i
    #        max_similarity = distance_from_vec_tfidf
    #        best_vec = document
    #        
    #print (utils.get_article_by_corpus_number(neighbour_index, docid_path), max_similarity)
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="""Vérifie si le texte en entrée standard possède une traduction dans le corpus""")
    parser.add_argument('corpus_name', type=str, help='Le nom du corpus')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Afficher les messages d'information")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO) -v
        
    print find_translation(sys.stdin.read(), args.corpus_name)

