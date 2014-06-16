# -*- coding: utf-8 -*-

"""
Ce script prend l'id d'un article en entrée, et renvoie 5 articles proches

"""

import argparse
import logging
import sys
from gensim import corpora, similarities, models

import utils

def find_similar_articles(corpus_name, method, id=None, content=None):

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
        
    if id is not None:  
        corpus_id = utils.get_article_by_id(id, docid_file)
        tokens = corpus[corpus_id]

    elif content is not None:
        dico_file = corpus_name + '_wordids.txt'

        try:
            id2word = corpora.dictionary.Dictionary.load_from_text(dico_file)
        except Exception:
            raise IOError("Impossible de charger le fichier %s" % (dico_file))
            
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
    
    else:
        raise Exception("Il faut fournir un id ou un contenu")
    
    sims = index[tokens]   
    sims = sorted(enumerate(sims), key=lambda item: -item[1])

    return [(utils.get_article_by_corpus_number(x[0], docid_file), x[1]) for x in sims[:5]]

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="""Ce script prend l'id d'un article en entrée, et renvoie 5 articles proches""")
    parser.add_argument('corpus_name', type=str, help='Le nom du corpus')
    parser.add_argument('method', type=str, help="La méthode utilisée (lda, lsi, tfidf)")
    parser.add_argument('--id', type=int, help="L'id de l'article")
    parser.add_argument('--file', type=str, help="Un fichier contenant du texte")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Afficher les messages d'information")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    
    if args.id:
        print find_similar_articles(args.corpus_name, args.method, id=args.id)
    else:
        with open(args.file) as f:
            content = unicode(f.read(), 'utf8')
            print find_similar_articles(args.corpus_name, args.method, content=content)

